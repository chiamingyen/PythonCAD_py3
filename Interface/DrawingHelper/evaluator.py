#@+leo-ver=5-thin
#@+node:1.20130426141258.3864: * @file evaluator.py
#
# Copyright (c) ,2010 Matteo Boscolo
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
# evaluator Class to manage  command computation
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3865: ** <<declarations>> (evaluator)
from math import *
from Interface.pycadapp import PyCadApp
from sympy.physics import units as u

RESERVED_WORK=['self._print', 'self._error', 'self._ok','self._cadApplication','self.evaluate', 'self._eval', 'self._exec'  ]
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3866: ** class Evaluator
class Evaluator(object):
    #@+others
    #@+node:1.20130426141258.3867: *3* __init__
    def __init__(self, printFunction):
        self._print=printFunction
        self._error='*error*'
        self._ok='*Ok*'
        self._cadApplication=PyCadApp
    #@+node:1.20130426141258.3868: *3* evaluate
    def evaluate(self, value):
        """
            evaluate the string
        """
        if len(value)<=0:
            return None
        if value in RESERVED_WORK:
            if value.count(value):
                return self._error + "->Reserved word"
        if value[0]=='>': # eval
            return self._eval(value[1:])
        if value[0]=='@':
            return self._exec(value[1:])
        else:
            return value
    #@+node:1.20130426141258.3869: *3* _eval
    def _eval(self, value):
        """
            evaluate the evaluated value
        """
        try:
            return eval(value)
        except:
            return self._error
    #@+node:1.20130426141258.3870: *3* _exec
    def _exec(self, value):
        """
            exec value
        """
        try:
            value=str(value).replace('print', 'self._print')
            value=str(value).replace('pyCad', 'self._cadApplication')
            exec(value)
            return self._ok
        except:
            return self._error
    #@-others
#@-others
#@-leo
