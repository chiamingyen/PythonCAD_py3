#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.4177: * @file segment.py
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
#@+node:1.20130426141258.4178: ** <<declarations>> (segment)
from Interface.Preview.base         import PreviewBase
from Interface.Entity.segment       import Segment 
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4179: ** class PreviewSegment
#

class PreviewSegment(PreviewBase):
    #@+others
    #@+node:1.20130426141258.4180: *3* __init__
    def __init__(self,command):
        super(PreviewSegment, self).__init__(command)
    #@+node:1.20130426141258.4181: *3* canDraw
    @property
    def canDraw(self):
        if self.value[0]!=None and self.value[1]!=None:
            self.x=self.value[0].x()
            self.y=self.value[0].y()
            self.x1=self.value[1].x()
            self.y1=self.value[1].y()
            return True
        return False
    #@+node:1.20130426141258.4182: *3* drawGeometry
    def drawGeometry(self, painter,option,widget):
        """
            Overloading of the paint method
        """
        if self.canDraw:
            Segment.__dict__['drawGeometry'](self,painter,option,widget)
    #@+node:1.20130426141258.4183: *3* drawShape
    def drawShape(self, painterPath):
        """
            overloading of the shape method
        """
        if self.canDraw:
            Segment.__dict__['drawShape'](self,painterPath)
    #@-others
#@-others
#@-leo
