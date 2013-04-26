#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.2757: * @file pycadevent.py
#@@first

#
# Copyright (c) 2010 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# This  module define a custom event class 
#




#@@language python
#@@tabwidth -4
#@+others
#@+node:1.20130426141258.2758: ** class PyCadEvent
class PyCadEvent(object):
    """
        this class fire the envent from the python kernel
    """
    #@+others
    #@+node:1.20130426141258.2759: *3* __init__
    def __init__(self):
        self.handlers = set()
    #@+node:1.20130426141258.2760: *3* handle
    def handle(self, handler):
        self.handlers.add(handler)
        return self
    #@+node:1.20130426141258.2761: *3* unhandle
    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("PythonCad Handler is not handling this event.")
        return self
    #@+node:1.20130426141258.2762: *3* fire
    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)
    #@+node:1.20130426141258.2763: *3* getHandlerCount
    def getHandlerCount(self):
        return len(self.handlers)
    #@-others
    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount
#@-others
#@-leo
