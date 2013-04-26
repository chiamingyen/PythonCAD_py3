#@+leo-ver=5-thin
#@+node:1.20130426141258.3273: * @file geometricalentity.py
#
# Copyright (c) 2010 - 2013 Matteo Boscolo
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
# This is the base class for all the geometrical entitys
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3274: ** <<declarations>> (geometricalentity)
import math

import sympy            as mainSympy
import sympy.geometry   as geoSympy
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3275: ** class GeometricalEntity
class GeometricalEntity(dict):
    """
        This class provide the basic interface for all the geometrical entitys
    """
    #@+others
    #@+node:1.20130426141258.3276: *3* __init__
    def __init__(self, kw, argNameType):
        """
            argv name must be created before init the base class
        """
        if kw is None and argNameType is None:
            return
        if len(kw)!=len(argNameType):
            raise TypeError("Wrong number of items ")
        for k in kw:
            if k in argNameType:
                if isinstance(kw[k],argNameType[k]):
                    self[k]=kw[k]
                else:
                    raise TypeError("Wrong Type for argument %s"%str(k))
            else:
                raise TypeError("Wrong argument %s "%str(k))
        self.arguments=argNameType
        self._properties={}
    #@+node:1.20130426141258.3277: *3* updateSnapPoint
    def updateSnapPoint(self, force=None, fromPoint=None, fromEnt=None):
        pass
    #@+node:1.20130426141258.3278: *3* getUpdatedSnapPoints
    def getUpdatedSnapPoints(self, force, fromPoint=None,  fromEnt=None):
        """
            update the snappoint with force argument and return an array of geopoint
        """
        self.updateSnapPoint(force, fromPoint, fromEnt)
        return self.snapPoints
    #@+node:1.20130426141258.3279: *3* snapPoints
    @property
    def snapPoints(self):
        """
            return the snap points
        """
        return self._snapPoints
    #@+node:1.20130426141258.3280: *3* snapPoints
    @snapPoints.setter
    def snapPoints(self, value):
        self._snapPoints=value
    #@+node:1.20130426141258.3281: *3* getArgumentsName
    def getArgumentsName(self):
        """
            get the construction arguments Name
        """
        return self.arguments
    #@+node:1.20130426141258.3282: *3* getConstructionElements
    def getConstructionElements(self):
        """
            Get the construction element of entity..
        """
        return self
    #@+node:1.20130426141258.3283: *3* setConstructionElements
    def setConstructionElements(self, kw):
        """
            set the construction elemtnts
        """
        self=kw
    #@+node:1.20130426141258.3284: *3* move
    def move(self, fromPoint, toPoint):
        """
            this method must be defined for moving operation
        """
        from Kernel.GeoUtil.geolib import Vector
        from Kernel.GeoEntity.point import Point
        v=Vector(fromPoint, toPoint)
        for key in self:
            if isinstance(self[key] , Point):
                self[key]+=v.point
        return v.point
    #@+node:1.20130426141258.3285: *3* rotate
    def rotate(self, rotationPoint, angle):
        """
            this method must be defined for rotation
        """
        from Kernel.GeoUtil.geolib import Vector
        from Kernel.GeoEntity.point import Point
        
        for key in self:
            if isinstance(self[key] , Point):
                v=Vector(rotationPoint,self[key] )
                v.rotate(angle)
                self[key]=rotationPoint+v.point
    #@+node:1.20130426141258.3286: *3* getSympy
    def getSympy(self):
        """
            get the sympy object
        """
        pass
    #@+node:1.20130426141258.3287: *3* setFromSympy
    def setFromSympy(self, sympyPoint):    
        """
            update the points cord from a sympyobject
        """
        pass   
    #@-others
#@+node:1.20130426141258.3288: ** class GeometricalEntityComposed
class GeometricalEntityComposed(dict):
    """
        this class provide the basic object for composed entity 
        like dimension labels ...
    """
    #@+others
    #@+node:1.20130426141258.3289: *3* __init__
    def __init__(self, kw, argNameType):
        if kw is None and argNameType is None:
            return
        if len(kw)!=len(argNameType):
            raise TypeError("Wrong number of items ")
        for k in kw:
            if k in argNameType:
                newTest=argNameType[k]
                if isinstance(argNameType[k], tuple):
                    if None in argNameType[k]:
                        if kw[k] == None:
                            self[k]=kw[k]
                            continue
                        else:
                            newTest=tuple([x for x in argNameType[k] if x!=None])
                if isinstance(kw[k],newTest):
                    self[k]=kw[k]
                else:
                    raise TypeError("Wrong Type for argument %s"%str(k))
            else:
                raise TypeError("Wrong argument %s "%str(k))
        self.arguments=argNameType
    #@+node:1.20130426141258.3290: *3* getArgumentsName
    def getArgumentsName(self):
        """
            get the construction arguments Name
        """
        return self.arguments
    #@+node:1.20130426141258.3291: *3* getConstructionElements
    def getConstructionElements(self):
        """
            Get the construction element of ..
            This must return a tuple of object better if there are point
        """
        pass
    #@+node:1.20130426141258.3292: *3* getReletedComponent
    def getReletedComponent(self):
        """
            Get The releted object to be updated
        """
        pass
    #@-others
#@-others
#@-leo
