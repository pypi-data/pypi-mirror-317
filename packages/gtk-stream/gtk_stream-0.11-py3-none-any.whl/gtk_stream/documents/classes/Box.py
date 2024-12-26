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

class BoxPrepend(PseudoDocument):
    def __init__(self, app, after = None):
        super().__init__(app)
        self.after = after

class Box(Document):
    __g_class__ = Gtk.Box
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.Box()
    def insert_child(self, w, d):
        if isinstance(d, BoxPrepend):
            if d.after != None:
                w.insert_child_after(d.render(), self.app.namedWidgets[d.after])
            else:
                w.prepend(d.render())
        else:
            w.append(d.render())
