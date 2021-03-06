#!/usr/bin/env python

import os, sys
#
from PyQt5 import QtCore, QtGui, QtWidgets
# 
import os
import sqlite3 as sqlite
#
# this is needed for me to use unpickle objects
#
sys.path.append(os.path.join(os.getcwd(), 'Generic'))
sys.path.append(os.path.join(os.getcwd(), 'Interface'))
#
from Interface.cadwindow    import CadWindowMdi
#
def getPythonCAD():

    app = QtWidgets.QApplication(sys.argv)
    # splashscreen
    splashPath=os.path.join(os.getcwd(), 'icons', 'splashScreen1.png')
    splash_pix = QtGui.QPixmap(splashPath)
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    
    w=CadWindowMdi()
    w.show()
    
    # end splashscreen
    splash.finish(w)
    return w, app
#
if __name__ == '__main__':
    w,app=getPythonCAD()
    sys.exit(app.exec_())
