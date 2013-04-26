#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.2470: * @file pythoncad_qt.py
#@@first

#
# This is only needed for Python v2 but is harmless for Python v3.
#




#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.2471: ** <<declarations>> (pythoncad_qt)
import sys
#if sys.version_info <(2, 7):
#    try:
#        import sip
#        sip.setapi('QString', 2)
#        sip.setapi('QVariant', 2)
#    except:
#        pass
    
#
from PyQt4 import QtCore, QtGui
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
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.2472: ** getPythonCAD
#
def getPythonCAD():

    app = QtGui.QApplication(sys.argv)
    # splashscreen
    splashPath=os.path.join(os.getcwd(), 'icons', 'splashScreen1.png')
    splash_pix = QtGui.QPixmap(splashPath)
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    
    w=CadWindowMdi()
    w.show()
    
    # end splashscreen
    splash.finish(w)
    return w, app
#@-others
#
if __name__ == '__main__':
    w,app=getPythonCAD()
    sys.exit(app.exec_())
#@-leo
