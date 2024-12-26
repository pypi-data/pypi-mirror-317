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
from .. import Document, PseudoDocument

class FlowBoxPrepend(PseudoDocument):
    def __init__(self, app):
        super().__init__(app)

class FlowBox(Document):
    __g_class__ = Gtk.FlowBox
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.FlowBox()
    def insert_child(self, w, d):
        if isinstance(d, FlowBoxPrepend):
            w.prepend(d.render())
        else:
            w.append(d.render())
