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

from ... import Gtk, Gio, GObject
from .. import Document

class Item(Document):
    def __init__(self, app, value, **kwargs):
        super().__init__(app, **kwargs)
        self.child = None
        self.value = value
    def add_child(self, child):
        self.child = child
    def render(self):
        return self.child.render()
class _ItemObject(GObject.Object):
    def __init__(self, doc):
        super().__init__()
        self.doc = doc
        self.value = doc.value

    @GObject.Property(type=str)
    def item_value(self):
        return self.value
        
class Dropdown(Document):
    __g_class__ = Gtk.DropDown
    def __init__(self, app, id, **kwargs):
        super().__init__(app, id=id, **kwargs)
    def render_raw(self):
        model = Gio.ListStore(item_type=_ItemObject)
        for item in self.children:
            model.append(_ItemObject(item))

        factory = Gtk.SignalListItemFactory()
        def on_list_setup(_, list_item):
            list_item.item_value = None
        def on_list_bind(_, list_item):
            item = list_item.get_item()
            if list_item.item_value != item.value:
                list_item.item_value = item.value
                list_item.set_child(item.doc.render())
        factory.connect("setup", on_list_setup)
        factory.connect("bind", on_list_bind)

        ret = Gtk.DropDown(
            model=model,
            expression=Gtk.PropertyExpression.new(_ItemObject, None, 'item_value'),
            factory=factory)
        
        self.connect_event(
            ret, 'notify::selected-item', 'selected',
            get_data = lambda w,_: w.get_selected_item().value)
        return ret
    def insert_child(self, w, d):
        pass
