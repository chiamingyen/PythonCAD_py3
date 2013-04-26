#@+leo-ver=5-thin
#@+node:1.20130426141258.3042: * @file externalformat.py
#
# Copyright (c) 2009,2010 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the termscl_bo of the GNU General Public License as published by
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


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3043: ** <<declarations>> (externalformat)
import os.path
#
from Kernel.ExternalFormat.Dxf.dxf import Dxf
from Kernel.exception import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3044: ** class ExtFormat
#
class ExtFormat(object):
    """
        This class provide base class for hendly different drawing format in pythoncad
    """
    #@+others
    #@+node:1.20130426141258.3045: *3* __init__
    def __init__(self,kernel):
        """
            Default Constructor
        """
        self.__kernel=kernel
        self.__errorList=[]
    #@+node:1.20130426141258.3046: *3* openFile
    def openFile(self,fileName):
        """
           Open a generic file
        """
        path,exte=os.path.splitext( fileName )
        if( exte.upper()==".dxf".upper()):
            dxf=Dxf(self.__kernel,fileName)
            dxf.importEntitis()
            if not dxf.getError() is None:
                self.__errorList=dxf.getError()
                raise DxfReport("Dxf report have to be shown some error/warning in import dxf")
        else:
            raise  DxfUnsupportedFormat("Format %s not supported"%str(exte))
    #@+node:1.20130426141258.3047: *3* saveFile
    def saveFile(self,fileName):
        """
            save the current file in a non pythoncad Format
        """
        path,exte=os.path.splitext( fileName )
        if( exte.upper()==".dxf".upper()):
            dxf=Dxf(self.__kernel,fileName)
            dxf.exportEntitis()
    #@+node:1.20130426141258.3048: *3* getErrorList
    def getErrorList(self):
        """
            get the error warning generated
        """
        return self.__errorList
    #@-others
#@-others
#@-leo
