#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.3738: * @file functionhandler.py
#@@first

#
# Copyright (c) 2010 Matteo Boscolo
# Copyright (c) 2010 Gertwin Geon
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
# This  module Provide custom exception for the db module and kernel
#





#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3739: ** <<declarations>> (functionhandler)
from Kernel.GeoEntity.point     import Point
from Kernel.GeoUtil.geolib      import Vector
from Kernel.pycadevent          import PyCadEvent
from Kernel.unitparser          import  convertLengh, convertAngle

from Interface.DrawingHelper.evaluator      import Evaluator
from Interface.Preview.factory              import getPreviewObject
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3740: ** class FunctionHandler
class FunctionHandler(object):
    '''
        This object contains all known commands.
        Commands are registered by "registerCommand" before the are available.
        Evaluation of commands or expressions is done by "evaluate"
    '''
    #@+others
    #@+node:1.20130426141258.3741: *3* __init__
    def __init__(self, edit_ctrl, edit_output):
        '''
            Defines an dictionary containing all known commands.
            Member 'registerCommand' add's a command to the table.
            Member 'evaluate' execute a command by call its call-back or evaluates an expression.
        '''
        # Input control
        self.__edit_ctrl = edit_ctrl
        # Output Control
        self.__edit_output=edit_output
        # current value
        self._value = None
        # command table
        self._command_table = {}
        # Global inner command evaluation
        self.evaluateInner=None
        #Evaluator
        self._eval=Evaluator(self.printCommand)
    #@+node:1.20130426141258.3742: *3* registerCommand
    def registerCommand(self, name, callback):
        '''
        Register a command with it's callback in the command table.
        Commands are executed by a call to the evaluate function.
        '''
        # a command is at least one character
        if len(name) > 0:
            # the callback is not None
            if not callback is None:
                # commands are always defined in upper case
                self._command_table[name.upper()] = callback
    #@+node:1.20130426141258.3743: *3* evaluate
    def evaluate(self, expression):
        '''
            Looks up the expression from the command table.
            If a command is found, it's callback function is called.
            If it is not a command the expression is evaluated.
            Return: command exit, the evaluated expression or "*error*"
        '''
        # commands are always defined in upper case
        command = str(expression).upper()
        # is it a command from the command table?
        self.__edit_ctrl.clear()
        if command in self._command_table:    # Interface command evaluation
            # call function
            # echo on the comand line
            self.printCommand(command)
            self._value = self._command_table[command]()
        else:
            try:
                # let python evaluate expression
                self.printCommand(expression)
                self._value=self._eval.evaluate(expression)
            except:
                self._value ="*error*"
            finally:
                self.__edit_ctrl.clear()
        # show result
        if self._value :
            self.printOutput(self._value)
        return self._value
    #@+node:1.20130426141258.3744: *3* resetCommand
    def resetCommand(self, reflect=True):
        """
            reset the command if eny are set
        """
        if reflect:
            self.printOutput("Command Ended from the user")
    #@+node:1.20130426141258.3745: *3* printCommand
    def printCommand(self, msg):
        """
            print message
        """
        msg=str(msg)
        if len(msg)>0:
            msg=">>> "+msg
            self.__edit_output.printMsg(msg)
    #@+node:1.20130426141258.3746: *3* printOutput
    def printOutput(self, msg):
        """
            print a message in the output message windows
        """
        msg=str(msg)
        if len(msg)>0:
            msg="<PythonCAD> : "+msg
            self.__edit_output.printMsg(msg)
    #@-others
#@-others
#@-leo
