#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.4150: * @file polygon.py
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
#@+node:1.20130426141258.4151: ** <<declarations>> (polygon)
import math

from Interface.Preview.base         import *
from Kernel.GeoUtil.geolib          import Vector
from Kernel.GeoEntity.point         import Point
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4152: ** class QtPolygonItem
class QtPolygonItem(PreviewBase):
    #@+others
    #@+node:1.20130426141258.4153: *3* __init__
    def __init__(self, command):
        super(QtPolygonItem, self).__init__(command)
        self.command=command
        # get the geometry
    #@+node:1.20130426141258.4154: *3* polygonPoint
    @property
    def polygonPoint(self):
        """
            get the poligon points
        """
        if self.side<=0:
            self.side=6
        deltaAngle=(math.pi*2)/self.side
        cPoint=Point(self.center.x(), self.center.y())
        vPoint=Point(self.vertex.x(), self.vertex.y())
        vertexVector=Vector(cPoint, vPoint)
        radius=vertexVector.norm
        angle=vertexVector.absAng
        pol=QtGui.QPolygonF()
        pFirst=None
        for i in range(0, int(self.side)):
            angle=deltaAngle+angle
            xsP=cPoint.x+radius*math.cos(angle)*-1.0
            ysP=cPoint.y+radius*math.sin(angle)*-1.0
            p=QtCore.QPointF(xsP,ysP)
            pol.append(p)
            if not pFirst:
                pFirst=p
        if pFirst:        
            pol.append(pFirst)
        return pol
    #@+node:1.20130426141258.4155: *3* drawGeometry
    def drawGeometry(self, painter,option,widget):
        """
            overloading of the paint method
        """
        if self.center and self.vertex:
            painter.drawPolyline(self.polygonPoint)
    #@+node:1.20130426141258.4156: *3* drawShape
    def drawShape(self, painterPath):    
        """
            overloading of the shape method 
        """
        if self.center and self.vertex:
            painter.drawPolyline(self.polygonPoint)
    #@+node:1.20130426141258.4157: *3* boundingRect
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        if self.center and self.vertex:
            return self.polygonPoint.boundingRect() 
        return QtCore.QRectF(0,0 ,0.1,0.1)
    #@+node:1.20130426141258.4158: *3* center
    @property
    def center(self):
        return self.value[0]
    #@+node:1.20130426141258.4159: *3* center
    @center.setter
    def center(self, value):
        self.value[0]=value
        self.update(self.boundingRect())
    #@+node:1.20130426141258.4160: *3* vertex
    @property
    def vertex(self):    
        return self.value[1]
    #@+node:1.20130426141258.4161: *3* vertex
    @vertex.setter
    def vertex(self, value):
        self.value[1]=value
        self.update(self.boundingRect())
    #@+node:1.20130426141258.4162: *3* side
    @property
    def side(self):
        return self.value[2]
    #@-others
#@-others
#@-leo
