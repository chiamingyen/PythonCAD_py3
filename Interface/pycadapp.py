#@+leo-ver=5-thin
#@+node:1.20130426141258.3678: * @file pycadapp.py
#
# Copyright (c) 2010 Matteo Boscolo, Gertwin Groen
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
# This module contain global functions
#

# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QString', 2)


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3679: ** <<declarations>> (pycadapp)
from PyQt4 import QtGui
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3680: ** class PyCadApp
class PyCadApp(object):
    '''
    PyCadApp contain static interface functions to the kernel application object.
    '''

    # kernel application object
    __application = None
    # main application window
    __cad_window = None
    
    
    #@+others
    #@+node:1.20130426141258.3681: *3* CadWindow
    @staticmethod
    def CadWindow():
        '''
        Gets the main window.
        The main window is an instance of the CadWindow object.
        '''
        return PyCadApp.__cad_window
    #@+node:1.20130426141258.3682: *3* SetCadWindow
    @staticmethod
    def SetCadWindow(cad_window):
        '''
        Sets the main window.
        The main window is an instance of the CadWindow object.
        '''
        PyCadApp.__cad_window = cad_window
    #@+node:1.20130426141258.3683: *3* Application
    @staticmethod
    def Application():
        '''
        Gets the application object from the kernel.
        '''
        return PyCadApp.__application
    #@+node:1.20130426141258.3684: *3* SetApplication
    @staticmethod
    def SetApplication(application):
        '''
        Sets the application object from the kernel.
        '''
        PyCadApp.__application = application
    #@+node:1.20130426141258.3685: *3* ActiveDocument
    @staticmethod
    def ActiveDocument():
        '''
        Gets the current active document in the editor.
        '''
        if not PyCadApp.__application is None:
            return PyCadApp.__application.ActiveDocument
        return None
    #@+node:1.20130426141258.3686: *3* CreateNewDocument
    @staticmethod
    def CreateNewDocument():
        '''
        Create a new document.
        '''
        if not PyCadApp.__application is None:
            PyCadApp.__application.newDocument()
            return PyCadApp.__application.ActiveDocument
        return None
    #@+node:1.20130426141258.3687: *3* OpenDocument
    @staticmethod
    def OpenDocument(filename):
        '''
        Open an existing document.
        '''
        if not PyCadApp.__application is None:
            PyCadApp.__application.openDocument(filename)
            # return the opened, current active document
            return PyCadApp.ActiveDocument()
        return None
    #@+node:1.20130426141258.3688: *3* critical
    @staticmethod
    def critical(text):
        '''
        Shows an critical message dialog
        '''
        dlg = QtGui.QMessageBox()
        dlg.setText(text)
        dlg.setIcon(QtGui.QMessageBox.Critical)
        dlg.exec_()
        return
    #@-others
#@-others
#@-leo
