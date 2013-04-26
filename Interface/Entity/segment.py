#@+leo-ver=5-thin
#@+node:1.20130426141258.4063: * @file segment.py
# Copyright (c) 2009,2010 Matteo Boscolo
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
# classes for interface segment
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.4064: ** <<declarations>> (segment)
from Interface.Entity.base import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4065: ** class Segment
class Segment(BaseEntity):
    #@+others
    #@+node:1.20130426141258.4066: *3* __init__
    def __init__(self, entity):
        super(Segment, self).__init__(entity)
        p1, p2=self.geoItem.getEndpoints()
        self.x, self.y=p1.getCoords()
        self.x1, self.y1=p2.getCoords()
        self.y=self.y*-1.0
        self.y1=self.y1*-1.0
        return
    #@+node:1.20130426141258.4067: *3* drawShape
    def drawShape(self, painterPath):    
        """
            overloading of the shape method 
        """
        painterPath.moveTo(self.x, self.y)
        painterPath.lineTo(self.x1, self.y1)
    #@+node:1.20130426141258.4068: *3* drawGeometry
    def drawGeometry(self, painter, option, widget):
        #Create Segment
        p1=QtCore.QPointF(self.x, self.y)
        p2=QtCore.QPointF(self.x1, self.y1)
        painter.drawLine(p1,p2)
    #@-others
#@-others
#@-leo
