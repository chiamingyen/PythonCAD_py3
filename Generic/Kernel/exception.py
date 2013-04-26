#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.2662: * @file exception.py
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
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# This  module Provide custom exception for the db module and kernel
#




#@@language python
#@@tabwidth -4
#@+others
#@+node:1.20130426141258.2663: ** class EntityMissing
class EntityMissing(Exception):
    """
        Wrong entity provided
    """
    #@+others
    #@+node:1.20130426141258.2664: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2665: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2666: ** class NoDefaultValue
class NoDefaultValue(Exception):
    """
        no default value provided by the command
    """
    #@+others
    #@+node:1.20130426141258.2667: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2668: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2669: ** class NotImplementedError
class NotImplementedError(Exception):
    """
        Thi means that the followeing method is not yet implemented
    """
    #@+others
    #@+node:1.20130426141258.2670: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2671: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2672: ** class DeprecatedError
class DeprecatedError(Exception):
    """
        This means that the followeing method is no longer supported
    """
    #@+others
    #@+node:1.20130426141258.2673: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2674: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2675: ** class StructuralError
class StructuralError(Exception):
    """
        Very bad error that menans that the kernel has made somthing very bad
    """
    #@+others
    #@+node:1.20130426141258.2676: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2677: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2678: ** class EmptyFile
class EmptyFile(Exception):
    """
        class for managin empty file
    """
    #@+others
    #@+node:1.20130426141258.2679: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2680: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2681: ** class StyleUndefinedAttribute
class StyleUndefinedAttribute(Exception):
    """
        Class for managing styleAttribute problems
    """
    #@+others
    #@+node:1.20130426141258.2682: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2683: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2684: ** class PythonCadWarning
class PythonCadWarning(Exception):
    """
        Class for raise a warning exception
    """
    #@+others
    #@+node:1.20130426141258.2685: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2686: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2687: ** class EmptyDbSelect
class EmptyDbSelect(Exception):
    """
        This exception is used for null return of
        db select
    """
    #@+others
    #@+node:1.20130426141258.2688: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2689: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2690: ** class EntityMissing
class EntityMissing(Exception):
    """
        This exception is used for null return of
        entity search
    """
    #@+others
    #@+node:1.20130426141258.2691: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2692: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2693: ** class UndoDbExc
class UndoDbExc(Exception):
    """
        This exception is used UndoDb class to manage is errors
    """
    #@+others
    #@+node:1.20130426141258.2694: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2695: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2696: ** class EntDb
class EntDb(Exception):
    """
        Generic error on entity db creatioin
    """
    #@+others
    #@+node:1.20130426141258.2697: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2698: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2699: ** class DxfReport
class DxfReport(Exception):
    """
        error to say that the report of dxf is ready to be visualized
    """
    #@+others
    #@+node:1.20130426141258.2700: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2701: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2702: ** class DxfUnsupportedFormat
class DxfUnsupportedFormat(Exception):
    """
        Unsupported format
    """
    #@+others
    #@+node:1.20130426141258.2703: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2704: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2705: ** class PyCadWrongCommand
#********************************
#       command exception
#********************************
class PyCadWrongCommand(Exception):
    """
        Wrong command for the PyCadApplication
    """
    #@+others
    #@+node:1.20130426141258.2706: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2707: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2708: ** class PyCadWrongImputData
class PyCadWrongImputData(Exception):
    """
        Wrong command for the PyCadApplication
    """
    #@+others
    #@+node:1.20130426141258.2709: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2710: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2711: ** class CommandException
#********************************
#       imput command exception
#********************************
class CommandException(Exception):
    #@+others
    #@+node:1.20130426141258.2712: *3* __init__
    def __init__(self, value):
        self.value = value
    #@+node:1.20130426141258.2713: *3* __str__
    def __str__(self):
        return repr(self.value)
    #@-others
#@+node:1.20130426141258.2714: ** class ExcPoint
class ExcPoint(CommandException):
    """
        when this exception is trown it means that the command need a point
    """
    pass
#@+node:1.20130426141258.2715: ** class ExcLenght
class ExcLenght(CommandException):
    """
        when this exception is thrown it means that the command need a lenght
    """
    pass
#@+node:1.20130426141258.2716: ** class ExcAngle
class ExcAngle(CommandException):
    """
        when this exception is thrown it means that the command need a deg angle
    """
    pass
#@+node:1.20130426141258.2717: ** class ExcText
class ExcText(CommandException):
    """
        when this exception is thrown it means that the command need text
    """
    pass
#@+node:1.20130426141258.2718: ** class ExcInt
class ExcInt(CommandException):
    """
        when this exception is thrown it means that the command need an Integer
    """
    pass
#@+node:1.20130426141258.2719: ** class ExcBool
class ExcBool(CommandException):
    """
        when this exception is thrown it means that the command need n Boolean
    """
    pass
#@+node:1.20130426141258.2720: ** class ExcEntity
class ExcEntity(CommandException):
    """
        when this exception is thrown it means that the command need n dbEnity
    """
    pass
#@+node:1.20130426141258.2721: ** class ExcMultiEntity
class ExcMultiEntity(CommandException):
    """
        when this exception is thrown it means that the command need an array of id
    """
    pass
#@+node:1.20130426141258.2722: ** class ExcEntityPoint
class ExcEntityPoint(CommandException):
    """
        when this exception is thrown it means that the command need an a string
        like id@x,y
    """
    pass
#@+node:1.20130426141258.2723: ** class ExcDicTuple
class ExcDicTuple(CommandException):
    """
        require a dictionary of tuple
    """
    pass
#@-others
#@-leo
