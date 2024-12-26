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
from . import Gtk, GLib, Gdk
from .common import printEvent
from .properties import parse_property, get_prop_type, set_parse_prop

class _Object:
    pass

def app_message(name, store = None):
    """A decorator for methods that are both called from the pilot
    application and need access to the gtk main thread"""
    def app_message_f(f):
        def ret(self, *args, **kwargs):
            def cb():
                f(self, *args, **kwargs)
            self.run_when_idle(cb)
        ret.__tag_name__ = name
        ret.__store__ = store
        return ret
    return app_message_f

def single_store():
    store = _Object()
    def setChild(child):
        store.child = child
    return (lambda: store.child, setChild, None)
def multiple_store():
    children = []
    return (lambda: children, children.append, None)
def style_store():
    style = []
    return (lambda: " ".join(style),None, style.append)

class GtkStreamApp(Gtk.Application):
    def __init__(self, logger, name = None, **kwargs):
        super().__init__(**kwargs)
        self.logger = logger
        if name != None:
            GLib.set_application_name(name)
        self.namedWidgets = { }
        self.namedWindows = { }
        
        # The first messages from the pilot may arrive before the
        # application is ready to process them.
        # 
        # If that happens, store the actions until they can be taken
        # (when the "startup" signal is called)
        callback_queue = []
        def run_when_idle_before_startup(cb):
            callback_queue.append(cb)
        self.run_when_idle = run_when_idle_before_startup
        
        def on_startup(_):
            for cb in callback_queue:
                GLib.idle_add(cb)
            self.run_when_idle = GLib.idle_add
        self.connect('startup', on_startup)
        
    def nameWidget(self, id, w):
        if id is not None:
            self.namedWidgets[id] = w

    @app_message('file-dialog')
    def openFileDialog(self, id, parent):
        dialog = Gtk.FileDialog()
        dialog.props.modal = True
        def on_choose(_, b):
            try:
                file = dialog.open_finish(b)
                print(f"{id}:selected:{file.get_path()}")
                sys.stdout.flush()
            except GLib.GError as e:
                print(f"{id}:none-selected")
                sys.stdout.flush()
                
        dialog.open(parent = self.namedWindows[parent], callback = on_choose)

    @app_message('window', single_store)
    def newWindow(self, document, id, **attrs):
        win = Gtk.Window(application=self)
        for (attr_name, attr_val) in attrs.items():
            set_parse_prop(self, win, attr_name, attr_val)
        self.namedWindows[id] = win
        win.set_child(document.render())
        win.connect('close-request', printEvent(self.logger, 'close-request', id))
        win.present()

    @app_message('style', style_store)
    def addStyle(self, style):
        provider = Gtk.CssProvider()
        provider.load_from_data(style)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    @app_message('add-icon-path')
    def addIconPath(self, path):
        theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        theme.add_search_path(path)
        
    @app_message('close-window')
    def closeWindow(self, id):
        self.namedWindows[id].close()

    @app_message('remove')
    def removeWidget(self, id):
        w = self.namedWidgets[id]
        w.get_parent().remove(w)

    @app_message('insert', multiple_store)
    def insertWidgets(self, documents, into):
        for doc in documents:
            self.insertWidget(doc, into)

    def insertWidget(self, document, into):
        if into in self.namedWidgets:
            w = self.namedWidgets[into]
            w.insert_child(document)
        else:
            raise Exception(f"Error: unknown widget id '{into}'")
    
    @app_message('set-prop')
    def setProp(self, id, name, value):
        w = self.namedWidgets[id]
        w.set_property(name, parse_property(get_prop_type(w.__class__, name), value)(self))

