#@+leo-ver=5-thin
#@+node:1.20130426141258.3132: * @file objoint.py
#
# Copyright (c) 2002, 2003, 2004, 2005, 2006 Art Haas
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
# code for base composed object
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3133: ** <<declarations>> (objoint)
from math import hypot, pi, sin, cos, tan, atan2

from Kernel.GeoEntity.geometricalentity    import *
from Kernel.GeoUtil.util                   import *
from Kernel.GeoUtil.intersection           import *
from Kernel.GeoEntity.segment              import Segment
#from Kernel.GeoEntity.acline               import ACLine
from Kernel.GeoEntity.arc                  import Arc
from Kernel.GeoEntity.ccircle              import CCircle
from Kernel.GeoUtil.geolib                 import Vector
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3134: ** class ObjectJoint
#ALLOW_CHAMFER_ENTITY=(Segment, ACLine)

class ObjectJoint(GeometricalEntityComposed):
    """
        A base class for chamfers and fillets
        A ObjectJoint object has the following methods:
    """
    #@+others
    #@+node:1.20130426141258.3135: *3* __init__
    def __init__(self, kw, argDes=None):
        from Kernel.initsetting import DRAWIN_ENTITY
        classNames=tuple(DRAWIN_ENTITY.keys())
        argDescription={"OBJECTJOINT_0":classNames, 
                        "OBJECTJOINT_1":classNames, 
                        "OBJECTJOINT_2":(Point,None), 
                        "OBJECTJOINT_3":(Point,None), 
                        "OBJECTJOINT_4":(str, str)
                        }
        if argDes:
            for k in argDes:
                argDescription[k]=argDes[k]
                
        self.trimModeKey={"FIRST":0, "SECOND":1, "BOTH":2, "NO_TRIM":3}
        GeometricalEntityComposed.__init__(self, kw, argDescription)
        self._externalIntersectio=False
        spoolIntersection=[Point(x, y) for x, y in find_intersections(self.obj1, self.obj2)]
        if len(spoolIntersection)<=0: #if not intesection is found extend it on cLine
            spoolIntersection=findSegmentExtendedIntersectionPoint(self.obj1, self.obj2)
            self._externalIntersectio=True
        self._intersectionPoints=spoolIntersection
    #@+node:1.20130426141258.3136: *3* angle
    @property
    def angle(self):
        """
            angle betwin the two entity
        """
        v1=self.getAngledVector(self.obj1, self.pointClick1)
        v2=self.getAngledVector(self.obj2, self.pointClick2)
        ang=v1.ang(v2)
        return ang
    #@+node:1.20130426141258.3137: *3* trimMode
    @property
    def trimMode(self):
        """
            trim mode for the entity
        """
        return self["OBJECTJOINT_4"]
    #@+node:1.20130426141258.3138: *3* trimMode
    @trimMode.setter
    def trimMode(self, value):
        if value in self.trimModeKey:
            self["OBJECTJOINT_4"]=value
        else:
            raise AttributeError("Bad trim mode use FIRST SECOND BOTH NO_TRIM") 
    #@+node:1.20130426141258.3139: *3* obj1
    @property
    def obj1(self):    
        """
            First object
        """
        return self["OBJECTJOINT_0"]
    #@+node:1.20130426141258.3140: *3* obj1
    @obj1.setter
    def obj1(self, value):
        self["OBJECTJOINT_0"]=value
    #@+node:1.20130426141258.3141: *3* obj2
    @property
    def obj2(self):    
        """
           second object
        """
        return self["OBJECTJOINT_1"]
    #@+node:1.20130426141258.3142: *3* obj2
    @obj2.setter
    def obj2(self, value):
        self["OBJECTJOINT_1"]=value
    #@+node:1.20130426141258.3143: *3* pointClick1
    @property    
    def pointClick1(self):
        """
            get the clicked point
        """
        return self["OBJECTJOINT_2"]
    #@+node:1.20130426141258.3144: *3* pointClick1
    @pointClick1.setter
    def pointClick1(self, value):
        self["OBJECTJOINT_2"]=value
    #@+node:1.20130426141258.3145: *3* pointClick2
    @property  
    def pointClick2(self):
        """
            get the clicked point
        """
        return self["OBJECTJOINT_3"]
    #@+node:1.20130426141258.3146: *3* pointClick2
    @pointClick2.setter
    def pointClick2(self, value):
        self["OBJECTJOINT_3"]=value
    #@+node:1.20130426141258.3147: *3* intersection
    @property    
    def intersection(self):
        """
            Return the intersection points of the ObjectJoint Entity Object.

            This method returns an array of intersection point 
            [] no intersection
        """
        return self._intersectionPoints
    #@+node:1.20130426141258.3148: *3* getConstructionElements
    def getConstructionElements(self):
        """
            Return the two Entity Object joined by the ObjectJoint.
            This method returns a tuple holding the two Entity Object joined
            by the ObjectJoint.
        """
        return self
    #@+node:1.20130426141258.3149: *3* getReletedComponent
    def getReletedComponent(self):
        """
            return the releted compont of the ObjectJoint
        """
        return self.getConstructionElements()
    #@+node:1.20130426141258.3150: *3* getAngledVector
    def getAngledVector(self, segment,  point):
        """
            calculate the vector use
        """
        pi=self.intersection[0]
        p1, p2=segment.getEndpoints()
        vs1=Vector(pi, p1)
        vs2=Vector(pi, p2)
        if abs(vs1.absAng-vs2.absAng)<0.00001:
            if pi.dist(p1)>pi.dist(p2):
                return Vector(pi, p1)
            else:
                return Vector(pi, p2)
        else:
            jp=segment.getProjection(point)
            vj=Vector(pi, jp)
            if abs(vj.absAng-vs1.absAng)<0.00001:
                return Vector(pi, p1)
            else:
                return Vector(pi, p2)  
    #@-others
#@-others
#@-leo
