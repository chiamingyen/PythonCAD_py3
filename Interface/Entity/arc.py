#@+leo-ver=5-thin
#@+node:1.20130426141258.3991: * @file arc.py
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
# qt arc class
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3992: ** <<declarations>> (arc)
from PyQt4 import QtCore, QtGui
from Interface.Entity.base import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3993: ** class Arc
class Arc(BaseEntity):
    """
        this class define the arcQT object 
    """
    #@+others
    #@+node:1.20130426141258.3994: *3* __init__
    def __init__(self, entity):
        super(Arc, self).__init__(entity)
        geoEnt=self.geoItem  # get the geometry from kernel
        self.startPoint, p2=geoEnt.getEndpoints()     
        self.xc, self.yc=geoEnt.center.getCoords()
        startAngle=geoEnt.startAngle
        self.sa=startAngle
        spanAngle=geoEnt.endAngle
        self.yc=(-1.0*self.yc)- geoEnt.radius
        self.xc=self.xc-geoEnt.radius
        self.h=geoEnt.radius*2
        # By default, the span angle is 5760 (360 * 16, a full circle).
        # From pythoncad the angle are in radiant ..
        self.startAngle=(startAngle*180/math.pi)*16
        self.spanAngle=(spanAngle*180/math.pi)*16-self.startAngle
        return
    #@+node:1.20130426141258.3995: *3* drawShape
    def drawShape(self, painterPath):    
        """
            extending of the shape method 
        """
        qRect=QtCore.QRectF(self.xc,
                             self.yc,
                             self.h,
                             self.h)
        #x, y=self.startPoint.getCoords()
        painterPath.moveTo(self.xc, self.yc*-1.0)
        painterPath.arcTo(qRect,self.startAngle,self.spanAngle) 
        return
    #@+node:1.20130426141258.3996: *3* drawGeometry
    def drawGeometry(self, painter, option, widget):
        """
            extending of the paint method
        """
        #Create Arc/Circle
        qRect=QtCore.QRectF(self.xc,
                             self.yc,
                             self.h,
                             self.h)
        painter.drawArc(qRect,self.startAngle,  self.spanAngle)
    #@-others
#@-others
#@-leo
