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

from ... import Gtk
from .. import Document
from ...properties import parse_property

class Switch(Document):
    __g_class__ = Gtk.Switch
    def __init__(self, app, id, managed = "false", **kwargs):
        super().__init__(app, id=id, **kwargs)
        self.managed = parse_property('gboolean', managed)(app)
    def render_raw(self):
        ret = Gtk.Switch()
        self.connect_event(
            ret, 'state-set', 'switch', 
            retval   = self.managed,
            get_data = lambda _,state: "on" if state else "off")
        return ret
