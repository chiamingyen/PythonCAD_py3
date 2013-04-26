#@+leo-ver=5-thin
#@+node:1.20130426141258.3249: * @file ellipse.py
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
# class stuff for ellipses
#
# Ellipse info:
# http://mathworld.wolfram.com/Ellipse.html
# http://astronomy.swin.edu.au/~pbourke/geometry/ellipsecirc/
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3250: ** <<declarations>> (ellipse)
import math


from Kernel.GeoUtil.tolerance              import *
from Kernel.GeoUtil.util                   import *
from Kernel.GeoEntity.point                import Point
from Kernel.GeoEntity.segment              import Segment
from Kernel.GeoEntity.cline                import CLine
from Kernel.GeoEntity.geometricalentity    import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3251: ** class Ellipse
class Ellipse(GeometricalEntity):
    """
        A base class for Ellipses
        An ellipse has the following attributes:
        center: A _point object
        horizontalRadius_axis:
        verticalRadius_axis:
    """
    #@+others
    #@+node:1.20130426141258.3252: *3* __init__
    def __init__(self,kw):
        """
            Initialize a Arc/Circle.
            kw['ELLIPSE_0'] center must be a point 
            kw['ELLIPSE_1'] hradius ax
            kw['ELLIPSE_2'] vradius ax
        """
        argDescription={
                        "ELLIPSE_0":Point,
                        "ELLIPSE_1":(float, int), 
                        "ELLIPSE_2":(float, int)
                        }
        _horizontalRadius=kw['ELLIPSE_1']
        _verticalRadius=kw['ELLIPSE_2']
        #if _verticalRadius > _horizontalRadius:
        #    kw['ELLIPSE_2']=get_float(_horizontalRadius)
        #    kw['ELLIPSE_1']=get_float(_verticalRadius)
        GeometricalEntity.__init__(self,kw, argDescription)
    #@+node:1.20130426141258.3253: *3* info
    @property
    def info(self):
        return "Ellipse: Center: %s, horizontalRadius: %s, verticalRadius:%s "%(str(self.center), str(self.horizontalRadius), str(self.verticalRadius))        
    #@+node:1.20130426141258.3254: *3* __eq__
    def __eq__(self, obj):
        """
            Compare one ellipse to another for equality.
        """
        if not isinstance(obj, Ellipse):
            return False
        if obj is self:
            return True
        return (self.center == obj.getCenter() and
                abs(self.horizontalRadius - obj.gethorizontalRadiusAxis()) < 1e-10 and
                abs(self.verticalRadius - obj.getverticalRadiusAxis()) < 1e-10 
                )
    #@+node:1.20130426141258.3255: *3* __ne__
    def __ne__(self, obj):
        """
            Compare one ellipse to another for equality.
        """
        return not self==object
    #@+node:1.20130426141258.3256: *3* getCenter
    def getCenter(self):
        """
            Return the center _Point of the Ellipse.
        """
        return self['ELLIPSE_0']
    #@+node:1.20130426141258.3257: *3* setCenter
    def setCenter(self, point):
        """
            Set the center _Point of the Ellipse.
            The argument must be a _Point or a tuple containing
            two float values.
        """
        self['ELLIPSE_0'] = point
    #@+node:1.20130426141258.3258: *3* gethorizontalRadiusAxis
    center = property(getCenter, setCenter, None, "Ellipse center")

    def gethorizontalRadiusAxis(self):
        """
            Return the horizontalRadius axis value of the Ellipse.
            This method returns a float.
        """
        return self['ELLIPSE_1']
    #@+node:1.20130426141258.3259: *3* sethorizontalRadiusAxis
    def sethorizontalRadiusAxis(self, val):
        """
            Set the horizontalRadius axis of the Ellipse.
            Argument 'val' must be a float value greater than 0.
        """
        _val = get_float(val)
        if _val < 0.0:
            raise ValueError("Invalid horizontalRadius axis value: %g" % _val)
        if _val < self.verticalRadius:
            self.self['ELLIPSE_1']=self.verticalRadius
            self.verticalRadius=_val
        else:
            self['ELLIPSE_1']=_val
    #@+node:1.20130426141258.3260: *3* getverticalRadiusAxis
    horizontalRadius= property(gethorizontalRadiusAxis, sethorizontalRadiusAxis, None,
                          "Ellipse horizontalRadius axis")

    def getverticalRadiusAxis(self):
        """
            Return the verticalRadius axis value of the Ellipse.
            This method returns a float.
        """
        return self['ELLIPSE_2']
    #@+node:1.20130426141258.3261: *3* setverticalRadiusAxis
    def setverticalRadiusAxis(self, val):
        """
            Set the verticalRadius axis of the Ellipse.
            Argument 'val' must be a float value greater than 0.
        """
        _val = get_float(val)
        if _val < 0.0:
            raise ValueError("Invalid verticalRadius axis value: %g" % _val)
        if _val > self.horizontalRadius:
            self['ELLIPSE_2']=self.horizontalRadius
            self.horizontalRadius=_val
        else:
            self['ELLIPSE_2']=_val
    #@+node:1.20130426141258.3262: *3* eccentricity
    verticalRadius = property(getverticalRadiusAxis, setverticalRadiusAxis, None,
                          "Ellipse verticalRadius axis")


    def eccentricity(self):
        """
            Return the eccecntricity of the Ellipse.
            This method returns a float value.
        """
        _horizontalRadius = self.horizontalRadius
        _verticalRadius = self.verticalRadius
        if abs(_horizontalRadius - _verticalRadius) < 1e-10: # circular
            _e = 0.0
        else:
            _e = math.sqrt(1.0 - ((_verticalRadius * _verticalRadius)/(_horizontalRadius * _horizontalRadius)))
        return _e
    #@+node:1.20130426141258.3263: *3* area
    def area(self):
        """
            Return the area of the Ellipse.
            This method returns a float value.
        """
        return math.pi * self.horizontalRadius * self.verticalRadius
    #@+node:1.20130426141258.3264: *3* circumference
    def circumference(self):
        """
            Return the circumference of an ellipse.
            This method returns a float.
            The algorithm below is taken from
            http://astronomy.swin.edu.au/~pbourke/geometry/ellipsecirc/
            Ramanujan, Second Approximation
        """
        _a = self.horizontalRadius
        _b = self.verticalRadius
        _h = math.pow((_a - _b), 2)/math.pow((_a + _b), 2)
        _3h = 3.0 * _h
        return math.pi * (_a + _b) * (1.0 + _3h/(10.0 + math.sqrt(4.0 - _3h)))
    #@+node:1.20130426141258.3265: *3* clone
    #
    # measure r from focus
    #
    # x = c + r*cos(theta)
    # y = r*sin(theta)
    #
    # c = sqrt(a^2 - b^2)
    #
    # r = a*(1-e)/(1 + e*cos(theta))

    def clone(self):
        """
            Make a copy of an Ellipse.
            This method returns a new Ellipse object
        """
        return Ellipse(self.getConstructionElements())
    #@+node:1.20130426141258.3266: *3* getSympy
    def getSympy(self):
        """
            get the sympy object in this case a ellipse
        """
        _cp=self.center.getSympy()
        return geoSympy.Ellipse(_cp,mainSympy.Rational(str(self.horizontalRadius*.5)),mainSympy.Rational(str(self.verticalRadius*.5)))
    #@+node:1.20130426141258.3267: *3* setFromSympy
    def setFromSympy(self, sympyEllipse):    
        """
            update the points cord from a sympyobject only avaiable for circle
        """
        self.center.setFromSympy(sympyEllipse.center)
        self.horizontalRadius=float(sympyEllipse.hradius )
        self.verticalRadius=float(sympyEllipse.vradius )
    #@+node:1.20130426141258.3268: *3* __str__
    def __str__(self):
        msg="Ellipse: Center %s , horizontalRadius Axi=%s, Mino Axi=%s"%(
            str(self.center), str(self.horizontalRadius), str(self.verticalRadius))
        return msg
    #@+node:1.20130426141258.3269: *3* mirror
    def mirror(self, mirrorRef):
        """
            perform the mirror of the line
        """
        if not isinstance(mirrorRef, (CLine, Segment)):
            raise TypeError("mirrorObject must be Cline Segment or a tuple of points")
        #
        self.center.mirror(mirrorRef)
    #@-others
#@-others
#@-leo
