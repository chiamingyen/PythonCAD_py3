#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.4107: * @file arc.py
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
#@+node:1.20130426141258.4108: ** <<declarations>> (arc)
import math
from PyQt4 import QtCore, QtGui
from Interface.Preview.base         import PreviewBase
from Interface.Entity.arc           import Arc
from Kernel.entity                  import Point
from Kernel.exception               import *
from Kernel.GeoEntity.point         import Point as GeoPoint
from Kernel.GeoUtil.geolib  import Vector
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4109: ** class PreviewArc
#TODO+: find a good way to retrive the geometry staff from a item in Interface.Entity.arc ..
#extend it for all the preview entity

class PreviewArc(PreviewBase):
    #@+others
    #@+node:1.20130426141258.4110: *3* __init__
    def __init__(self,command):
        super(PreviewArc, self).__init__(command)
    #@+node:1.20130426141258.4111: *3* canDraw
    @property
    def canDraw(self):
        if self.value[0]!=None:
            self.xc         =   self.value[0].x()
            self.yc         =   self.value[0].y()
            self.h          =   self.value[1]*2
          
            self.xc=self.xc-(self.h/2.0)
            self.yc=self.yc-(self.h/2.0)
            
            self.startAngle =  (self.value[2]*180/math.pi)*16
            self.spanAngle  =  (self.value[3]*180/math.pi)*16 
            return True       
        return False
    #@+node:1.20130426141258.4112: *3* drawGeometry
    def drawGeometry(self, painter,option,widget):
        """
            Overloading of the paint method
        """
        if self.canDraw:
            Arc.__dict__['drawGeometry'](self, painter,option,widget)
    #@+node:1.20130426141258.4113: *3* drawShape
    def drawShape(self, painterPath):
        """
            overloading of the shape method
        """
        if self.canDraw:
            Arc.__dict__['drawShape'](self, painterPath)
    #@+node:1.20130426141258.4114: *3* updatePreview
    def updatePreview(self,  position, distance, kernelCommand):
        """
            update the data at the preview item
        """
        self.prepareGeometryChange() #qtCommand for update the scene
        for i in range(0, len(kernelCommand.value)):
            self.value[i]=self.revertToQTObject(kernelCommand.value[i])
        # Assing Command Values
        index=kernelCommand.valueIndex
        try:
            raise kernelCommand.exception[index](None)
        except(ExcPoint):
            self.value[index]=self.revertToQTObject(position)
        except(ExcLenght, ExcInt):
            if not distance or distance !=None:
                self.value[index]=distance
        except(ExcAngle):
            p1 = kernelCommand.value[0]
            p2 = GeoPoint(position.x, position.y)
            ang=Vector(p1, p2).absAng
            if index==3:
                ang=ang-self.value[2]
            self.value[index]=ang
        except:
            print("updatePreview: Exception not managed")
            return
    #@-others
#@-others
#@-leo
