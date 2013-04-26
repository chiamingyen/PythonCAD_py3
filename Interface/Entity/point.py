#@+leo-ver=5-thin
#@+node:1.20130426141258.4049: * @file point.py
#
# Copyright (c) ,2010 Matteo Boscolo
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
# qt pythoncad Point class
#



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.4050: ** <<declarations>> (point)
from Interface.Entity.base import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4051: ** class Point
class Point(BaseEntity):
    """
        this class define the arcQT object
    """
    #@+others
    #@+node:1.20130426141258.4052: *3* __init__
    def __init__(self, entity):
        super(Point, self).__init__(entity)
        self.xc,self.yc= self.geoItem.getCoords()
        self.yc=(-1.0*self.yc)
        return
    #@+node:1.20130426141258.4053: *3* boundingRect
    def boundingRect(self):
        return QtCore.QRectF(self.xc-self.shapeSize/2,self.yc-self.shapeSize/2 ,self.shapeSize ,self.shapeSize)
    #@+node:1.20130426141258.4054: *3* drawShape
    def drawShape(self, painterPath):
        """
            overloading of the shape method
        """
        painterPath.addRect(self.boundingRect())
    #@+node:1.20130426141258.4055: *3* drawGeometry
    def drawGeometry(self, painter, option, widget):
        """
            overloading of the paint method
        """
        #Create Arc/Circle
        p=QtCore.QPoint(self.xc, self.yc)
        painter.drawRect(self.boundingRect())
        painter.drawPoint(p)
    #@-others
#@-others
#@-leo
