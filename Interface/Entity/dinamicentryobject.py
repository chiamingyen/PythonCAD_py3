#@+leo-ver=5-thin
#@+node:1.20130426141258.4034: * @file dinamicentryobject.py
#
# Copyright (c) 2010 Matteo Boscolo, Gertwin Groen
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
# This module the graphics scene class
#
#



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.4035: ** <<declarations>> (dinamicentryobject)
import math

from PyQt4 import QtCore, QtGui
from Kernel.pycadevent          import PyCadEvent
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4036: ** class DinamicEntryLine
class DinamicEntryLine(QtGui.QLineEdit):
    #@+others
    #@+node:1.20130426141258.4037: *3* __init__
    def __init__(self):
        super(DinamicEntryLine, self).__init__()
        self.hide()
        self.h=20
        self.w=60
        self.onEnter=PyCadEvent()
    #@+node:1.20130426141258.4038: *3* setPos
    def setPos(self, x, y):
        self.setGeometry(x, y, self.w, self.h)
    #@+node:1.20130426141258.4039: *3* text
    @property
    def text(self):
        return super(DinamicEntryLine, self).text()
    #@+node:1.20130426141258.4040: *3* text
    @text.setter
    def text(self, value):
        super(DinamicEntryLine, self).settext(value)
    #@+node:1.20130426141258.4041: *3* show
    def show(self):
        self.setFocus(7)
        super(DinamicEntryLine, self).show()  
    #@+node:1.20130426141258.4042: *3* keyPressEvent
    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Return:
            self.onEnter()
            super(DinamicEntryLine, self).hide()  
        super(DinamicEntryLine, self).keyPressEvent(event)
    #@-others
#@-others
#@-leo
