#@+leo-ver=5-thin
#@+node:1.20130426141258.2473: * @file test_sympy.py
#encoding: utf-8


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.2474: ** <<declarations>> (test_sympy)
from pythoncad_qt import *
from sympy import *

w,app=getPythonCAD()
w.createSympyDocument()

p=Point(10, 10)
w.plotFromSympy([p])

w.getSympyObject()
#@-<<declarations>>
#@+others
#@-others
#@-leo
