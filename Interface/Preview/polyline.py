#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.4163: * @file polyline.py
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
#@+node:1.20130426141258.4164: ** <<declarations>> (polyline)
import math

from Interface.Preview.base         import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4165: ** class QtPolylineItem
class QtPolylineItem(PreviewBase):
    #@+others
    #@+node:1.20130426141258.4166: *3* __init__
    def __init__(self, command):
        super(QtPolylineItem, self).__init__(command)
    #@+node:1.20130426141258.4167: *3* drawShape
    def drawShape(self, painterPath):    
        """
            overloading of the shape method 
        """
        first=True
        for p in self.value:
            if p and first:
                painterPath.moveTo(p)
                first=false
            elif p:
                painterPath.lineTo(p)    
    #@+node:1.20130426141258.4168: *3* boundingRect
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        X=[p.x() for p in self.value if p]
        Y=[p.y() for p in self.value if p]
        if X and Y:
            xmax=max(X)
            ymax=max(Y)
            xmin=min(X)
            ymin=min(Y)
            h=abs(xmin-xmax)
            w=abs(ymin-ymax)
            return QtCore.QRectF(xmin,ymin,h ,w)
        return QtCore.QRectF(0,0 ,0.1,0.1)
    #@+node:1.20130426141258.4169: *3* drawGeometry
    def drawGeometry(self, painter, option, widget):
        """
            overloading of the paint method
        """
        #Create polyline Object
        pol=QtGui.QPolygonF()
        points=[p for p in self.value if p]
        #points.reverse()
        for p in points:
            pol.append(p)
        if len(points)>1:
            painter.drawPolyline(pol)
        
        #painter.drawRect(self.boundingRect())
    #@-others
#@-others
#@-leo
