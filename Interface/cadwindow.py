############################################################################
#
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
#
#  This file is part of the example classes of the Qt Toolkit.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  this file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
#
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
############################################################################

# This is only needed for Python v2 but is harmless for Python v3.

#import sip
#sip.setapi('QString', 2)



import os
import sys

from PyQt5 import QtCore, QtGui, QtPrintSupport, QtWidgets

from . import cadwindow_rc

from Generic.application            import Application

#Interface
from Interface.LayerIntf.layerdock  import LayerDock
from Interface.cadscene             import CadScene
from Interface.cadview              import CadView
from Interface.idocument            import IDocument
from Interface.CmdIntf.cmdintf      import CmdIntf
from Interface.Entity.base          import BaseEntity
from Interface.Command.icommand     import ICommand
from Interface.cadinitsetting       import *
from Interface.Dialogs.preferences  import Preferences
#Kernel
from Kernel.exception               import *
from Kernel.initsetting             import * #SNAP_POINT_ARRAY, ACTIVE_SNAP_POINT


from Interface.DrawingHelper.polarguides import getPolarMenu
class CadWindowMdi(QtWidgets.QMainWindow):
    def __init__(self):
        super(CadWindowMdi, self).__init__()
        self.mdiArea = QtWidgets.QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)
        self.mdiArea.subWindowActivated.connect(self.subWindowActivatedEvent)
        self.oldSubWin=None
    #        self.readSettings() #now works for position and size, support for toolbars is still missing(http://www.opendocs.net/pyqt/pyqt4/html/qsettings.html)
        self.setWindowTitle("PythonCAD")
        qIcon=self._getIcon('pythoncad')
        if qIcon:
            self.setWindowIcon(qIcon)
        self.setUnifiedTitleAndToolBarOnMac(True)
        #pythoncad kernel
        self.__application = Application()
        self.__cmd_intf = CmdIntf(self)
        #self.__cmd_intf.FunctionHandler.commandExecuted+=self.commandExecuted
        # create all dock windows
        self._createDockWindows()
        # create status bar
        self._createStatusBar()
        self.setUnifiedTitleAndToolBarOnMac(True)
        self._registerCommands()
        self.updateMenus()
        self.lastDirectory=os.getenv('USERPROFILE') or os.getenv('HOME')

        self.readSettings() #now works for position and size and ismaximized, and finally toolbar position
        return
    @property
    def scene(self):
        if self.mdiArea.activeSubWindow():
            return self.mdiArea.activeSubWindow().scene
    @property
    def view(self):
        if self.mdiArea.activeSubWindow():
            return self.mdiArea.activeSubWindow().view
    @property
    def Application(self):
        """
            get the kernel application object
        """
        return self.__application
    @property
    def LayerDock(self):
        """
            get the layer tree dockable window
        """
        return self.__layer_dock
    # ###############################################STATUSBAR
    # ##########################################################

    def _createStatusBar(self):
        '''
            Creates the statusbar object.
        '''

        self.statusBar().showMessage("Ready")

        #------------------------------------------------------------------------------------Create status buttons

        #Force Direction
        self.forceDirectionStatus=statusButton('SForceDir.png', 'Orthogonal Mode [right click will in the future set increment constrain angle]')
        self.forceDirectionStatus.clicked.connect(self.setForceDirection)
        self.forceDirectionStatus.setMenu(getPolarMenu())
        self.statusBar().addPermanentWidget(self.forceDirectionStatus)


        #Snap
        self.SnapStatus=statusButton('SSnap.png', 'Snap [right click displays snap list]\n for future implementation it should be a checkist')
        self.SnapStatus.clicked.connect(self.setSnapStatus)
        self.SnapStatus.setMenu(self.__cmd_intf.Category.getMenu(6))
        self.SnapStatus.setChecked(True)
        self.statusBar().addPermanentWidget(self.SnapStatus)


        #Grid
        self.GridStatus=statusButton('SGrid.png', 'Grid Mode [not available yet]')
        self.GridStatus.clicked.connect(self.setGrid)
        self.statusBar().addPermanentWidget(self.GridStatus)

        #------------------------------------------------------------------------------------Set coordinates label on statusbar (updated by idocumet)
        self.coordLabel=QtWidgets.QLabel("x=0.000\ny=0.000")
        self.coordLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.coordLabel.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.coordLabel.setMinimumWidth(80)
        self.coordLabel.setMaximumHeight(20)
        self.coordLabel.setFont(QtGui.QFont("Sans", 6))
        self.statusBar().addPermanentWidget(self.coordLabel)
    def setForceDirection(self):
        if self.forceDirectionStatus.isChecked():
            self.scene.forceDirectionEnabled=True
            self.forceDirectionStatus.setFocus(False)
            if self.scene.activeICommand!=None and self.scene.fromPoint!=None:
                self.scene.GuideHandler.show()
        else:
            self.scene.forceDirectionEnabled=False
            self.scene.GuideHandler.hide()
    def setSnapStatus(self):
        if self.SnapStatus.isChecked():
            self.scene.snappingPoint.activeSnap=SNAP_POINT_ARRAY['LIST']
        else:
            self.scene.snappingPoint.activeSnap=SNAP_POINT_ARRAY['NONE']
    def setGrid(self):
        pass
    # ###############################################END STATUSBAR
    # ##########################################################

    def commandExecuted(self):
        self.resetCommand()
    def _createDockWindows(self):
        '''
            Creates all dockable windows for the application
        '''
        # commandline
        command_dock = self.__cmd_intf.commandLine
        # if the commandline exists, add it
        if not command_dock is None:
            self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, command_dock)
        return
    def closeEvent(self, event):
        """
            manage close event
        """
        self.mdiArea.closeAllSubWindows()
        if self.activeMdiChild():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
    
    def writeSettings(self):
        settings = QtCore.QSettings('PythonCAD', 'MDI Settings')

    def subWindowActivatedEvent(self):
        """
            Sub windows activation
        """
        if self.mdiArea.activeSubWindow():
            if (self.mdiArea.activeSubWindow().document!=
                        self.__application.ActiveDocument):
                self.resetCommand()
                self.__application.ActiveDocument=self.mdiArea.activeSubWindow().document
        self.updateMenus()
    def resetCommand(self):
        """
            Resect the active command
        """
        self.__cmd_intf.resetCommand()
        if self.scene!=None:
            self.scene.cancelCommand()
        self.statusBar().showMessage("Ready")
    # ################################# SET if ICON AND MENU are ENABLED
    # ##########################################################
    def updateMenus(self):
        """
            update menu status
        """
        hasMdiChild = (self.activeMdiChild() is not None)
        #File
        self.__cmd_intf.setVisible('import', hasMdiChild)
        self.__cmd_intf.setVisible('saveas', hasMdiChild)
        self.__cmd_intf.setVisible('close', hasMdiChild)
        self.__cmd_intf.setVisible('print', hasMdiChild)
        #Edit
        self.__cmd_intf.setVisible('undo', hasMdiChild)
        self.__cmd_intf.setVisible('redo', hasMdiChild)
        self.__cmd_intf.setVisible('copy', hasMdiChild)
        self.__cmd_intf.setVisible('move', hasMdiChild)
        self.__cmd_intf.setVisible('delete', hasMdiChild)
        self.__cmd_intf.setVisible('mirror', hasMdiChild)
        self.__cmd_intf.setVisible('rotate', hasMdiChild)
        self.__cmd_intf.setVisible('trim', hasMdiChild)
        self.__cmd_intf.setVisible('property', hasMdiChild)
        #Draw
        self.__cmd_intf.setVisible('point', hasMdiChild)
        self.__cmd_intf.setVisible('segment', hasMdiChild)
        self.__cmd_intf.setVisible('rectangle', hasMdiChild)
        self.__cmd_intf.setVisible('polyline', hasMdiChild)
        self.__cmd_intf.setVisible('circle', hasMdiChild)
        self.__cmd_intf.setVisible('arc', hasMdiChild)
        self.__cmd_intf.setVisible('ellipse', hasMdiChild)
        self.__cmd_intf.setVisible('polygon', hasMdiChild)
        self.__cmd_intf.setVisible('fillet', hasMdiChild)
        self.__cmd_intf.setVisible('chamfer', hasMdiChild)
        self.__cmd_intf.setVisible('bisect', hasMdiChild)
        self.__cmd_intf.setVisible('text', hasMdiChild)
        #Dimension
        self.__cmd_intf.setVisible('dimension', hasMdiChild)
        #View
        self.__cmd_intf.setVisible('fit', hasMdiChild)
        self.__cmd_intf.setVisible('zoomwindow', hasMdiChild)
        self.__cmd_intf.setVisible('zoomitem', hasMdiChild)
        #snap
        self.__cmd_intf.setVisible('snapauto', hasMdiChild)
        self.__cmd_intf.setVisible('snapend', hasMdiChild)
        self.__cmd_intf.setVisible('snapmid', hasMdiChild)
        self.__cmd_intf.setVisible('snapcen', hasMdiChild)
        self.__cmd_intf.setVisible('snapper', hasMdiChild)
        self.__cmd_intf.setVisible('snaptan', False)
        self.__cmd_intf.setVisible('snapqua', hasMdiChild)
        self.__cmd_intf.setVisible('snap00', hasMdiChild)
        self.__cmd_intf.setVisible('snapint', hasMdiChild)
        #Tools
        self.__cmd_intf.setVisible('info2p', hasMdiChild)
        #window
        self.__cmd_intf.setVisible('tile', hasMdiChild)
        self.__cmd_intf.setVisible('cascade', hasMdiChild)
        self.__cmd_intf.setVisible('next', hasMdiChild)
        self.__cmd_intf.setVisible('previous', hasMdiChild)
        #hasSelection = (self.activeMdiChild() is not None and
        #                self.activeMdiChild().textCursor().hasSelection())
        #self.cutAct.setEnabled(hasSelection)
        #self.copyAct.setEnabled(hasSelection)

        #StatusBAR Satus Tools
        self.forceDirectionStatus.setEnabled(hasMdiChild)
        self.GridStatus.setEnabled(hasMdiChild)
        self.SnapStatus.setEnabled(hasMdiChild)
    def createMdiChild(self, file=None):
        """
            Create new IDocument
        """
        if file:
            newDoc=self.__application.openDocument(file)
        else:
            newDoc=self.__application.newDocument()
        for mdiwind in self.mdiArea.subWindowList():
            if mdiwind._IDocument__document.dbPath==file:
                child=mdiwind
                break
        else:
            child = IDocument(newDoc,self.__cmd_intf, self)
            self.mdiArea.addSubWindow(child)

        #child.copyAvailable.connect(self.cutAct.setEnabled)
        #child.copyAvailable.connect(self.copyAct.setEnabled)
        return child
    #def setAppDocActiveOnUi(self, doc):
    #    self.mdiArea.

    def _registerCommands(self):
        '''
            Register all commands that are handed by this object
        '''
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, 'new', '&New Drawing', self._onNewDrawing)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, 'open', '&Open Drawing...', self._onOpenDrawing)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, 'import', '&Import Drawing...', self._onImportDrawing)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, 'saveas', '&Save As...', self._onSaveAsDrawing)
        #
        # Create recentFile structure
        #
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, '-')

        i=0
        for file in self.Application.getRecentFiles:
            fileName=self.strippedName(file)
            self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, 'file_'+str(i), fileName, self._onOpenRecent)
            i+=1
        #
        # separator
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, 'close', '&Close', self._onCloseDrawing)
        # separator
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, 'print', '&Print', self._onPrint)
        # separator
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.File, 'quit', '&Quit', self.close)
        # Edit
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Edit, 'undo', '&Undo', self._onUndo)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Edit, 'redo', '&Redo', self._onRedo)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Edit, 'property', '&Property', self._onProperty)

        # separator
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Edit, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Edit, 'preferences', '&User Preferences', self.preferences)
        #Modify
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Modify, 'copy', '&Copy', self._onCopy)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Modify, 'move', '&Move', self._onMove)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Modify, 'rotate', '&Rotate', self._onRotate)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Modify, 'mirror', '&Mirror', self._onMirror)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Modify, 'delete', '&Delete', self._onDelete)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Modify, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Modify, 'trim', '&Trim', self._onTrim)
        # Draw
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'point', '&Point', self._onPoint)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'segment', '&Segment', self._onSegment)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'rectangle', '&Rectangle', self._onRectangle)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'polyline', '&Polyline', self._onPolyline)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'circle', '&Circle', self._onCircle)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'arc', '&Arc', self._onArc)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'ellipse', '&Ellipse', self._onEllipse)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'polygon', '&Polygon', self._onPolygon)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'fillet', '&Fillet', self._onFillet)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'chamfer', '&Chamfer', self._onChamfer)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'bisect', '&Bisect', self._onBisect)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Draw, 'text', '&Text', self._onText)
        #   Dimension
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Dimension, 'dimension', '&Aligned Dimension', self._onDimension)
        # View
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.View, 'fit', '&Fit', self._onFit)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.View, 'zoomwindow', 'Zoom&Window', self._onZoomWindow)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.View, 'zoomitem', 'Zoom&Item',self._onCenterItem)
        # Snap
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, 'snapauto', 'Automatic Snap', self._onSnapCommand)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, 'snapend', 'End', self._onSnapCommand)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, 'snapmid', 'Middle', self._onSnapCommand)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, 'snapint', 'Intersection', self._onSnapCommand)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, 'snapper', 'Perpendicular', self._onSnapCommand)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, 'snapcen', 'Center', self._onSnapCommand)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, 'snapqua', 'Quadrant', self._onSnapCommand)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, 'snaptan', 'Tangent', self._onSnapCommand)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, '-')
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Snap, 'snap00', 'Origin', self._onSnapCommand)

        #Tools
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Tools, 'info2p', 'Info Two Points', self._onInfo2p)

        #--menu: Windows
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Windows, 'tile', '&Tile', self._onTile)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Windows, 'cascade', '&Cascade', self._onCascade)

        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Windows, 'next', 'Ne&xt', self.mdiArea.activateNextSubWindow)
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Windows, 'previous', 'Pre&vious', self.mdiArea.activatePreviousSubWindow)

        # Help
        self.__cmd_intf.registerCommand(self.__cmd_intf.Category.Help, 'about', '&About PythonCAD', self._onAbout)
        return
    def updateRecentFileList(self):
        """
            update the menu recent file list
        """
        i=0
        for file in self.Application.getRecentFiles:
            fileName=self.strippedName(file)
            self.__cmd_intf.updateText('file_'+str(i), fileName)
            i+=1
    def strippedName(self, fullFileName):
        """
            get only the name of the filePath
        """
        # 正確取得 stripped file name
        return QtCore.QFileInfo(fullFileName).fileName()
    # ##########################################              ON COMMANDS
    # ##########################################################

    def _onNewDrawing(self):
        '''
            Create a new drawing
        '''
        child = self.createMdiChild()
        child.show()
        self.updateRecentFileList()
        return
    def _onOpenDrawing(self):
        '''
            Open an existing drawing PDR or DXF
        '''
        # ask the user to select an existing drawing
        # 可以正確打開檔案, 與 PyQt4 不同
        drawing = str(QtWidgets.QFileDialog.getOpenFileName(parent=self,directory=self.lastDirectory,  caption ="Open Drawing", filter ="Drawings (*.pdr *.dxf)")[0])
        # open a document and load the drawing
        #print("drawing is:", drawing)
        if len(drawing)>0:
            self.lastDirectory=os.path.split(drawing)[0]
            (name, extension)=os.path.splitext(drawing)
            if extension.upper()=='.DXF':
                child = self.createMdiChild()
                child.importExternalFormat(drawing)
            elif extension.upper()=='.PDR':
                child = self.createMdiChild(drawing)
            else:
                self.critical("Wrong command selected")
                return
            child.show()
            self.updateRecentFileList()
            self.view.fit()
        return
    def _onImportDrawing(self):
        '''
            Import existing drawing in current drawing (some issues with PyQt4.7)
        '''
        drawing = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption="Import Drawing", directory=self.lastDirectory, filter="Dxf (*.dxf)")[0]
        # open a document and load the drawing
        if len(drawing)>0:
            self.lastDirectory=os.path.split(drawing)[0]
            self.mdiArea.activeSubWindow().importExternalFormat(drawing)
        return
    def _onOpenRecent(self):
        """
            on open recent file
        """
        #FIXME: if in the command line we insert file_1 or file_2
        #here we get en error action dose not have command attributes
        # action is en edit command not an action and have an empty value
        action = self.sender()
        if action:
            spool, index=action.command.split('_')
            fileName=self.Application.getRecentFiles[int(index)]
            if len(fileName)>0:
                child = self.createMdiChild(fileName)
                child.show()
                self.updateRecentFileList()
                self.view.fit()
        return
    def _onSaveAsDrawing(self):
        drawing = QtWidgets.QFileDialog.getSaveFileName(self, "Save As...", "/home", filter ="Drawings (*.pdr *.dxf)")[0]
        if len(drawing)>0:
            self.__application.saveAs(drawing)
    def _onPrint(self):
    #       printer.setPaperSize(QPrinter.A4);
        self.scene.clearSelection()
        printer=QtPrintSupport.QPrinter()
        printDialog=QtPrintSupport.QPrintDialog(printer)
        if (printDialog.exec_() == QtWidgets.QDialog.Accepted):
            painter=QtGui.QPainter()
            painter.begin(printer)
            painter.setRenderHint(QtGui.QPainter.Antialiasing);
            #self.mdiArea.activeSubWindow().scene.render(painter)
            self.mdiArea.activeSubWindow().view.render(painter)
            painter.end()
        self.statusBar().showMessage("Ready")
        return
    def _onCloseDrawing(self):
        path=self.mdiArea.activeSubWindow().fileName
        self.__application.closeDocument(path)
        self.mdiArea.closeActiveSubWindow()
        return
    #---------------------ON COMMANDS in DRAW

    def _onPoint(self):
        self.statusBar().showMessage("CMD:Point")
        self.callCommand('POINT')
        return
    def _onSegment(self):
        self.statusBar().showMessage("CMD:Segment")
        self.callCommand('SEGMENT')
        return
    def _onCircle(self):
        self.statusBar().showMessage("CMD:Circle")
        self.callCommand('CIRCLE')
        return
    def _onArc(self):
        self.statusBar().showMessage("CMD:Arc")
        self.callCommand('ARC')
        return
    def _onEllipse(self):
        self.statusBar().showMessage("CMD:Ellipse")
        self.callCommand('ELLIPSE')
        return
    def _onRectangle(self):
        self.statusBar().showMessage("CMD:Rectangle")
        self.callCommand('RECTANGLE')
        return
    def _onPolygon(self):
        self.statusBar().showMessage("CMD:Polygon")
        self.callCommand('POLYGON')
        return
    def _onPolyline(self):
        self.statusBar().showMessage("CMD:Polyline")
        self.callCommand('POLYLINE')
        return
    def _onFillet(self):
        self.statusBar().showMessage("CMD:Fillet")
        self.callCommand('FILLET')
        return
    def _onChamfer(self):
        self.statusBar().showMessage("CMD:Chamfer")
        self.callCommand('CHAMFER')
        return
    def _onBisect(self):
        self.statusBar().showMessage("CMD:Bisect")
        self.callCommand('BISECTOR')
        return
    def _onText(self):
        self.statusBar().showMessage("CMD:Text")
        self.callCommand('TEXT')
        return
    def _onDimension(self):
        self.statusBar().showMessage("CMD:Dimension")
        self.callCommand('DIMENSION')
        return
    #-------------------------ON COMMANDS in EDIT

    def _onUndo(self):
        self.scene.clearSelection()
        try:
           self.mdiArea.activeSubWindow().unDo()
        except UndoDbExc:
            self.critical("Unable To Perform Undo")
        self.statusBar().showMessage("Ready")
        return
    def _onRedo(self):
        self.scene.clearSelection()
        try:
            self.mdiArea.activeSubWindow().reDo()
        except UndoDbExc:
            self.critical("Unable To Perform Redo")
        self.statusBar().showMessage("Ready")
    def _onProperty(self):
        self.statusBar().showMessage("CMD:Property")
        self.callCommand('PROPERTY')
    def preferences(self):
        p=Preferences(self)
        #TODO: Fill up preferences
        if (p.exec_() == QtWidgets.QDialog.Accepted):
            #TODO: save Preferences
            pass
    #---------------------------ON COMMANDS in MODIFY

    def _onCopy(self):
        self.statusBar().showMessage("CMD:Copy")
        self.callCommand('COPY')
        return
    def _onMove(self):
        self.statusBar().showMessage("CMD:Move")
        self.callCommand('MOVE')
        return
    def _onDelete(self):
        self.statusBar().showMessage("CMD:Delete")
        self.callCommand('DELETE')
        self.statusBar().showMessage("Ready")
        return
    def _onTrim(self):
        self.statusBar().showMessage("CMD:Trim")
        self.callCommand('TRIM')
        self.statusBar().showMessage("Ready")
        return
    def _onMirror(self):
        self.statusBar().showMessage("CMD:Mirror")
        self.callCommand('MIRROR')
        return
    def _onRotate(self):
        self.statusBar().showMessage("CMD:Rotate")
        self.callCommand('ROTATE')
        return
    #---------------------------ON COMMANDS in VIEW

    def _onFit(self):
        self.view.fit()
    def _onZoomWindow(self):
        self.statusBar().showMessage("CMD:ZoomWindow")
        self.scene._cmdZoomWindow=True
    def _onCenterItem(self):
        self.view.centerOnSelection()
    #---------------------------ON COMMANDS in SNAP

    def _onSnapCommand(self):
        """
            On snep Command action
        """
        #__________SNAP NONE?
        self.scene.clearSelection()
        action = self.sender()
        if action:
            if action.command=="snapauto":
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["LIST"])
            elif action.command=="snapend":
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["END"])
            elif action.command=="snapmid":
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["MID"])
            elif action.command=="snapcen":
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["CENTER"])
            elif action.command=="snapper":
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["ORTHO"])
            elif action.command=="snaptan":
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["TANGENT"])
            elif action.command=="snapqua":
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["QUADRANT"])
            elif action.command=="snap00":
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["ORIG"])
            elif action.command=="snapint":
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["INTERSECTION"])
            else:
                self.scene.setActiveSnap(SNAP_POINT_ARRAY["LIST"])
    #------------------------ON COMMANDS in TOOLS

    def _onInfo2p(self):
        """
            on info two point command
        """
        self.scene.clearSelection()
        self.statusBar().showMessage("CMD:Info2Points")
        self.callCommand('DISTANCE2POINT', 'document')
        return
    #-- - - -=- - - - -=on commands in menu: Windows
    def _onTile(self):   #<-(by: S-PM 110524)
        "on Tile command"    #standard  "Documentation String"

        self.mdiArea.tileSubWindows()   #--call "tile" method
        return
    #_onTile>


    def _onCascade(self):   #<-(by: S-PM 110524)
        "on Cascade command"    #standard  "Documentation String"

    #-- - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=
    #                                                                       Prologue
        def cascadeFit(self):  #<-"Fit" function definition
            #--Register
            rgL=[]      #List
            rgN=0       #Integer
            rgGp=None   #General purpose

            #--Action
            rgL=self.mdiArea.subWindowList()    #--get child-List,
            rgN=len(rgL)                        #  and child-count
            if (rgN<1):  return(rgN)    #no sub-window: exit

            rgW = self.mdiArea.width()  #--get actually available room
            rgH = self.mdiArea.height()

            #--compute cascade offset dimensions
            if (rgN<2):     #<-less than 2 sub-windows: no offset
                rgCx=0
                rgCy=0
            elif (rgN>1):   #<-more than 1 sub-window: get offset
                rgCx=rgL[1].x()
                rgCy=rgL[1].y()
            #>
            rgCx=rgCx*(rgN-1)   #compute total cascade offset
            rgCy=rgCy*(rgN-1)

            #<-loop resize all sub-windows, so to fit them into available room
            for rgGp in rgL:
                rgGp.resize(rgW-rgCx, rgH-rgCy)
            #>

            return(rgN)
        #cascadeFit>

    #-- - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=- - - - -=
    #                                                                       Action
        #--call "cascade" method, as-is (rudimentary)
        self.mdiArea.cascadeSubWindows()

        rgN=cascadeFit(self)    #"fit" all sub-windows into available room
        return
    #encoding: utf-8
    #_onCascade>



    #-----------------------ON COMMANDS in ABOUT

    def _onAbout(self):
        QtWidgets.QMessageBox.about(self, "About PythonCAD",
                """<b>PythonCAD</b> is a CAD package written, surprisingly enough, in Python using the PyQt5 interface.<p>
                   The PythonCAD project aims to produce a scriptable, open-source,
                   easy to use CAD package for any Python/PyQt supported Platforms
                   <p>
                   This is an Alfa Release For The new R38 Vesion <b>(R38.0.0.5)<b><P>
                   <p>
                   <a href="http://sourceforge.net/projects/pythoncad/">PythonCAD Web Site On Sourceforge</a>
                   <p>
                   <a href="http://pythoncad.sourceforge.net/dokuwiki/doku.php">PythonCAD Wiki Page</a>
                   <p>
                   由 KMOL 改為 Python3 與 PyQt5 版本
                   """)
        return
    # ########################################## CALL COMMAND
    # ##########################################################

    def callCommand(self, commandName, commandFrom=None):
        """
            call a document command (kernel)
        """
        try:
            if commandFrom==None or commandFrom=='kernel':
                self.scene.activeKernelCommand=self.__application.getCommand(commandName)
            elif commandFrom=='document':
                self.scene.activeKernelCommand=self.getCommand(commandName)
            else:
                return
            self.scene.activeICommand=ICommand(self.scene)
            self.scene.activeICommand.updateInput+=self.updateInput
            self.updateInput(self.scene.activeKernelCommand.activeMessage)
        except EntityMissing:
            self.scene.cancelCommand()
            self.critical("You need to have an active document to perform this command")
        #checks if scene has selected items and launches them directly to the ICommand
        #if it's first prompt it's "give me entities"
        if len(self.scene.selectedItems())>0:
            if  self.scene.activeKernelCommand.activeException()==ExcMultiEntity:
                qtItems=[item for item in self.scene.selectedItems() if isinstance(item, BaseEntity)]
                self.scene.activeICommand.addMauseEvent(point=None,
                                                    entity=qtItems,
                                                    force=None)
            else:
                self.scene.clearSelection()
    def getCommand(self, name):
        """
            get an interface command
        """
        if name in INTERFACE_COMMAND:
            return INTERFACE_COMMAND[name](self.mdiArea.activeSubWindow().document,
                                           self.mdiArea.activeSubWindow())
        else:
            self.critical("Wrong command")
    def updateInput(self, message):
            self.__cmd_intf.commandLine.printMsg(str(message))
            self.statusBar().showMessage(str(message))
    @staticmethod
    def critical(text):
        '''
            Shows an critical message dialog
        '''
        dlg = QtWidgets.QMessageBox()
        dlg.setText(text)
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.exec_()
        return
    # ########################################## SETTINGS STORAGE
    # ##########################################################
    def readSettings(self):
        settings = QtCore.QSettings('PythonCAD', 'MDI Settings')
        settings.beginGroup("CadWindow")
        max = settings.value("maximized", False)
        # settings.setValue("size", QtCore.QSize(800, 600))
        # settings.setValue("pos", QtCore.QPoint(400, 300))
        if max == True:  # if cadwindow was maximized set it maximized again
            self.showMaximized()
        else:  # else set it to the previous position and size
            try:
                self.resize(settings.value("size").toSize()) # self.resize(settings.value("size", QtCore.QSize(800, 600)).toSize())
                self.move(settings.value("pos").toPoint())   # self.move(settings.value("pos", QtCore.QPoint(400, 300)).toPoint())+
                #self.resize(settings.value("size", QtCore.QSize(800, 600)))
                #self.move(settings.value("pos", QtCore.QPoint(400, 300)))
                #self.resize(settings.value("size"))
                #self.move(settings.value("pos"))
            except:    
                print("Warning: unable to set the previews values")
        settings.endGroup()
        
        settings.beginGroup("CadWindowState")
        try:
            self.restoreState(settings.value('State').toByteArray())
        except:
            print("Warning: Unable to set state")
        settings.endGroup()

    # ########################################## END SETTINGS STORAGE
    # ##########################################################

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None
    def switchLayoutDirection(self):
        if self.layoutDirection() == QtCore.Qt.LeftToRight:
            QtWidgets.QApplication.setLayoutDirection(QtCore.Qt.RightToLeft)
        else:
            QtWidgets.QApplication.setLayoutDirection(QtCore.Qt.LeftToRight)
    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)
    def _getIcon(self, cmd):
        '''
        Create an QIcon object based on the command name.
        The name of the icon is ':/images/' + cmd + '.png'.
        If the cmd = 'Open', the name of the icon is ':/images/Open.png'.
        '''
        icon_name = cmd + '.png'
        icon_path = os.path.join(os.path.join(os.getcwd(), 'icons'), icon_name)
        # check if icon exist
        if os.path.exists(icon_path):
            icon = QtGui.QIcon(icon_path)
            return icon
        # icon not found, don't use an icon, return None
        return None
    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Escape:
            self.resetCommand()

        super(CadWindowMdi, self).keyPressEvent(event)
    # ########################################## SYMPY INTEGRATION
    # ##########################################################

    def plotFromSympy(self, objects):
        """
            plot the sympy Object into PythonCAD
        """
        if self.mdiArea.currentSubWindow()==None:
            self._onNewDrawing()
        for obj in objects:
            self.plotSympyEntity(obj)
    def plotSympyEntity(self, sympyEntity):
        """
            plot the sympy entity
        """
        self.mdiArea.currentSubWindow().document.saveSympyEnt(sympyEntity)
    def createSympyDocument(self):
        """
            create a new document to be used by sympy plugin
        """
        self._onNewDrawing()
    def getSympyObject(self):
        """
            get an array of sympy object
        """
        #if self.Application.ActiveDocument==None:
        if self.mdiArea.currentSubWindow()==None:
            raise StructuralError("unable to get the active document")

        ents=self.mdiArea.currentSubWindow().scene.getAllBaseEntity()
        return [ents[ent].geoItem.getSympy() for ent in ents if ent!=None]
# ##########################################  CLASS STATUSBUTTON
# ##########################################################
# ##########################################################
# ##########################################################

class statusButton(QtWidgets.QToolButton):
    def __init__(self, icon=None,  tooltip=None):
        super(statusButton, self).__init__()
        self.setCheckable(True)
        self.setFixedSize(30, 20)
        if icon:
            self.getIcon(icon)
        self.setToolTip(tooltip)
    def getIcon(self, fileName):
        iconpath=os.path.join(os.getcwd(), 'icons', fileName)
        self.setIcon(QtGui.QIcon(iconpath))
    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            self.click()
        elif event.button()==QtCore.Qt.RightButton:
            self.showMenu()
