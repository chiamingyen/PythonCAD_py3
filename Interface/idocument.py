#@+leo-ver=5-thin
#@+node:1.20130426141258.3656: * @file idocument.py
#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3657: ** <<declarations>> (idocument)
from PyQt4 import QtCore, QtGui
from Generic.Kernel.document import *
from Interface.LayerIntf.layerdock  import LayerDock
from Interface.cadscene             import CadScene
from Interface.cadview              import CadView
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3658: ** class IDocument
class IDocument(QtGui.QMdiSubWindow):
    sequenceNumber = 1
    #@+others
    #@+node:1.20130426141258.3659: *3* __init__
    def __init__(self, document, cmdInf, parent):
        super(IDocument, self).__init__(parent)
        IDocument.sequenceNumber += 1
        self.__document=document
        self.__document.handledErrorEvent+=self._errorEvent
        self.__cmdInf=cmdInf
        self.__cadwindow=parent
        self.setWindowTitle(document.dbPath + '[*]')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True
        # layer list
        self.__layer_dock = LayerDock(self,self.__document)
        self._scene = CadScene(document, parent=self)
        self.__cmdInf.commandLine.evaluatePressed+=self.scene.textInput
        self.__view = CadView(self._scene, self)
        # the graphics view is the main/central component
        innerWindows = QtGui.QMainWindow()
        innerWindows.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.__layer_dock)
        innerWindows.setCentralWidget(self.__view)
        self.setWidget(innerWindows)
        #Inizialize scene
        self._scene.initDocumentEvents()
        self._scene.populateScene(document)
        self._scene.zoomWindows+=self.__view.zoomWindows
        self._scene.fireCommandlineFocus+=self.__cmdInf.commandLine.setFocus
        self._scene.fireKeyShortcut+=self.keyShortcut
        self._scene.fireKeyEvent+=self.keyEvent
        self._scene.fireWarning+=self.popUpWarning
        self._scene.fireCoords+=self.setStatusbarCoords
    #@+node:1.20130426141258.3660: *3* document
    @property
    def document(self):
        return self.__document
    #@+node:1.20130426141258.3661: *3* cmdInf
    @property
    def cmdInf(self):
        return self.__cmdInf
    #@+node:1.20130426141258.3662: *3* view
    @property
    def view(self):
        return self.__view
    #@+node:1.20130426141258.3663: *3* scene
    @property
    def scene(self):
        return self._scene
    #@+node:1.20130426141258.3664: *3* application
    @property
    def application(self):
        """
        get the kernel application object
        """
        return self.__application
    #@+node:1.20130426141258.3665: *3* layerDock
    @property
    def layerDock(self):
        """
        get the layer tree dockable window
        """
        return self.__layer_dock
    #@+node:1.20130426141258.3666: *3* fileName
    @property
    def fileName(self):
        """
            get the current file name
        """
        return self.document.dbPath
    #@+node:1.20130426141258.3667: *3* unDo
    def unDo(self):
        """
            perform undo on the active document
        """
        self.document.unDo()
        self.__layer_dock.RefreshStructure()
    #@+node:1.20130426141258.3668: *3* reDo
    def reDo(self):
        """
            perform redo on the active document
        """
        self.document.reDo()
        self.__layer_dock.RefreshStructure()
    #@+node:1.20130426141258.3669: *3* importExternalFormat
    def importExternalFormat(self, file):
        """
            import an external document
        """
        self.document.importExternalFormat(file)
    #@+node:1.20130426141258.3670: *3* renderCurrentScene
    def renderCurrentScene(self, painter):
        """
            render the current scene for the printer
        """
        self.view.render(painter)
    #@+node:1.20130426141258.3671: *3* wWellEWvent
    def wWellEWvent(self, event):
        self.__view.scaleFactor=math.pow(2.0, -event.delta() / 240.0)
        self.__view.scaleView(self.__view.scaleFactor)
    #@+node:1.20130426141258.3672: *3* popUpWarning
    def popUpWarning(self, msg):
        """
            popUp a warning mesage
        """
        ret = QtGui.QMessageBox.warning(self,"Warning",  msg)
        return
    #@+node:1.20130426141258.3673: *3* popUpInfo
    def popUpInfo(self, msg):
        """
            popUp a Info mesage
        """
        ret = QtGui.QMessageBox.information(self,"Information",  msg)
        return
    #@+node:1.20130426141258.3674: *3* _errorEvent
    def _errorEvent(self, err):
        """
            executed when the document rise an error
            the err is a dictionary like the one below
            _err={'object':, 'error':}
        """
        msgBox=QtGui.QMessageBox(self)
        msgBox.setIcon(QtGui.QMessageBox.Critical)
        msg="Error came from object %s"%(str(err['error']))
        dmsg=msg
        for _e in err['object'].getErrorList():
            dmsg=dmsg+"\n"+str(_e)
        msgBox.setWindowTitle("Error !!")
        msgBox.setText(msg)
        msgBox.setDetailedText(dmsg)
        msgBox.exec_()
        return
    #@+node:1.20130426141258.3675: *3* setStatusbarCoords
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------------------MANAGE SCENE EVENTS
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def setStatusbarCoords(self, x, y, status):
        #set statusbar coordinates when mouse move on the scene
        if status=="abs":
            self.__cadwindow.coordLabel.setText("X="+str("%.3f" % x)+"\n"+"Y="+str("%.3f" % y)) # "%.3f" %  sets the precision decimals to 3
        elif status=="rel":
            self.__cadwindow.coordLabel.setText("dx="+str("%.3f" % x)+"\n"+"dy="+str("%.3f" % y)) # "%.3f" %  sets the precision decimals to 3
    #@+node:1.20130426141258.3676: *3* keyEvent
    def keyEvent(self, event): #fire the key event in the scene to the commandline
        self.__cmdInf.commandLine._keyPress(event)
    #@+node:1.20130426141258.3677: *3* keyShortcut
    def keyShortcut(self, command):
        self.__cadwindow.statusBar().showMessage(str(command))
        self.__cadwindow.callCommand(command)
    #@-others
#@-others
#@-leo
