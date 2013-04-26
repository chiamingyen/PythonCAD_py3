#@+leo-ver=5-thin
#@+node:1.20130426141258.3408: * @file text.py
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
# basic text functionality
#



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3409: ** <<declarations>> (text)
from .geometricalentity      import GeometricalEntity


from Kernel.GeoUtil.util import *
from Kernel.GeoEntity.point import Point
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3410: ** class Text
#
# Text
#
class Text(GeometricalEntity):
    """
        A class representing text in a drawing.
        A Text instance has the following attributes:
    """
    #@+others
    #@+node:1.20130426141258.3411: *3* __init__
    def __init__(self,kw):
        """
            Initialize a Arc/Circle.
            kw['TEXT_0'] position point must be a point 
            kw['TEXT_1'] text must be a valid text
            kw['TEXT_2'] angle must be a valid radiant float value or None
            kw['TEXT_3'] position of the text refered to the position point must be a valid string value or None
        """
        argDescription={
                        "TEXT_0":Point,
                        "TEXT_1":(float, str, str), 
                        "TEXT_2":(float, int), 
                        "TEXT_3":(str, str)
                        }
        
        if kw['TEXT_2']==None:
            kw['TEXT_2'] = 0
        from Kernel.initsetting             import TEXT_POSITION
        if kw['TEXT_3']==None:
            kw['TEXT_3'] = 'sw'
        else:
            if not kw['TEXT_3'] in TEXT_POSITION:
                kw['TEXT_3'] = 'sw'
                #if kw['TEXT_3']=='':
                #    kw['TEXT_3'] = 'sw'
                #else:
                #    raise TypeError, "Argument for TEXT_3 not supported"

        GeometricalEntity.__init__(self,kw, argDescription)
    #@+node:1.20130426141258.3412: *3* __eq__
    def __eq__(self, objTest):
        if isistance(objTest,Text):
            if(self.text== objTest.text and
                self.angle ==objTest.angle and
                self.location==objTest.location and
                self.pointPosition==objTest.pointPosition):
                return True
            else:
                return False
        else:
            raise TypeError("obj must be of type Text")
    #@+node:1.20130426141258.3413: *3* info
    @property
    def info(self):
        return "Text: %s"%str(self.location) 
    #@+node:1.20130426141258.3414: *3* text
    @property            
    def text(self):
        """
            Get the current text within the Text.
        """
        return self['TEXT_1']
    #@+node:1.20130426141258.3415: *3* text
    @text.setter
    def text(self, text):
        """
            Set the text within the Text.
        """
        if not isinstance(text, str):
            raise TypeError("Invalid text data: " + str(text))
        self['TEXT_1'] = text
    #@+node:1.20130426141258.3416: *3* location
    @property
    def location(self):
        """
            Return the Text spatial position.
        """
        return self['TEXT_0']
    #@+node:1.20130426141258.3417: *3* location
    @location.setter
    def location(self, x, y):
        """
            Store the spatial position of the Text.
        """
        _x = get_float(x)
        _y = get_float(y)
        self['TEXT_0'] = Point(_x, _y)
    #@+node:1.20130426141258.3418: *3* angle
    @property
    def angle(self):
        """
            Return the angle at which the text is drawn.
        """
        return self['TEXT_2']
    #@+node:1.20130426141258.3419: *3* angle
    @angle.setter
    def angle(self, angle=None):
        """
            Set the angle at which the text block should be drawn.
        """
        self['TEXT_2']= get_float(angle)
    #@+node:1.20130426141258.3420: *3* pointPosition
    @property
    def pointPosition(self):
        """
            return the position of the textrefered to the point 
        """
        return self['TEXT_3']
    #@+node:1.20130426141258.3421: *3* pointPosition
    @pointPosition.setter
    def pointPosition(self, position):
        """
            set the position of the textrefered to the point 
        """
        from Kernel.initsetting             import TEXT_POSITION
        from Kernel.exception               import PythopnCadWarning
        if position in TEXT_POSITION:
            self['TEXT_3']=position
        raise TypeError("bad Point position")    
    #@+node:1.20130426141258.3422: *3* getLineCount
    def getLineCount(self):
        """
            Return the number of lines of text in the Text
        """
        #
        # ideally Python itself would provide a linecount() method
        # so the temporary list would not need to be created ...
        #
        return len(self.text.splitlines())
    #@+node:1.20130426141258.3423: *3* clone
    def clone(self):
        """
            Return an identical copy of a Text.
        """
        _x, _y = self.getLocation().getCoords()
        _text = self.getText()
        _tb = Text(_x, _y, _text)
        _tb.angle = self.getAngle()
        _tb.pointPosition=self.pointPosition
        return _tb
    #@+node:1.20130426141258.3424: *3* mirror
    def mirror(self, mirrorRef):
        """
            perform the mirror of the line
        """
        # TODO Look at the qt text implementation to understand better the text 
        # mirror 
        pass
        if not isinstance(mirrorRef, ( Segment)):
            raise TypeError("mirrorObject must be Cline Segment or a tuple of points")

        pl=self.getLocation()
        pl.mirror(mirrorRef)
    #@+node:1.20130426141258.3425: *3* rotate
    def rotate(self, rotationPoint, angle):
        """
            overloading of the rotate base method 
        """
        GeometricalEntity.rotate(self, rotationPoint, angle)
        self.angle=self.angle-angle
    #@-others
#@-others
#@-leo
