#@+leo-ver=5-thin
#@+node:1.20130426141258.3691: * @file cmdaction.py
'''
Created on May 12, 2010

@author: gertwin
'''

#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3692: ** <<declarations>> (cmdaction)
# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3693: ** class CmdAction
class CmdAction(QtGui.QAction):
    '''
    Derived action class to hold a command name.
    The FunctionHandler class handles signals emitted by this class.
    '''
    #@+others
    #@+node:1.20130426141258.3694: *3* __init__
    def __init__(self, command, icon, text, parent, function_handler):
        '''
        Parameters:
            command: name of the command.
            function_handler: reference to the function_handler object. 
        '''
        if not icon is None:
            super(CmdAction, self).__init__(icon, text, parent, triggered=self._actionHandler)
        else:
            super(CmdAction, self).__init__(text, parent, triggered=self._actionHandler)
        # command name
        self.__command = command
        # function handler
        self.__function_handler = function_handler
        # visible 
        self.__visible=True
        return
    #@+node:1.20130426141258.3695: *3* show
    def show(self):
        """
            show the command 
        """
        self.setEnabled(True)
    #@+node:1.20130426141258.3696: *3* hide
    def hide(self):
        """
            hide the command
        """
        self.setEnabled(False)
    #@+node:1.20130426141258.3697: *3* command
    @property   
    def command(self):
        """
            get the command name
        """
        return self.__command
    #@+node:1.20130426141258.3698: *3* _actionHandler
    def _actionHandler(self):
        '''
        All actions are handled by the function handler.
        From the function handler the command call-back is called.
        '''
        self.__function_handler.evaluate(self.__command)
        return
    #@-others
#@-others
#@-leo
