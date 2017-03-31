# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\OmniaSolutions\Programming\EclipseWorkSpace\PythonCad\PythonCAD\Interface\Dialogs\preferencies.ui'
#
# Created: Tue Apr 24 08:38:50 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!




from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_preferences(object):
    def setupUi(self, preference):
        preference.setObjectName("preference")
        preference.setWindowModality(QtCore.Qt.ApplicationModal)
        preference.resize(305, 234)
        self.verticalLayout = QtWidgets.QVBoxLayout(preference)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(preference)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(preference)
        QtCore.QMetaObject.connectSlotsByName(preference)
    def retranslateUi(self, preference):
        preference.setWindowTitle(QtCore.QCoreApplication.translate("preference", "Preferences", None))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    preference = QtWidgets.QDialog()
    ui = Ui_preference()
    ui.setupUi(preference)
    preference.show()
    sys.exit(app.exec_())
