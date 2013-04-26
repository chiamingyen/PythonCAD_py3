#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.3749: * @file distance2point.py
#@@first

#
# Copyright (c) 2010 Matteo Boscolo
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
# This module provide a command to calculate the distance from 2 point
#





#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3750: ** <<declarations>> (distance2point)
import math

from Kernel.exception                  import *
from Kernel.Command.basecommand        import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3751: ** class Distance2Point
class Distance2Point(BaseCommand):
    """
        This class rappresent the distance 2 point command
    """
    #@+others
    #@+node:1.20130426141258.3752: *3* __init__
    def __init__(self, document, iDocument):
        BaseCommand.__init__(self, document)
        self.iDocuemnt=iDocument
        self.exception=[ExcPoint, ExcPoint]
        self.defaultValue=[None, None]
        self.message=["Give Me the first Point", 
                        "Give Me the second Point"]
    #@+node:1.20130426141258.3753: *3* applyCommand
    def applyCommand(self):
        if len(self.value)<1:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        leng=self.value[0].dist(self.value[1])
        msg="Lenght: "+ str(leng)
        self.iDocuemnt.popUpInfo(msg)
    #@-others
#@-others
#@-leo
