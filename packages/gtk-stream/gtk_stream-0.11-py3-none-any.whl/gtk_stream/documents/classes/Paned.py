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

class Paned(Document):
    __g_class__ = Gtk.Paned
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render(self):
        if len(self.children) == 1:
            return self.children[0].render()
        
        l = self.children[0].render()
        for (r,rem_size) in zip(self.children[1:], range(len(self.children),1,-1)):
            j = Gtk.Paned()
            j.set_shrink_start_child(False)
            j.set_shrink_end_child(False)
            j.props.start_child = l
            j.props.end_child = r.render()
            self.set_properties(j)
            l = j
        return l
