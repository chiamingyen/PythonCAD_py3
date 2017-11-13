#!/usr/bin/env python

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
# This  module provide the main api interface of pythoncad
#
#


import sys
import os
import shutil
from PyQt5 import QtCore
#
if __name__=="__main__":
    sys.path.append(os.path.join(os.getcwd(), 'Kernel'))
#
from Kernel.pycadevent          import PyCadEvent
from Kernel.exception           import *
from Kernel.document            import *
from Kernel.Command             import *
class Application(object):
    """
        this class provide the real pythoncad api interface ..
    """
    def __init__(self, **args):
        userDirectory=os.getenv('USERPROFILE') or os.getenv('HOME')
        pyUserDir=os.path.join(userDirectory, "PythonCAD")
        if not os.path.exists(pyUserDir):
            os.makedirs(pyUserDir)
        baseDbName=os.path.join(pyUserDir, 'PythonCAD_Local.pdr')
        #--
        self.kernel=Document(baseDbName)
        self.__applicationCommand=APPLICATION_COMMAND
        # Setting up Application Events
        self.startUpEvent=PyCadEvent()
        self.beforeOpenDocumentEvent=PyCadEvent()
        self.afterOpenDocumentEvent=PyCadEvent()
        self.beforeCloseDocumentEvent=PyCadEvent()
        self.afterCloseDocumentEvent=PyCadEvent()
        self.activateDocumentEvent=PyCadEvent()
        # manage Document inizialization
        self.__Documents={}
        # 除了開檔之外, 其餘 active document 設為 None
        if 'open' in args:
            self.openDocument(args['open'])
        else:
            self.__ActiveDocument=None
        # Fire the Application inizialization
        self.startUpEvent(self)
    @property
    def getRecentFiles(self):
        """
            read from application settings the recent files
        """
        objSettings=self.getApplicationSetting()
        nFiles=objSettings.getVariable("MAX_RECENT_FILE")
        if nFiles:
            files=objSettings.getVariable("RECENT_FILE_ARRAY")
            if files:
                return files
            else:
                objSettings.setVariable("RECENT_FILE_ARRAY",[] )
                self.updateApplicationSetting(objSettings)
        else:
            objSettings.setVariable("MAX_RECENT_FILE",MAX_RECENT_FILE )
            objSettings.setVariable("RECENT_FILE_ARRAY",[] )
            self.updateApplicationSetting(objSettings)
        return []
    def addRecentFiles(self,fPath):
    #-- - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=
    #                                                                   S-PM 110427
    #Method to add the given full file name on top of the "Open history list",
    #provided it is different from the one already present on top of the list.
    #
    #--Req-global
    #MAX_RECENT_FILE    local default max. history list length
    #
    #--Req
    #fPath   full file name to add to the list
    #-- - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=
        #--standard "Documentation String"
        """Add a new file name on top of the history list"""

        #--Register
        rgO=None    #Object
        rgN=None    #Integer
        rgL=None    #List

        #--Action
        rgO=self.getApplicationSetting()    #get current settings

        #--get and consider history list lenght parameter
        rgN=rgO.getVariable("MAX_RECENT_FILE")
        if (not rgN): rgN=0 #assure it's numeric
        if (rgN<1):   #<-force a local default value, if not given
            rgN=MAX_RECENT_FILE
            if (rgN<1): rgN=1   #force anyhow at least a length=1
            rgO.setVariable("MAX_RECENT_FILE",rgN)
        #>

        #--get and consider current history list
        rgL=rgO.getVariable("RECENT_FILE_ARRAY")
        if (not rgL):   #<-assign an empty list, if not given
            rgL=[]
        #>

        #--conditioned addition of the given full file name
        if (len(rgL)==0):       #<-empty list:
            rgL.insert(0,fPath)      #add given file path
        elif (rgL[0]!=fPath):   #=-last recorded path is not the same:
            rgL.insert(0,fPath)      #add given file path
        #>

        while(len(rgL)>(rgN)):    #--chop the list to the desired length
            rgL.pop(-1)
        #>

        rgO.setVariable("RECENT_FILE_ARRAY", rgL)   #--update current settings
        self.updateApplicationSetting(rgO)
    #addRecentFiles>


    def getCommand(self,commandType):
        """
            Get a command of commandType
        """
        if not self.__ActiveDocument:
            raise EntityMissing("Miss Active document in the application")
        if commandType in self.__applicationCommand:
            cmd=self.__applicationCommand[commandType]
            cmdIstance=cmd(self.__ActiveDocument)
            return cmdIstance
        else:
            raise PyCadWrongCommand("")
    def getCommandList(self):
        """
            get the list of all the command
        """
        return list(self.__applicationCommand.keys())
    def newDocument(self, fileName=None):
        """
            Create a new document empty document in the application
        """
        newDoc=Document(fileName)
        fileName=newDoc.dbPath
        self.__Documents[fileName]=newDoc
        self.afterOpenDocumentEvent(self, self.__Documents[fileName])   #   Fire the open document event
        self.ActiveDocument=self.__Documents[fileName]      #   Set Active the document
        self.addRecentFiles(fileName)
        return self.__Documents[fileName]
    def openDocument(self, fileName):
        """
            open a saved document
        """
        
        self.beforeOpenDocumentEvent(self, fileName)
        if fileName not in self.__Documents:
            self.__Documents[fileName]=Document(fileName)
            self.addRecentFiles(fileName)
        self.afterOpenDocumentEvent(self, self.__Documents[fileName])   #   Fire the open document event
        self.ActiveDocument=self.__Documents[fileName]                  #   Set Active the document
        return self.__Documents[fileName]


    def saveAs(self, newFileName):
        """
            seve the current document to the new position
        """

        if self.__ActiveDocument:
            (name, extension)=os.path.splitext(str(newFileName))
            if extension.upper()=='.DXF':
                self.__ActiveDocument.exportExternalFormat(newFileName)
                return self.__ActiveDocument
            else:
                oldFileName = self.__ActiveDocument.getName()
                print("oldFileName is:", oldFileName)
                print("newFileName:", newFileName)
                # 可以正確 close oldFileName
                self.closeDocument(oldFileName)
                # 在 PyQt5 模式下, 好像沒有正確執行 copy2 ??
                shutil.copy2(oldFileName, newFileName)
                #return self.openDocument(newFileName)
                return self.openDocument(oldFileName)
        raise EntityMissing("No document open in the application unable to perform the saveAs comand")

    def closeDocument(self, dFile):
    #-- - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=
    #                                                                   S-PM 110427
    # Method to "Close" the named drawing file.
    # --Rq-local
    #  __Documents   dictionary of currently opened drawing files
    #                (was misspelled: "__Docuemnts")
    # --Rq
    #  dFile         drawing file to close
    # -- - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=

    #"Close current document"    #standard "Documentation String"

        self.beforeCloseDocumentEvent(self, dFile)   #initial house-keeping

        if dFile in self.__Documents: #<-file to Close is there:
            self.__Documents[dFile].close()
            del(self.__Documents[dFile])    #delete from dictionary
            #--check dictionary for possible next active document
            for keyDoc in self.__Documents: #<-dictionary is not empty:
                self.ActiveDocument = self.__Documents[keyDoc]    #pick next
                break
            else:   #=-dictionary is empty:
                self.ActiveDocument = None  #set no active document
            #>
        else:   #=-file to Close is NOT there:
            raise IOError("Unable to close the file:  %s"%str(dFile))
        #>

        self.afterCloseDocumentEvent(self)          #final house-keeping

    #closeDocument>

    # 參考: http://www.python-course.eu/python3_properties.php
    @property
    def ActiveDocument(self):
        """
            get The active Document
        """
        return self.__ActiveDocument
    @ActiveDocument.setter
    def ActiveDocument(self, document):
        """
            Set the document to active
        """
        if document:
            print("1- document is:", document)
            # document 為 Kernel.document.Document 物件
            #self.__Documents is dictionary
            print("2- self.__Documents is:", self.__Documents)
            print("3. document.dbPath is:", document.dbPath)
            #path = document.dbPath.replace("\\", "\\\\")
            #print("4. path:", path)
            if document.dbPath in self.__Documents:
                self.__ActiveDocument=self.__Documents[document.dbPath]
            else:
                raise EntityMissing("Unable to set active the document %s"%str(document.dbPath))
        else:
            self.__ActiveDocument=document
        self.activateDocumentEvent(self, self.__ActiveDocument)
        

    def getDocuments(self):
        """
            get the Docuemnts Collection
        """
        return self.__Documents
    #
    # manage application style
    #
    def getApplicationStyleList(self):
        """
            Get the application styles
        """
        return self.kernel.getDBStyles()
    def getApplicationStyle(self, id=None, name=None):
        """
            retrive a style from the application
        """
        return self.kernel.getStyle(id, name)
    def setApplicationStyle(self, style):
        """
            add style to the application
        """
        self.kernel.saveEntity(style)
    def deleteApplicationStyle(self, styleID):
        """
            delete the application style
        """
        self.kernel.deleteEntity(styleID)
    #
    # Manage the application settings
    #
    def getApplicationSetting(self):
        """
            return the setting object from the application
        """
        return self.kernel.getDbSettingsObject()
    def updateApplicationSetting(self, settingObj):
        """
            update the application settingObj
        """
        #apObj=self.kernel.getDbSettingsObject()
        #apObj.setConstructionElement(settingObj)
        self.kernel.saveEntity(settingObj)
if __name__=='__main__':
    from . import application_test  as test
    app= Application()
    doc=app.newDocument()
    #doc.importExternalFormat('C:\Users\mboscolo\Desktop\jettrainer.dxf')
    #segments=doc.getEntityFromType("SEGMENT")
    #print len(segments)
    #test.TestSympy()
    test.TestIntersection()
