#@+leo-ver=5-thin
#@+node:1.20130426141258.3871: * @file polarguides.py
#
# Copyright (c) 2010 Matteo Boscolo, Carlo Pavan
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
# This Module provide a polar guides management for the drawing scene and icommand
# 
#



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3872: ** <<declarations>> (polarguides)
import math

from PyQt4 import QtCore, QtGui
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3873: ** getPolarMenu
def getPolarMenu():
    '''
    returns a menu to operate with guide objects STILL TO BE IMPLEMENTED
    '''
    menu=QtGui.QMenu()
    
    return menu
#@+node:1.20130426141258.3874: ** class GuideHandler
class GuideHandler(QtGui.QGraphicsItem):
    '''
    This class provide management of a guide Handler to be instanced by the scene
    on startup, and to be placed by iCommand when a point is succesfully added to a command
    '''
    #@+others
    #@+node:1.20130426141258.3875: *3* __init__
    def __init__(self, parent, x, y, a):
        super(GuideHandler, self).__init__()
        self.scene=parent
        
        self.x=x
        self.y=y
        self.a=a
        
        self.guides=[]
        
        self.addGuidesByIncrement(math.pi/6)
    #@+node:1.20130426141258.3876: *3* collidesWithItem
    def collidesWithItem(self,other,mode):
        return False
    #@+node:1.20130426141258.3877: *3* setForceDirection
    def setForceDirection(self, a):
        '''
        set scene.forceDirection to a angle
        '''
        self.scene.forceDirection=a
    #@+node:1.20130426141258.3878: *3* setIsGuided
    def setIsGuided(self, bool):
        '''
        set scene.isGuided to bool value
        '''
        self.scene.isGuided=bool
    #@+node:1.20130426141258.3879: *3* setIsGuidLocked
    def setIsGuidLocked(self, bool):
        '''
        set scene.isGuideLocked to bool value
        '''
        self.scene.isGuideLocked=bool
    #@+node:1.20130426141258.3880: *3* addGuideByAngle
    def addGuideByAngle(self, a):
        '''
        add guide by a angle
        '''
        Guide(self, a)
        self.guides.append(a)
    #@+node:1.20130426141258.3881: *3* addGuidesByIncrement
    def addGuidesByIncrement(self, a=math.pi/2):
        '''
        add guides by a increment angle
        '''
        self.clearGuides()
        Guide(self, 0.0)
        i=0.0
        while i<math.pi*2:
            g=Guide(self, i)
            self.guides.append(g)
            i=i+a
        return
    #@+node:1.20130426141258.3882: *3* clearGuides
    def clearGuides(self):
        '''
        delete all guides   STILL DOESN'T WORK HELPPPPPPPPPPPPPPPPPPPPP
        '''
        for i in self.childItems():
            i.kill()
    #@+node:1.20130426141258.3883: *3* place
    def place(self, x, y):
        '''
        set position of the handler (called by icommand)
        '''
        self.setPos(x, y*-1)
    #@+node:1.20130426141258.3884: *3* reset
    def reset(self):
        '''
        reset position of the handler and hides it
        '''
        try:
            self.scene.forceDirection=None
            self.setPos(0.0, 0.0)
            self.hide()
        except:
            return
    #@+node:1.20130426141258.3885: *3* hideGuides
    def hideGuides(self):
        '''
        hides every guide children
        '''
        for i in self.childItems():
            i.hide()
    #@+node:1.20130426141258.3886: *3* boundingRect
    def boundingRect(self):
        return self.childrenBoundingRect()
    #@+node:1.20130426141258.3887: *3* paint
    def paint(self, painte, option, widget):
        return
    #@-others
#@+node:1.20130426141258.3888: ** class Guide
class Guide(QtGui.QGraphicsLineItem):
    '''
    This class provide a guide object and it's management
    it's added to the GuideHandler object
    '''
    #@+others
    #@+node:1.20130426141258.3889: *3* __init__
    def __init__(self, parent=None, a=0.0):
        super(Guide, self).__init__(parent)
        self.handler=parent
        #Flags
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations, True)
        self.setAcceptsHoverEvents(True)
        #Events
        
        self.a=parent.a+a
        line=QtCore.QLineF(0.0, 0.0, 20000*math.cos(a), (20000*math.sin(a))*-1)
        self.setLine(line)
        self.setToolTip("Guide [Press Shift to lock direction] "+ str(self.a)+"rad")
        
        self.highlightPen=QtGui.QPen(QtGui.QColor(150, 150, 150, 255), 1, QtCore.Qt.DotLine)
        self.hidePen=QtGui.QPen(QtGui.QColor(255, 50, 50, 0),1, QtCore.Qt.DotLine)
        
        self.setPen(self.hidePen)
        self.hide()
    #@+node:1.20130426141258.3890: *3* collidesWithItem
    def collidesWithItem(self,other,mode):
        return False
    #@+node:1.20130426141258.3891: *3* hide
    def hide(self):
        self.setPen(self.hidePen)
        self.handler.setForceDirection(None)
        self.handler.setIsGuided(None)
    #@+node:1.20130426141258.3892: *3* kill
    def kill(self):
        
        del self
    #@+node:1.20130426141258.3893: *3* shape
    def shape(self):
        x=self.pos().x()
        y=self.pos().y()
        P1=QtCore.QPointF(x+10*math.cos(self.a-0.4), y-10*math.sin(self.a-0.4))
        P2=QtCore.QPointF(x+20000*math.cos(self.a-0.03), y-20000*math.sin(self.a-0.03))
        P3=QtCore.QPointF(x+20000*math.cos(self.a+0.03), y-20000*math.sin(self.a+0.03))
        P4=QtCore.QPointF(x+10*math.cos(self.a+0.4), y-10*math.sin(self.a+0.4))
        poly=QtGui.QPolygonF([P1, P2, P3, P4])
        #self.handler.scene.addPolygon(poly) #this is for checking the design of snapping guides
        shp=QtGui.QPainterPath()
        shp.addPolygon(poly)
        return shp
        
        return shp
    #@+node:1.20130426141258.3894: *3* hoverEnterEvent
    def hoverEnterEvent(self, event):
        if self.handler.scene.isGuideLocked==None:
            self.handler.hideGuides()
            self.setPen(self.highlightPen)
            self.handler.setForceDirection(self.a)
            self.handler.setIsGuided(True)
        super(Guide, self).hoverEnterEvent(event)
        return
    #@+node:1.20130426141258.3895: *3* hoverLeaveEvent
    def hoverLeaveEvent(self, event):
        if self.handler.scene.isGuideLocked==None:
            self.hide()
            #self.update(self.boundingRect())
        super(Guide, self).hoverLeaveEvent(event)
    #@-others
#@-others
#@-leo
