#@+leo-ver=5-thin
#@+node:1.20130426141258.3100: * @file chamfer.py
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
# code for base for Chamfer
#



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3101: ** <<declarations>> (chamfer)
from Kernel.GeoComposedEntity.objoint import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3102: ** class Chamfer
class Chamfer(ObjectJoint):
    """
        A Chamfer class 
    """
    #@+others
    #@+node:1.20130426141258.3103: *3* __init__
    def __init__(self, kw):
        """
            obj1, obj2, distance1, distance2, pointClick1=None, pointClick2=None
            "OBJECTJOINT_0" obj1        :(Segment ,ACLine)
            "OBJECTJOINT_1" obj2        :(Segment ,ACLine)
            "OBJECTJOINT_2" pointClick1 :Clicked point from the u.i near the obj1
            "OBJECTJOINT_3" pointClick2 :Clicked point from the u.i near the obj2
            "OBJECTJOINT_4" chamfer trim Mode :Trim Mode (FIRST,SECOND,BOTH,NO_TRIM)
            "OBJECTJOINT_5" distance1   :Real distance from intersection point to chamfer
            "OBJECTJOINT_6" distance2   :Real distance from intersection point to chamfer
        """
        argDes={"OBJECTJOINT_5":(float, int), 
                "OBJECTJOINT_6":(float, int)}
        ObjectJoint.__init__(self, kw, argDes)
        
        for dis in (self.distance1, self.distance2):
            if dis<0.0:
                raise StructuralError("Distance parameter must be greater then 0")
        self.segment=self._UpdateChamferSegment()
    #@+node:1.20130426141258.3104: *3* setConstructionElements
    def setConstructionElements(self, kw):    
        """
            set the construction elements
        """
        for k in kw:
            self[k]=kw[k]
    #@+node:1.20130426141258.3105: *3* _UpdateChamferSegment
    def _UpdateChamferSegment(self):           
        """
            Recompute the Chamfer segment
        """
        obj1, pc1=self._updateSegment(self.obj1,self.distance1, self.pointClick1 )
        obj2, pc2=self._updateSegment(self.obj2,self.distance2, self.pointClick2 )
        if self.trimModeKey[self.trimMode]!=self.trimModeKey["NO_TRIM"]:
            if self.trimModeKey[self.trimMode]==self.trimModeKey["FIRST"] or self.trimModeKey[self.trimMode]==self.trimModeKey["BOTH"]:
                self.obj1=obj1
            if self.trimModeKey[self.trimMode]==self.trimModeKey["SECOND"] or self.trimModeKey[self.trimMode]==self.trimModeKey["BOTH"]:
                self.obj2=obj2
        arg={"SEGMENT_0":pc1, "SEGMENT_1":pc2}
        seg=Segment(arg)
        return seg
    #@+node:1.20130426141258.3106: *3* _updateSegment
    def _updateSegment(self, obj,distance,  clickPoint=None):
        """
            recalculate the segment for the chamfer
            and give the point for the chamfer
        """
        ip=self._intersectionPoints[0]
        if isinstance(obj, Segment):
            p1, p2=obj.getEndpoints()
            if p1==ip:
                mvPoint=p1
                stPoint=p2
            elif p2==ip:
                mvPoint=p2
                stPoint=p1
            elif clickPoint:
                dist1=clickPoint.dist(p1)
                dist2=clickPoint.dist(p2)
                if dist1<dist2:
                    mvPoint=p1
                    stPoint=p2  
                else:
                    mvPoint=p2
                    stPoint=p1           
            else:
                dist1=ip.dist(p1)
                dist2=ip.dist(p2)
                if dist1<dist2:
                    mvPoint=p1
                    stPoint=p2  
                else:
                    mvPoint=p2
                    stPoint=p1   
                    
            v=Vector(mvPoint,stPoint).mag()
            v.mult(distance)
            ePoint=ip+v.point
            arg={"SEGMENT_0":ePoint, "SEGMENT_1":stPoint}
            return Segment(arg), ePoint
    #@+node:1.20130426141258.3107: *3* getConstructionElements
    def getConstructionElements(self):
        """
            retutn the construction element of the object
        """
        outElement=(self._obj1 , 
                    self._obj2 ,
                    self.distance1, 
                    self.distance2, 
                    self.pointClick1, 
                    self.pointClick2
                    )
        return outElement
    #@+node:1.20130426141258.3108: *3* getLength
    def getLength(self):
        """
            Return the Chamfer length.
        """
        if self.__segment:
            return self.__segment.length()
        else:
            return 0.0
    #@+node:1.20130426141258.3109: *3* setDistance1
    def setDistance1(self, distance):
        """
            change the value of the distance1
        """
        if distance<=TOL:
            raise StructuralError("Distance could be greater then 0")
        self["OBJECTJOINT_5"]=distance
        self._UpdateChamferSegment()
    #@+node:1.20130426141258.3110: *3* getDistance1
    def getDistance1(self):
        """
            return the distance from intersection point to chanfer start
        """
        return self["OBJECTJOINT_5"]
    #@+node:1.20130426141258.3111: *3* setDistance2
    def setDistance2(self, distance):
        """
            change the value of the distance1
        """
        if distance<=TOL:
            raise StructuralError("Distance could be greater then 0")
        self["OBJECTJOINT_6"]=distance
        self._UpdateChamferSegment()
    #@+node:1.20130426141258.3112: *3* getDistance2
    def getDistance2(self):
        """
            return the distance from intersection point to chanfer start
        """
        return self["OBJECTJOINT_6"]
    #@+node:1.20130426141258.3113: *3* clone
    distance1=property(getDistance1, setDistance1, None, "set the first distance") 
    distance2=property(getDistance2, setDistance2, None, "set the second distance") 

    def clone(self):
        """
            Clone the Chamfer .. 
            I do not why somone whant to clone a chamfer ..
            But Tis is the functionality .. :-)
        """
        newChamfer=Chamfer(self._obj1 , 
                    self._obj2 ,
                    self.distance1, 
                    self.distance2, 
                    self.pointClick1, 
                    self.pointClick2)
        return newChamfer
    #@+node:1.20130426141258.3114: *3* getReletedComponent
    def getReletedComponent(self):
        """
            return the element to be written in the db and used for renderin
        """
        return self.obj1 , self.obj2 ,self.segment
    #@-others
#@-others
#@-leo
