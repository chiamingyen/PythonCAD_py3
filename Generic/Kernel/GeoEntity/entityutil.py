#@+leo-ver=5-thin
#@+node:1.20130426141258.3270: * @file entityutil.py
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
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# This module provide some utility  for the entity 
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3271: ** <<declarations>> (entityutil)
import math

import sympy            as mainSympy
import sympy.geometry   as geoSympy

from Kernel.GeoEntity.point        import Point
from Kernel.GeoEntity.segment      import Segment
from Kernel.GeoEntity.arc          import Arc
from Kernel.GeoEntity.ellipse      import Ellipse
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3272: ** getEntityEntity
#    "Ray",
#    "Line",
#    "Triangle",
#    "RegularPolygon",
#    "Polygon",
#    "Curve"
    
def getEntityEntity(sympyEntity):
    """
        convert sympy object into PyCAD object
    """
    if isinstance(sympyEntity, geoSympy.Circle):
        arg={"ARC_0":Point(0.0, 0.0), 
             "ARC_1":1, 
             "ARC_2":None, 
             "ARC_3":None
             }    
        arc=Arc(arg)
        arc.setFromSympy(sympyEntity)
        return arc
    elif isinstance(sympyEntity, geoSympy.Point):
        p=Point(0.0, 0.0)
        p.setFromSympy(sympyEntity)
        return p
    elif isinstance(sympyEntity, geoSympy.Segment):
        segArg={"SEGMENT_0":Point(0.0, 0.0), "SEGMENT_1":Point(1.0, 1.0)}
        seg=Segment(segArg)
        seg.setFromSympy(sympyEntity)
        return seg
    elif isinstance(sympyEntity, geoSympy.Ellipse):
        arg={"ELLIPSE_0":Point(0.0, 0.0), "ELLIPSE_1":1.0, "ELLIPSE_2":2.0}
        e=Ellipse(arg)
        e.setFromSympy(sympyEntity)
        return e
    else:
        raise "not supported entity"
#@-others
#@-leo
