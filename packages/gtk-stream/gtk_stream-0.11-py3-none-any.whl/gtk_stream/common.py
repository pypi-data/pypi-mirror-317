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
from enum import Enum

def _data_str_default(*args):
    return ''
def _data_str_by(get_data):
    def ret(*args):
        return ":"+get_data(*args)
    return ret

def printEvent(logger, event, id, retval = None, get_data = None):
    data_str = _data_str_default if get_data == None else _data_str_by(get_data)
    def ret(*args):
        try:
            print("{}:{}{}".format(id,event,data_str(*args)), file=sys.stdout)
            sys.stdout.flush()
        except Exception as e:
            logger.error("Exception when writing an event: %s", e)
        return retval
    return ret

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

class Logger:
    def __init__(self, level = LogLevel.WARN, stderr = sys.stderr):
        self.stderr = stderr
        self.level = level
        self.debug = self._initLogger(LogLevel.DEBUG)
        self.info  = self._initLogger(LogLevel.INFO)
        self.warn  = self._initLogger(LogLevel.WARN)
        self.error = self._initLogger(LogLevel.ERROR)
    def flush(self):
        self.stderr.flush()
        
    def _initLogger(self, level):
        if self.level.value <= level.value:
            def ret(fmt, *args):
                print((f"[{level.name}]: {fmt}") % args, file=self.stderr)
            return ret
        else:
            def ret(*args):
                pass
            return ret
