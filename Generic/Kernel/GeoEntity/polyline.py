#@+leo-ver=5-thin
#@+node:1.20130426141258.3361: * @file polyline.py
#
# Copyright (c) 2003, 2004, 2005, 2006 Art Haas
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
# classes for polyline objects
#





#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3362: ** <<declarations>> (polyline)
import math

from Kernel.GeoUtil.tolerance              import *
from Kernel.GeoEntity.point                import Point
from Kernel.GeoEntity.segment              import Segment
from Kernel.GeoEntity.cline                import CLine
from Kernel.GeoEntity.geometricalentity    import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3363: ** class Polyline
class Polyline(GeometricalEntity):
    """
        A class representing a polyline. A polyline is essentially
        a number of segments that connect end to end.
    """
    #@+others
    #@+node:1.20130426141258.3364: *3* __init__
    def __init__(self,kw):
        """
            Initialize a Polyline object.
            kw['POLYLINE_0'] must be a point
            kw['POLYLINE_..'] must be a point
            kw['POLYLINE_..n'] must be a point
        """
        if len(kw)<2:
            raise ValueError("Invalid number of imput value ")
        argDescription=dict([(key,Point) for key in kw])
        GeometricalEntity.__init__(self,kw, argDescription)
    #@+node:1.20130426141258.3365: *3* __str__
    #def __len__(self):
    #    return len(self.points)

    def __str__(self):
        return "Polyline"
    #@+node:1.20130426141258.3366: *3* info
    @property
    def info(self):
        return "Polyline"
    #@+node:1.20130426141258.3367: *3* __eq__
    def __eq__(self, obj):
        """
            Compare two Polyline objects for equality.
        """
        if not isinstance(obj, Polyline):
            return False
        if obj is self:
            return True
        _val = False
        _ppts = obj.points
        _pcount = len(_ppts)
        _spts = self.points
        _scount = len(_spts)
        if _pcount == _scount:
            _val = True
            for _i in range(_scount):
                if _ppts[_i] != _spts[_i]:
                    _val = False
                    break
            if not _val: # check reversed point list of second polyline
                _val = True
                _ppts.reverse()
                for _i in range(_scount):
                    if _ppts[_i] != _spts[_i]:
                        _val = False
                        break
        return _val
    #@+node:1.20130426141258.3368: *3* __ne__
    def __ne__(self, obj):
        """
            Compare two Polyline objects for inequality.
        """
        if not isinstance(obj, Polyline):
            return True
        if obj is self:
            return False
        _val = True
        _ppts = obj.getPoints()
        _pcount = len(_ppts)
        _spts = self.points
        _scount = len(_spts)
        if _pcount == _scount:
            _val = False
            for _i in range(_scount):
                if _ppts[_i] != _spts[_i]:
                    _val = True
                    break
            if _val: # check reversed point list of second polyline
                _val = False
                _ppts.reverse()
                for _i in range(_scount):
                    if _ppts[_i] != _spts[_i]:
                        _val = True
                        break
        return _val
    #@+node:1.20130426141258.3369: *3* getPoints
    def getPoints(self):
        """
            Get the points of the Polyline.
            This function returns a list containing all the Point
            objects that define the Polyline.
        """
        return self.getConstructionElements()
    #@+node:1.20130426141258.3370: *3* addPoint
    def addPoint(self, name, point):
        """
            Add a Point to the Polyline.
            The argument 'i' must be an integer, and argument 'p' must be a
            Point. The Point is added into the list of points comprising
            the Polyline as the i'th point.
        """
        if not isinstance(point, Point):
            raise TypeError("Invalid Point for Polyline point: " + repr(type(point)))
        self[name]=point
    #@+node:1.20130426141258.3371: *3* delPoint
    def delPoint(self, name):
        """
            Remove a Point from the Polyline.
            The argument i represents the index of the point to remove from
            the list of points defining the Polyline. The point will be
            removed only if the polyline will still have at least two Points.
        """

        if len(self) > 2:
            del self[name]
    #@+node:1.20130426141258.3372: *3* getBounds
    def getBounds(self):
        """
            Return the bounding rectangle around a Polyline.
            This method returns a tuple of four values:
            (xmin, ymin, xmax, ymax)
        """
        _pts = self.points
        _pxmin = None
        _pymin = None
        _pxmax = None
        _pymax = None
        for _pt in _pts:
            _px, _py = _pt.getCoords()
            if _pxmin is None or _px < _pxmin:
                _pxmin = _px
            if _pymin is None or _py < _pymin:
                _pymin = _py
            if _pxmax is None or _px > _pxmax:
                _pxmax = _px
            if _pymax is None or _py > _pymax:
                _pymax = _py
        return _pxmin, _pymin, _pxmax, _pymax
    #@+node:1.20130426141258.3373: *3* points
    def points(self):
        """
            return a list of point
        """
        exit=[]
        kk=list(self.keys())
        kk.sort()
        for k in kk:
            exit.append(self[k])
        return exit
    #@+node:1.20130426141258.3374: *3* clone
    def clone(self):
        """
            Create an identical copy of a Polyline.
        """
        _cpts = {}
        i=0
        for _pt in self.points:
            name="POLYLINE_%s"%str(i)
            _cpts[name]=_pt.clone()
            i+=1
        return Polyline(_cpts)
    #@+node:1.20130426141258.3375: *3* getSympySegments
    def getSympySegments(self):
        """
            return an array of sympy Segment
        """
        out=[]

        for s in self.getSegments():
            out.append(s.getSympy())
        return out
    #@+node:1.20130426141258.3376: *3* getSegments
    def getSegments(self):
        """
            return an array of segments that identifie the polyline
            used for intersection porpouse
        """
        tempPoint=None
        exitArray=[]
        for p in self.points():
            if tempPoint:
                constr={"SEGMENT_0":tempPoint, "SEGMENT_1":p}
                exitArray.append(Segment(constr))
            tempPoint=p
        else:
            return exitArray
        return []
    #@+node:1.20130426141258.3377: *3* mirror
    def mirror(self, mirrorRef):
        """
            perform the mirror
        """
        for k in self:
            self[k].mirror(mirrorRef)
    #@-others
#@-others
#@-leo
