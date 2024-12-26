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

import functools
import threading
import signal
import sys
import xml.sax as sax

from . import GLib
from . import documents as docs

from .application import GtkStreamApp

WIDGET_DOCUMENTS = {
    'progress-bar'    : docs.ProgressBar,
    'label'           : docs.Label,
    'box'             : docs.Box,
    'box-prepend'     : docs.BoxPrepend,
    'button'          : docs.Button,
    'dropdown'        : docs.Dropdown,
    'item'            : docs.Item,
    'paned'           : docs.Paned,
    'grid'            : docs.Grid,
    'cell'            : docs.Cell,
    'frame'           : docs.Frame,
    'frame-label'     : docs.FrameLabel,
    'link'            : docs.LinkButton,
    'switch'          : docs.Switch,
    'picture'         : docs.Picture,
    'icon'            : docs.Icon,
    'separator'       : docs.Separator,
    'scrolled-window' : docs.ScrolledWindow,
    'stack'           : docs.Stack,
    'flow-box'        : docs.FlowBox,
    'flow-box-prepend': docs.FlowBoxPrepend,
    'entry'           : docs.Entry,
    'scale'           : docs.Scale
    
}

class GtkStreamXMLHandler(sax.ContentHandler):
    def __init__(self, logger):
        self.logger = logger
        self.transition_enter = self.transE_conn
        self.transition_leave = self.transL_final
        self.transition_chars = self.ignore_chars
        self.namedWidgets = { }
        self.windows = { }

    def quit_application(self):
        def cb():
            self.logger.info("Quitting app")
            self.app.quit()
        GLib.idle_add(cb)
        self.logger.info("Waiting for app to terminate")
        self.app_thread.join()
        self.logger.info("App terminated")
        sys.exit(0)

    def setNamed(self, attrs, ):
        if 'id' in attrs:
            self.namedWidgets[attrs['id']] = widget
    def ignore_chars(self, s):
        pass
        
    def transE_final(self, name, attrs):
        raise Exception(f"Unexpected tag '{name}'")
    def transL_final(self, name):
        raise Exception(f"Unexpected end tag '{name}'")
    def transL_tag(self, tag, enter, leave_parent, leave = None):
        def ret(name):
            if name == tag:
                if leave != None:
                    leave()
                self.transition_enter = enter
                self.transition_leave = leave_parent
            else:
                raise Exception(f"Error: expected end tag '{tag}', got '{name}'")
        return ret
                               
    def transE_conn(self, name, attrs):
        match name:
            case 'application':
                self.app = GtkStreamApp(self.logger, **attrs)
                def on_activate(a):
                    a.hold()
                self.app.connect('activate', on_activate)
                def appMain():
                    self.app.run([])
                self.app_thread = threading.Thread(target = appMain)
                self.app_thread.start()

                def on_sigint(a,b):
                    self.logger.info("SIGINT received")
                    self.quit_application()
                signal.signal(signal.SIGINT, on_sigint)

                # Get all messages directly from the application
                # class. This allows defining new messages without
                # touching the parser
                self.messages = {
                    f.__tag_name__: self.startMessage(functools.partial(f,self.app), f.__store__)
                    for f in GtkStreamApp.__dict__.values()
                    if hasattr(f, '__tag_name__')
                }
                self.logger.debug("Messages: %s", self.messages)

                self.transition_enter = self.transE_message
                self.transition_leave = self.transL_tag('application', self.transE_final, self.transL_final)
            case _:
                raise Exception("Error: expected 'application' tag")

    def startMessage(self, f, child = None):
        if child != None:
            def ret(name,attrs):
                getC, setC, setChars = child()
                old_chars = self.transition_chars
                def leave():
                    if setChars != None:
                        self.transition_chars = old_chars
                    f(getC(),**attrs)
                if setChars != None:
                    self.transition_chars = setChars
                self.transition_enter = self.transE_addChild(setC)
                self.transition_leave = self.transL_tag(name, self.transE_message, self.transition_leave, leave)
        else:
            def ret(name, attrs):
                def leave():
                    f(**attrs)
                self.transition_enter = self.transE_final
                self.transition_leave = self.transL_tag(name, self.transE_message, self.transition_leave, leave)
        return ret

    def transE_message(self, name, attrs):
        start = self.messages.get(name)
        if start != None:
            start(name,attrs)
        else:
            raise Exception(f"Error: unknown message '{name}'")

    def transE_addChild(self, addChild):
        def ret(name, attrs):
            leave_parent = self.transition_leave
            doc_class = WIDGET_DOCUMENTS.get(name)
            if doc_class != None:
                doc = doc_class(self.app, **attrs)
                addChild(doc)
                self.transition_enter = self.transE_addChild(lambda child: doc.add_child(child))
                self.transition_leave = self.transL_tag(name, self.transE_addChild(addChild), leave_parent)
            else:
                raise Exception(f"Error: Unknown widget type '{name}'")
        return ret

    def characters(self, s):
        self.transition_chars(s)
    def startElement(self, name, attrs):
        self.transition_enter(name, attrs)
    def endElement(self, name):
        self.transition_leave(name)
