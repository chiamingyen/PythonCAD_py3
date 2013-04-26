#@+leo-ver=5-thin
#@+node:1.20130426141258.2727: * @file layer.py
#
# Copyright (c) 2002, 2003, 2004, 2005, 2006 Art Haas 2009 Matteo Boscolo
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
# classes that describe the layer 
#



#@@language python
#@@tabwidth -4
#@+others
#@+node:1.20130426141258.2728: ** class Layer
class Layer(object):
    """
        this class manage a single layer
    """
    #@+others
    #@+node:1.20130426141258.2729: *3* __init__
    def __init__(self, layerName=None, visible=True):
        """
            name            = name of the layer
        """
        self.__name=layerName
        self.__visible=visible
    #@+node:1.20130426141258.2730: *3* name
    @property
    def name(self):
        """
            Get/Set The layer name
        """
        return self.__name
    #@+node:1.20130426141258.2731: *3* name
    @name.setter
    def name(self, value):
        self.__name=value
    #@+node:1.20130426141258.2732: *3* Visible
    @property
    def Visible(self):
        """
            manage layer visibility 
        """
        return self.__visible
    #@+node:1.20130426141258.2733: *3* Visible
    @Visible.setter
    def Visible(self, value):
        self.__visible=value
    #@-others
#@-others
#@-leo
