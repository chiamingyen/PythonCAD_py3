#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.2769: * @file settings.py
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
# This module provide all the basic operation for the pythoncad settings
#





#@@language python
#@@tabwidth -4
#@+others
#@+node:1.20130426141258.2770: ** class Settings
class Settings(object):
    """
        this class provide access at all the pythoncad settings
    """
    #@+others
    #@+node:1.20130426141258.2771: *3* __init__
    def __init__(self,name):
        """
            the name of the settings schema
        """
        self.__name=name
        self.__activeLayer="ROOT"
        self.__property={}
    #@+node:1.20130426141258.2772: *3* name
    @property
    def name(self):
        """
            get the settings Name
        """
        return self.__name
    #@+node:1.20130426141258.2773: *3* name
    @name.setter
    def name(self,name):
        """
            set the settings name
        """
        self.__name=name
    #@+node:1.20130426141258.2774: *3* layerName
    @property
    def layerName(self):
        """
            get the anctive layer of the settings
        """
        return self.__activeLayer
    #@+node:1.20130426141258.2775: *3* layerName
    @layerName.setter
    def layerName(self,lName):
        """
            set the active layer id
        """
        self.__activeLayer=lName
    #@+node:1.20130426141258.2776: *3* getVariable
    def getVariable(self, name):
        """
            Get The variable in the settings object
        """
        if self.__property and name in self.__property:
            return self.__property[name]
        return None
    #@+node:1.20130426141258.2777: *3* setVariable
    def setVariable(self, name, value):
        """
            Set The variable in the settings object
        """
        self.__property[name]=value
    #@-others
#@-others
#@-leo
