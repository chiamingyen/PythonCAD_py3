#@+leo-ver=5-thin
#@+node:1.20130426141258.4003: * @file base.py
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
#
# This module provide basic class for all  the qtitems to be displayed
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.4004: ** <<declarations>> (base)
import sys
#if sys.version_info <(2, 7):
#    import sip
#    sip.setapi('QString', 2)
#    sip.setapi('QVariant', 2)

import math
from PyQt4  import QtCore, QtGui

from Kernel.initsetting         import PYTHONCAD_HIGLITGT_COLOR, PYTHONCAD_COLOR, MOUSE_GRAPH_DIMENSION

from Kernel.GeoEntity.point     import Point
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.4005: ** class BaseEntity
class BaseEntity(QtGui.QGraphicsItem):
    shapeSize=MOUSE_GRAPH_DIMENSION
    showShape=False #This Flag is used for debug porpoise
    showBBox=False  #This Flag is used for debug porpoise
    #@+others
    #@+node:1.20130426141258.4006: *3* __init__
    def __init__(self, entity):
        super(BaseEntity, self).__init__()
        self.setAcceptsHoverEvents(True)                        #Fire over events
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        #Get the geometry
        self._entity=entity
        self.setToolTip(str(self.toolTipMessage))
        #Set color from style
        r, g, b= self.style.getStyleProp("entity_color")
        color = QtGui.QColor.fromRgb(r, g, b)
        #set line thickness
        lineWith=self.style.getStyleProp("entity_thickness")
        #set line style
        penStyle=self.style.getStyleProp("entity_linetype")
        pen=QtGui.QPen(color)
        #TODO: Actually disable because the line with is not very nice
        #in the drawing ..
        #pen.setWidthF(float(lineWith))
        pen.setStyle(int(penStyle))
        self.pen=pen
        return
    #@+node:1.20130426141258.4007: *3* nearestSnapPoint
    def nearestSnapPoint(self, qtPointEvent, snapForceType=None, fromEntity=None):
        """
            compute the nearest point and return a qtPoint
        """
        pClick=Point(qtPointEvent.x(), qtPointEvent.y()*-1.0)
        ePoint=None
        for p in self.geoItem.getUpdatedSnapPoints(snapForceType, pClick,fromEntity):
            distance=p.dist(pClick)
            if ePoint==None:
                oldDistance=distance
                ePoint=p
            else:
                if oldDistance>distance:
                    oldDistance=distance
                    ePoint=p
        if ePoint==None:
            return qtPointEvent
        return QtCore.QPointF(ePoint.x, ePoint.y*-1.0)
    #@+node:1.20130426141258.4008: *3* entity
    @property
    def entity(self):
        return self._entity
    #@+node:1.20130426141258.4009: *3* ID
    @property
    def ID(self):
        return self._entity.getId()
    #@+node:1.20130426141258.4010: *3* geoItem
    @property
    def geoItem(self):
        return self._entity.toGeometricalEntity()
    #@+node:1.20130426141258.4011: *3* style
    @property
    def style(self):
        return self._entity.getInnerStyle()
    #@+node:1.20130426141258.4012: *3* toolTipMessage
    @property
    def toolTipMessage(self):
        toolTipMessage=self.geoItem.info
        return toolTipMessage
    #@+node:1.20130426141258.4013: *3* updateSelected
    def updateSelected(self):
        self.setColor()
        self.update(self.boundingRect())
        return
    #@+node:1.20130426141258.4014: *3* itemChange
    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            #self.setColor(value==1)
            self.update(self.boundingRect())
        return QtGui.QGraphicsItem.itemChange(self, change, value)
    #@+node:1.20130426141258.4015: *3* setColor
    def setColor(self, forceHilight=None):
        if forceHilight==None:
            if self.isSelected() or forceHilight:
                r, g, b=PYTHONCAD_HIGLITGT_COLOR
            else:
                r, g, b=self.style.getStyleProp("entity_color")
        else:
            if forceHilight:
                r, g, b=PYTHONCAD_HIGLITGT_COLOR
            else:
                r, g, b=self.style.getStyleProp("entity_color")
        color = QtGui.QColor.fromRgb(r, g, b)
        self.pen.setColor(color)
        return
    #@+node:1.20130426141258.4016: *3* setHiglight
    def setHiglight(self):
        r, g, b=PYTHONCAD_HIGLITGT_COLOR
        color = QtGui.QColor.fromRgb(r, g, b)
        self.pen.setColor(color)
        return
    #@+node:1.20130426141258.4017: *3* hoverEnterEvent
    def hoverEnterEvent(self, event):
        self.setHiglight()
        super(BaseEntity, self).hoverEnterEvent(event)
        return
    #@+node:1.20130426141258.4018: *3* hoverLeaveEvent
    def hoverLeaveEvent(self, event):
        self.setColor()
        super(BaseEntity, self).hoverLeaveEvent(event)
        return
    #@+node:1.20130426141258.4019: *3* drawGeometry
    def drawGeometry(self, painter, option, widget):
        """
             this method must be inerit from qtPycadObject
        """
        pass
    #@+node:1.20130426141258.4020: *3* drawShape
    def drawShape(self, painterPath):
        """
            overloading of the shape method
        """
        pass
    #@+node:1.20130426141258.4021: *3* shape
    def shape(self):
        """
            overloading of the shape method
        """
        painterStrock=QtGui.QPainterPathStroker()
        path=QtGui.QPainterPath()
        self.drawShape(path)
        painterStrock.setWidth(self.shapeSize)
        path1=painterStrock.createStroke(path)
        return path1
    #@+node:1.20130426141258.4022: *3* paint
    def paint(self, painter,option,widget):
        """
            overloading of the paint method
        """
        #draw geometry
        if self.showShape:
            r, g, b= PYTHONCAD_COLOR["cyan"]
            painter.setPen(QtGui.QPen(QtGui.QColor.fromRgb(r, g, b)))
            painter.drawPath(self.shape())

        if self.showBBox:
            r, g, b= PYTHONCAD_COLOR["darkblue"]
            painter.setPen(QtGui.QPen(QtGui.QColor.fromRgb(r, g, b)))
            painter.drawRect(self.boundingRect())

        painter.setPen(self.pen)
        self.drawGeometry(painter,option,widget)
        return
    #@+node:1.20130426141258.4023: *3* getDistance
    def getDistance(self, qtPointF_1, qtPointF_2):
        """
            calculate the distance betwing the two line
        """
        x=abs(qtPointF_1.x()-qtPointF_2.x())
        y=abs(qtPointF_1.y()- qtPointF_2.y())
        return math.sqrt(x**2+y**2)
    #@+node:1.20130426141258.4024: *3* boundingRect
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        return self.shape().boundingRect()
    #@-others
#@-others
#@-leo
