#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:1.20130426141258.4140: * @file factory.py
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
# This module provide a factory for the preview objects
#




#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.4141: ** <<declarations>> (factory)
from Kernel.Command.pointcommand        import PointCommand
from Kernel.Command.segmentcommand      import SegmentCommand
from Kernel.Command.arccommand          import ArcCommand
from Kernel.Command.circlecommand       import CircleCommand
from Kernel.Command.rectanglecommand    import RectangleCommand
from Kernel.Command.ellipsecommand      import EllipseCommand
from Kernel.Command.polylinecommand     import PolylineCommand
from Kernel.Command.polygoncommand      import PolygonCommand

from Interface.Preview.point        import PreviewPoint
from Interface.Preview.segment      import PreviewSegment
from Interface.Preview.arc          import PreviewArc
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4142: ** getPreviewObject
#from Interface.Preview.rectangle    import QtRectangleItem
#from Interface.Preview.ellipse      import QtEllipseItem
#from Interface.Preview.polyline     import QtPolylineItem
#from Interface.Preview.polygon      import QtPolygonItem

def getPreviewObject(command):
    if isinstance(command , PointCommand):
        return PreviewPoint(command)
    if isinstance(command , SegmentCommand):
        return PreviewSegment(command)
    elif isinstance(command , (ArcCommand,CircleCommand)):
        return PreviewArc(command)
#    elif isinstance(command , RectangleCommand):
#        return QtRectangleItem(command)
#    elif isinstance(command , EllipseCommand):
#        return QtEllipseItem(command)
#    elif isinstance(command , PolylineCommand):
#        return QtPolylineItem(command)
#    elif isinstance(command ,  PolygonCommand):
#        return QtPolygonItem(command)
    else:
        return None
#@-others
#@-leo
