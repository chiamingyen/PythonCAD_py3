#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.4127: * @file ellipse.py
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
# EllipsePreview object
#




#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.4128: ** <<declarations>> (ellipse)
import math

from Interface.Preview.base         import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4129: ** class QtEllipseItem
class QtEllipseItem(PreviewBase):
    #@+others
    #@+node:1.20130426141258.4130: *3* __init__
    def __init__(self, command):
        super(QtEllipseItem, self).__init__(command)
        # get the geometry
    #@+node:1.20130426141258.4131: *3* drawGeometry
    def drawGeometry(self, painter,option,widget):
        """
            overloading of the paint method
        """
        if self.center:
            xc=self.center.x()
            yc=self.center.y()
            painter.drawEllipse(xc-(self.major/2.0),yc-(self.minor/2.0),self.major ,self.minor)
    #@+node:1.20130426141258.4132: *3* drawShape
    def drawShape(self, painterPath):    
        """
            overloading of the shape method 
        """
        if self.center:
            xc=self.center.x()
            yc=self.center.y()
            painterPath.drawEllipse(xc-(self.major/2.0),yc-(self.minor/2.0),self.major ,self.minor)
    #@+node:1.20130426141258.4133: *3* boundingRect
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        if self.center:
            xc=self.center.x()
            yc=self.center.y()
            return QtCore.QRectF(xc-(self.major/2.0),yc- (self.minor/2.0) ,self.major ,self.minor )
        return QtCore.QRectF(0,0 ,0.1,0.1)
    #@+node:1.20130426141258.4134: *3* center
    @property
    def center(self):
        return self.value[0]
    #@+node:1.20130426141258.4135: *3* center
    @center.setter
    def center(self, value):
        self.value[0]=value
        self.update(self.boundingRect())
    #@+node:1.20130426141258.4136: *3* major
    @property
    def major(self):
        return self.value[1]
    #@+node:1.20130426141258.4137: *3* major
    @major.setter
    def major(self, value):
        self.value[1] =value
        self.update(self.boundingRect())
    #@+node:1.20130426141258.4138: *3* minor
    @property
    def minor(self):
        return self.value[2]
    #@+node:1.20130426141258.4139: *3* minor
    @minor.setter
    def minor(self, value):
        self.value[2]=value
        self.update(self.boundingRect())
    #@-others
#@-others
#@-leo
