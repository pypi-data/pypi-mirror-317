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

class Cell(PseudoDocument):
    def __init__(self, app, x, y, w="1", h="1"):
        super().__init__(app)
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)

class Grid(Document):
    __g_class__ = Gtk.Grid
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

    def render_raw(self):
        return Gtk.Grid()
    def insert_child(self, w, d):
        w.attach(d.render(), d.x, d.y, d.w, d.h)
