# Gtk-Stream : A stream-based GUI protocol
# Copyright (C) 2024  Marc Coiffier
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys

from . import Gtk

def _const(x):
    return lambda _: x
def _parse_orientation_property(val):
    return _const((Gtk.Orientation.HORIZONTAL) if val == "horizontal" else (Gtk.Orientation.VERTICAL))
def _parse_boolean_property(val):
    return _const(True if val == "true" else False)
def _parse_float_property(val):
    return _const(float(val))
def _parse_int_property(val):
    return _const(int(val))
def _parse_searchMode_property(val):
    match val:
        case 'exact':
            return _const(Gtk.StringFilterMatchMode.EXACT)
        case 'substring':
            return _const(Gtk.StringFilterMatchMode.SUBSTRING)
        case _:
            return _const(Gtk.StringFilterMatchMode.PREFIX)
def _parse_adjustment_property(val):
    adj = Gtk.Adjustment()
    start, end, *rest = val.split(':')
    adj.set_lower(int(start))
    adj.set_upper(int(end))
    if len(rest) > 0:
        default = rest[0]
    else:
        default = start
    adj.set_value(int(default))
    return _const(adj)
def _parse_css_classes_property(val):
    return _const(val.split())
def _parse_widget_property(val):
    return lambda app: app.namedWidgets[val]
        
_PARSE_TYPE_PROPERTY = {
    'GStrv'                    : _parse_css_classes_property,
    'GtkOrientation'           : _parse_orientation_property,
    'gdouble'                  : _parse_float_property,
    'gfloat'                   : _parse_float_property,
    'gint'                     : _parse_int_property,
    'gboolean'                 : _parse_boolean_property,
    'GtkStringFilterMatchMode' : _parse_searchMode_property,
    'GtkWidget'                : _parse_widget_property,
    'GtkAdjustment'            : _parse_adjustment_property,
    'gchararray'               : _const,
}

def parse_property(prop_type, val):
    # print(f"Parsing property '{val}' of type '{prop_type}'", file=sys.stderr)
    return _PARSE_TYPE_PROPERTY[prop_type](val)
def get_prop_type(klass, prop):
    try:
        return klass.find_property(prop).value_type.name
    except AttributeError:
        raise Exception(f"Unknown GTK property '{prop}' of class '{klass}'")
def set_parse_prop(app, w, prop_name, val):
    w.set_property(prop_name, parse_property(get_prop_type(w.__class__, prop_name), val)(app))
