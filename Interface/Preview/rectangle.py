#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.4170: * @file rectangle.py
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
# You should have received a copy of the GNU General Public Licensesegmentcmd.py
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# SegmentPreview object
#




#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.4171: ** <<declarations>> (rectangle)
import math

from Interface.Preview.base         import *
from Kernel.GeoEntity.segment       import Segment as geoSegment
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4172: ** class QtRectangleItem
class QtRectangleItem(PreviewBase):
    #@+others
    #@+node:1.20130426141258.4173: *3* __init__
    def __init__(self,command):
        super(QtRectangleItem, self).__init__(command)
    #@+node:1.20130426141258.4174: *3* drawGeometry
    def drawGeometry(self, painter,option,widget):
        """
            Overloading of the paint method
        """
        if self.value[0]!=None and self.value[1]!=None:
            painter.drawRect(self.getRectangle())
    #@+node:1.20130426141258.4175: *3* boundingRect
    def boundingRect(self):
        """
            Overloading of the qt bounding rectangle
        """
        if self.value[0]!=None and self.value[1]!=None :
            return self.getRectangle()
        return QtCore.QRectF(0.0,0.0 ,0.1,0.1)
    #@+node:1.20130426141258.4176: *3* getRectangle
    def getRectangle(self):
        """
            Create the rectangle
        """
        x=min(self.value[0].x(), self.value[1].x())
        y=min(self.value[0].y(), self.value[1].y())
        d1=abs(self.value[0].x()-self.value[1].x())
        d2=abs(self.value[0].y()-self.value[1].y())
        return QtCore.QRectF(x,y ,d1,d2)
    #@-others
#@-others
#@-leo
