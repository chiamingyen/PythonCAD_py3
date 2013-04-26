#@+leo-ver=5-thin
#@+node:1.20130426141258.2595: * @file composedentity.py
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
# This module provide basic DB class for storing entity with relation in pythoncad
# entity such as Chamfer Fillet Blocks
#



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.2596: ** <<declarations>> (composedentity)
from Kernel.Db.pycadobject      import *
from Kernel.GeoEntity.style            import Style
from Kernel.GeoEntity.point            import Point
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.2597: ** class ComposedEntity
class ComposedEntity(PyCadObject):
    """
        this class provide the besic functionality for storing entity that need a 
        sort of relation such Chamfer Fillet Blocks
    """
    #@+others
    #@+node:1.20130426141258.2598: *3* __init__
    def __init__(self, objId,constructionElements, eType, style, childEnt=[] ):
        """
            Inizialize a composed entity
        """
        from Kernel.initsetting             import PY_CAD_COMPOSED_ENT 
        if not eType in PY_CAD_COMPOSED_ENT:
            raise TypeError('entType not supported')
        PyCadObject.__init__(self,eType=eType, objId=objId,style=style)
        self.setChildEnt(childEnt)
        self.setConstructionElement(constructionElements)
    #@+node:1.20130426141258.2599: *3* getChildEnt
    def getChildEnt(self):
        """
            return an array of cildren ents
        """
        return self.__childEnt
    #@+node:1.20130426141258.2600: *3* setChildEnt
    def setChildEnt(self, childEnt):
        """
            set all the child entitys
        """
        from Kernel.initsetting             import PY_CAD_ENT   
        for ent in childEnt:
            if not ent.eType in PY_CAD_ENT:
                raise TypeError('entType with id: %s not supported as child ent'%(str(ent.getId())))
        self.__childEnt=childEnt
    #@+node:1.20130426141258.2601: *3* getConstructionElements
    def getConstructionElements(self):
        """
            Return the base entity
        """
        return self._constructionElements
    #@+node:1.20130426141258.2602: *3* setConstructionElement
    def setConstructionElement(self, constructionElements):
        """
            set the construction elements for the object
        """
        if not isinstance(constructionElements,dict):
            raise TypeError('type error in dictionary')
        self._constructionElements=constructionElements
    #@-others
#@-others
#@-leo
