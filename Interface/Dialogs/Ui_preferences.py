#@+leo-ver=5-thin
#@+node:1.20130426141258.3832: * @file Ui_preferences.py
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\OmniaSolutions\Programming\EclipseWorkSpace\PythonCad\PythonCAD\Interface\Dialogs\preferencies.ui'
#
# Created: Tue Apr 24 08:38:50 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3833: ** <<declarations>> (Ui_preferences)
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3834: ** class Ui_preferences
class Ui_preferences(object):
    #@+others
    #@+node:1.20130426141258.3835: *3* setupUi
    def setupUi(self, preference):
        preference.setObjectName(_fromUtf8("preference"))
        preference.setWindowModality(QtCore.Qt.ApplicationModal)
        preference.resize(305, 234)
        self.verticalLayout = QtGui.QVBoxLayout(preference)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(preference)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(preference)
        QtCore.QMetaObject.connectSlotsByName(preference)
    #@+node:1.20130426141258.3836: *3* retranslateUi
    def retranslateUi(self, preference):
        preference.setWindowTitle(QtGui.QApplication.translate("preference", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
    #@-others
#@-others
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    preference = QtGui.QDialog()
    ui = Ui_preference()
    ui.setupUi(preference)
    preference.show()
    sys.exit(app.exec_())
#@-leo
