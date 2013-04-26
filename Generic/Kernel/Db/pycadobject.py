#@+leo-ver=5-thin
#@+node:1.20130426141258.2990: * @file pycadobject.py
#encoding: utf-8
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
# This module provide basic pythoncadObject
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.2991: ** <<declarations>> (pycadobject)
from Kernel.GeoEntity.style             import Style
from Kernel.exception                   import EntityMissing
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.2992: ** class PyCadObject
class PyCadObject(object):
    """
        This class provide basic information for all the pythoncad object 
    """
    #@+others
    #@+node:1.20130426141258.2993: *3* __init__
    def __init__(self,objId,style,eType,properties={}):
        from Kernel.initsetting import OBJECT_STATE
        self.OBJECT_STATE=OBJECT_STATE
        self.__entityId=objId
        self.__state="MODIFIE"
        self._index=0
        self.__visible=1
        self.__style=style
        self.__entType=eType
        self.__properties=properties
    #@+node:1.20130426141258.2994: *3* addPropertie
    def addPropertie(self,name,value):
        """
            add a properties to the object
        """
        self.__properties[name]=value
    #@+node:1.20130426141258.2995: *3* getPropertie
    def getPropertie(self,name):
        """
            get the properties with a given name
        """
        if name in self.__properties:
            return self.__properties[name]
        raise EntityMissing("No entity with name %s"%str(name))
    #@+node:1.20130426141258.2996: *3* resetProperty
    def resetProperty(self):
        """
            reset the property 
        """
        self.__properties={}
    #@+node:1.20130426141258.2997: *3* properties
    @property
    def properties(self):
        """
            get all the properties from the entity
        """
        return self.__properties
    #@+node:1.20130426141258.2998: *3* setVisible
    def setVisible(self, visible):
        """
            set the visible value
        """
        self.__visible=visible
    #@+node:1.20130426141258.2999: *3* getVisible
    def getVisible(self):
        """
            get the visible value
        """
        return self.__visible
    #@+node:1.20130426141258.3000: *3* getId
    visible=property(getVisible, setVisible, None,"Set/Get the entity visibiolity")

    def getId(self):
        """
            get the entity id
        """
        return self.__entityId
    #@+node:1.20130426141258.3001: *3* getState
    def getState(self):
        """
            get the active entity state
        """
        return self.__state
    #@+node:1.20130426141258.3002: *3* setState
    def setState(self, state):
        """
            set the active state
        """ 
        if state in self.OBJECT_STATE:
            self.__state=state
        else:
            print("Wrong argunent")
            raise 
    #@+node:1.20130426141258.3003: *3* getIndex
    state=property(getState, setState, None, "Get/Set the state of the entity")

    def getIndex(self):
        """
            get the index of the revision index of the current object
        """
        return self._index
    #@+node:1.20130426141258.3004: *3* getNewIndex
    def getNewIndex(self):
        """
            Get the new index of the current entity
        """
        if self._index:
            self._index+=self._index
            self.__state=self.OBJECT_STATE[0]
        else: 
            self._index=0
            self.__state=self.OBJECT_STATE[0]
    #@+node:1.20130426141258.3005: *3* setIndex
    def setIndex(self,index):
        """
            Set The index of the entity
        """
        if index:
            self._index=index
    #@+node:1.20130426141258.3006: *3* delete
    index=property(getIndex, setIndex, "Get The new index of the current entity")

    def delete(self):
        """
            mark the entity to delete
        """
        self.__state='DELETE'
    #@+node:1.20130426141258.3007: *3* relese
    def relese(self):
        """
            mark the entity as released
        """
        self.__state='RELEASED'
    #@+node:1.20130426141258.3008: *3* getStyle
    def getStyle(self):
        """
            get the object EntityStyle
        """
        return self.__style
    #@+node:1.20130426141258.3009: *3* setStyle
    def setStyle(self,style):
        """
            set/update the entitystyle
        """
        self.__style=style
    #@+node:1.20130426141258.3010: *3* getInnerStyle
    style=property(getStyle,setStyle,None,"Get/Set the entity style")

    def getInnerStyle(self):
        """
            return the inner style of type Style
        """
        if self.style!=None:
            styleEnt=self.style.getConstructionElements() 
            return styleEnt[list(styleEnt.keys())[0]]
        else:
            return None
    #@+node:1.20130426141258.3011: *3* setEntType
    def setEntType(self, type):
        """
            Set the entity type
        """
        self.__entType=type
    #@+node:1.20130426141258.3012: *3* getEntityType
    def getEntityType(self):
        """
            Get the entity type
        """
        return self.__entType
    #@-others
    eType=property(getEntityType,setEntType,None,"Get/Set the etity type ")
#@-others
#@-leo
