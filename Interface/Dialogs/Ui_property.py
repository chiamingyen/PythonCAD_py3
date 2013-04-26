#@+leo-ver=5-thin
#@+node:1.20130426141258.3837: * @file Ui_property.py
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\OmniaSolutions\Programming\EclipseWorkSpace\PythonCad\PythonCAD\Interface\Dialogs\property.ui'
#
# Created: Mon Apr 23 17:27:00 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3838: ** <<declarations>> (Ui_property)
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3839: ** class Ui_Dialog
class Ui_Dialog(object):
    #@+others
    #@+node:1.20130426141258.3840: *3* setupUi
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(254, 279)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.propertyConteiner = QtGui.QVBoxLayout()
        self.propertyConteiner.setObjectName(_fromUtf8("propertyConteiner"))
        self.verticalLayout.addLayout(self.propertyConteiner)
        spacerItem = QtGui.QSpacerItem(20, 178, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.customProperty = QtGui.QTableView(self.tab_2)
        self.customProperty.setObjectName(_fromUtf8("customProperty"))
        self.verticalLayout_3.addWidget(self.customProperty)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    #@+node:1.20130426141258.3841: *3* retranslateUi
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "Geometrical Attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Custom Property", None, QtGui.QApplication.UnicodeUTF8))
    #@-others
#@-others
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
#@-leo
