#@+leo-ver=5-thin
#@+node:1.20130426141258.3754: * @file icommand.py
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
# This Module provide a Interface Command managing the preview the and the snap
# system
#
# How it works:
#


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3755: ** <<declarations>> (icommand)
import logging
#
#Kernel Import
#
from Kernel.GeoUtil.intersection    import *
from Kernel.pycadevent              import *
from Kernel.exception               import *
from Kernel.unitparser              import *
#
# Interface Import
#
from Interface.cadinitsetting       import RESTART_COMMAND_OPTION
from Interface.Dialogs.property     import Property
from Interface.Preview.factory      import *
from Interface.DrawingHelper.snap   import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3756: ** class ICommand
class ICommand(object):
    """
        this class provide base command operation
    """
    #self.scene.snappingPoint.activeSnap=SNAP_POINT_ARRAY["LIST"]  # Define the active snap system
    drawPreview=True                    # Enable the preview system
    automaticApply=True                 # Apply the command at the last insert value
    #@+others
    #@+node:1.20130426141258.3757: *3* __init__
    #restartCommandOption=False         # moved to Interface.cadinitsetting  > RESTART_COMMAND_OPTION

    def __init__(self, scene):
        self._scene=scene              # This is needed for the preview creation
        self._previewItem=None
        self._point={}
        self._entity={}
        self._distance={}
        self._angle={}
        self._snap={}
        self._forceSnap={}
        self._index=-1
        self.updateInput=PyCadEvent()
        #self.scene.snappingPoint.activeSnap=#SNAP_POINT_ARRAY["LIST"]  # Define the active snap system
    #@+node:1.20130426141258.3758: *3* forceDirection
    @property
    def forceDirection(self):
        """
            get scene force direction
        """
        return self.scene.forceDirection
    #@+node:1.20130426141258.3759: *3* kernelCommand
    @property
    def kernelCommand(self):
        """
            get scene the kernel command
        """
        return self.scene.activeKernelCommand
    #@+node:1.20130426141258.3760: *3* scene
    @property
    def scene(self):
        """
            get scene
        """
        return self._scene
    #@+node:1.20130426141258.3761: *3* index
    @property
    def index(self):
        return self._index
    #@+node:1.20130426141258.3762: *3* restartCommand
    def restartCommand(self):
        """
            reuse the command
        """
        if self.kernelCommand!=None:
            self.kernelCommand.reset()
        self._point={}
        self._entity={}
        self._distance={}
        self._angle={}
        self._snap={}
        self._forceSnap={}
        self._index=-1
        self.removePreviewItemToTheScene()
    #@+node:1.20130426141258.3763: *3* addMauseEvent
    def addMauseEvent(self, point, entity,distance=None,angle=None , text=None, force=None, correct=True):
        """
            add value to a new slot of the command
        """
        #
        # Compute snap distance and position force
        #
        logging.debug("log: addMauseEvent [%s][%s][%s][%s][%s][%s]"%( str(point), str(entity), str(distance), str(angle), str(text), str(force)))
        if correct!=None:
            snap=self.scene.snappingPoint.getSnapPoint(point,self.getEntity(point))
            snap=self.correctPositionForcedDirection(snap, self._scene.forceDirection)
        else:
            snap=point
            
        if angle==None:
            angle=self.calculateAngle(snap)
            
        if distance==None:
            distance=self.getDistance(snap)
        #
        # Assing value to the object arrays
        #
        try:
            self.kernelCommand[self._index]=(snap,entity,distance, angle, text) #Here you got all the magic
            self.scene.fromPoint=snap
            if self.kernelCommand.activeException()==ExcPoint or self.kernelCommand.activeException()==ExcLenght:
                if snap!=None:
                    self.scene.GuideHandler.place(snap.getx(), snap.gety())
                if self.scene.forceDirectionEnabled==True:
                    self.scene.GuideHandler.show()
        except Exception as ex:
            self.updateInput("msg")
            self.updateInput(self.kernelCommand.activeMessage)
            self.scene.clearSelection()
            print("Error ",str(ex))
            return
        self._index+=1
        self._point[self._index]=(point)
        self._entity[self._index]=(entity)
        self._distance[self._index]=(distance)
        self._angle[self._index]=(angle)
        self._snap[self._index]=(snap)
        self._forceSnap[self._index]=(force)
        #self.updatePreview(point,distance,entity )
        try:
            next(self.kernelCommand)
        except StopIteration:
            self.applyCommand()
            return

        self.updateInput(self.kernelCommand.activeMessage)
        if self.automaticApply and self.kernelCommand.automaticApply:
            if(self._index>=self.kernelCommand.lenght-1): #Apply the command
                self.applyCommand()

        if self.kernelCommand.activeException()==ExcDicTuple:
            dialog=Property(parent =self.scene.parent(),  entity=entity)
            if dialog.changed:
                self.kernelCommand[self._index]=(None,entity,None, None, dialog.value)
                self.applyCommand()
            else:
                self.restartCommand()
    #@+node:1.20130426141258.3764: *3* addTextEvent
    def addTextEvent(self, value):
        """
            compute imput from text
        """
        if str(value)=="":
            self.kernelCommand.applyDefault()
            self.applyCommand()
            return
        elif str(value).upper()=="UNDO":
            #TODO: perform a back operation to the command
            return
        elif str(value).upper()=="REDO":
            #TODO: perform a forward operation to the command
            return
        else:
            try:
                tValue=self.decodeText(str(value))
                self.addMauseEvent(tValue[0], tValue[1], tValue[2], tValue[3], tValue[4], correct=None)
            except PyCadWrongImputData as msg:
                print("Problem on ICommand.addTextEvent")
                self.updateInput(msg)
                self.updateInput(self.kernelCommand.activeMessage)
                return
    #@+node:1.20130426141258.3765: *3* applyDefault
    def applyDefault(self):
        """
            apply the default value command
        """
        try:
            self.kernelCommand.performDefaultValue()
            next(self.kernelCommand)
            self.updateInput(self.kernelCommand.activeMessage)
        except NoDefaultValue:
            return
        except StopIteration:
                self.applyCommand()
                return
    #@+node:1.20130426141258.3766: *3* applyCommand
    def applyCommand(self):
        """
            apply the command
        """
        self.scene.hideSnapMarks()
        try:
            self.kernelCommand.applyCommand()
            if RESTART_COMMAND_OPTION and self.kernelCommand.autorestart:
                    self.restartCommand()
                    self.updateInput(self.kernelCommand.activeMessage)
                    self.scene.clearSelection()
                    self.scene.fromPoint=None
                    self.scene.isGuided=None
                    self.scene.isGuideLocked=None
                    self.scene.GuideHandler.reset()
            else:
                self.scene.cancelCommand()
                self.updateInput("Ready")
                self.scene.clearPreview()
                self.removePreviewItemToTheScene()
                self=None
                return
            self.scene.clearPreview()
            self.removePreviewItemToTheScene()
        except Exception as e:
            print(type(e))     # the exception instance
            print("ICommand applyCommand Errore ", str(e))
            self.restartCommand()
    #@+node:1.20130426141258.3767: *3* getEntity
    def getEntity(self, position):
        """
            get the entity nearest at the mouse position
        """
        if position ==None:
            return None
        p=QtCore.QPointF(position.x, position.y*-1.0)
        ents=self._scene.items(p)
        if len(ents)>1: # bug: it was 0
            #TODO: here it will be nice to have a sort of control for chosing one entity
            #in case of overlapping entity selection
            pass
        for e in ents:
            if isinstance(e, BaseEntity):
                return e
        return None
    #@+node:1.20130426141258.3768: *3* updateMauseEvent
    def updateMauseEvent(self, point, entity, distance=None, force=None):
        """
            update value to the active slot of the command
        """
        if self.index>-1:
            updIndex=self.index+1
            self._point[updIndex]=point
            self._entity[updIndex]=entity
            
            if distance==None:
                distance=self.getDistance(point) 
            
            self._distance[updIndex]=distance
            self._snap[updIndex]=point
            self._forceSnap[updIndex]=force
        self.updatePreview(point, distance, entity) #   mange preview
    #@+node:1.20130426141258.3769: *3* getDistance
    def getDistance(self, point):
        """
            Get The distance from 2 points
        """
        prPoint=self.getActiveSnapClick()
        if prPoint!=None and point!=None:
            d=prPoint.dist(point)
            return d
        else:
            return None
    #@+node:1.20130426141258.3770: *3* calculateAngle
    def calculateAngle(self, snap):
        """
            calculate the angle betwin the point clicked
        """
        if snap==None:
            return None
        try:
            for snapPoint in self._snap:
                print("angle ",self._snap[snapPoint],snap) 
                v=Vector(self._snap[snapPoint],snap )
                return v.absAng
            else:
                return None
        except EntityMissing:
            return None
    #@+node:1.20130426141258.3771: *3* decodeText
    def decodeText(self, value):
        """
            encode the text given from the user
        """
        point=None
        distance=None
        entitys=None
        text=None
        angle=None
        value=str(value)
        
        def niceReturn():
            return (point,entitys, distance,angle, text)
        try:
            try:
                raise self.kernelCommand.activeException()(None)
            except ExcPoint:
                if value.find(',')>-1:              # ABSOLUTE CARTESIAN INPUT
                    x, y=value.split(',')
                    point=Point(convertLengh(x), convertLengh(y))
                    return niceReturn()
                elif value.find(';')>-1:            # RELATIVE CARTESIAN INPUT
                    x, y=value.split(';')
                    x=self.scene.fromPoint.getx()+convertLengh(x)
                    y=self.scene.fromPoint.gety()+convertLengh(y)
                    point=Point(x, y)
                    return niceReturn()
                elif value.find('>')>-1:
                    ang, distance=value.split('>')
                    ang=convertAngle(ang)
                    distance=convertLengh(distance)
                    x=math.cos(float(ang))*float(distance)
                    y=math.sin(float(ang))*float(distance)
                    x=self.scene.fromPoint.getx()+float(x)
                    y=self.scene.fromPoint.gety()+float(y)
                    point=Point(x, y)
                    return niceReturn()
                else: # DISTANCE+ANGLE FROM SCENE set coordinate based on distance input and angle from mouse position on the scene
                    d=float(value)
                    pX=self.scene.mouseOnSceneX
                    pY=self.scene.mouseOnSceneY
                    if self.scene.forceDirection is not None:
                        pc=Point(pX, pY)
                        pc=self.correctPositionForcedDirection(pc, self.scene.forceDirection)
                        pX, pY=pc.getCoords()
                    #if frompoint is not none else exception
                    dx=pX-self.scene.fromPoint.getx()
                    dy=pY-self.scene.fromPoint.gety()
                    a=math.atan2(dy, dx)
                    x=self.scene.fromPoint.getx()+d*math.cos(a)
                    y=self.scene.fromPoint.gety()+d*math.sin(a)
                    point=Point(x, y)
                    return niceReturn()
            except (ExcEntity,ExcMultiEntity):
                entitys=self.getIdsString(value)
                return niceReturn()
            except ExcEntityPoint:
                #(4@10,20)
                id, p=value.split('@')
                x, y=p.split(',')
                point=Point(float(x), float(y))
                entitys=self.getIdsString(id)
                return niceReturn()
            except (ExcLenght, ExcInt, ExcBool):
                distance=value
                return niceReturn()
            except(ExcAngle):
                angle=value
                return niceReturn()
            except(ExcText):
                text=value
                return niceReturn()
        except:
            raise PyCadWrongImputData("BaseCommand : Wrong imput parameter for the command")
        return niceReturn()
    #@+node:1.20130426141258.3772: *3* getIdsString
    def getIdsString(self, value):
        """
            return the entity from a string value (id)
        """
        return self.scene.getEntFromId(value)
    #@+node:1.20130426141258.3773: *3* updatePreview
    def updatePreview(self, point, distance, entity):
        """
            make update of the preview
        """
        if self.drawPreview:
            if self._previewItem==None:            #Create the Preview Item
                self._previewItem=getPreviewObject(self.kernelCommand)
                self.addPreviewItemToTheScene()
            else:                                   #Use the item already stored
                self._previewItem.updatePreview(point,
                                                distance,
                                                    self.kernelCommand)
    #@+node:1.20130426141258.3774: *3* addPreviewItemToTheScene
    def addPreviewItemToTheScene(self):
        """
            add the preview item at the scene
        """
        if self._previewItem!=None:
            self._scene.addItem(self._previewItem)
    #@+node:1.20130426141258.3775: *3* removePreviewItemToTheScene
    def removePreviewItemToTheScene(self):
        """
            Remove all the preview items from the scene
        """
        if self._previewItem!=None:
            self._scene.clearPreview()
            self._previewItem=None
    #@+node:1.20130426141258.3776: *3* getPointClick
    def getPointClick(self, index):
        """
            return the index clicked entity
        """
        return self.getDummyElement(self._point, index)
    #@+node:1.20130426141258.3777: *3* getEntityClick
    def getEntityClick(self, index):
        """
            return the index clicked entity
        """
        return self.getDummyElement(self._entity, index)
    #@+node:1.20130426141258.3778: *3* getDistanceClick
    def getDistanceClick(self, index):
        """
            return the index clicked entity
        """
        return self.getDummyElement(self._distance, index)
    #@+node:1.20130426141258.3779: *3* getSnapClick
    def getSnapClick(self, index):
        """
            return the index clicked entity
        """
        return self.getDummyElement(self._snap, index)
    #@+node:1.20130426141258.3780: *3* getForceSnap
    def getForceSnap(self, index):
        """
            return the index clicked entity
        """
        return self.getDummyElement(self._forceSnap, index)
    #@+node:1.20130426141258.3781: *3* getDummyElement
    def getDummyElement(self, array, index):
        """
            generic function to get an item from a generic array
        """
        if len(array)>=0 and index<=self.index:
            return array[index]
        raise IndexError
    #@+node:1.20130426141258.3782: *3* getDummyActive
    def getDummyActive(self, func):
        """
            parametric function to return an element of an array
        """
        if self.index>=0:
            return func(self.index)
        return None
    #@+node:1.20130426141258.3783: *3* getActiveSnapClick
    def getActiveSnapClick(self):
        """
            get the clicked snap point
        """
        return self.getDummyActive(self.getSnapClick)
    #@+node:1.20130426141258.3784: *3* getActiveDistanceClick
    def getActiveDistanceClick(self):
        """
            get the clicked distance
        """
        return self.getDummyActive(self.getDistanceClick)
    #@+node:1.20130426141258.3785: *3* getDummyBefore
    def getDummyBefore(self, func):
        """
            parametric function to return a previews element of an array
        """
        if self.index>0:
            return func(self.index-1)
        return None
    #@+node:1.20130426141258.3786: *3* getBeforeEntity
    def getBeforeEntity(self):
        """
            get the before clicked entity
        """
        return self.getDummyBefore(self.getEntityClick)
    #@+node:1.20130426141258.3787: *3* getBeforeSnapClick
    def getBeforeSnapClick(self):
        """
            get the before clicked snap point
        """
        return self.getDummyBefore(self.getSnapClick)
    #@+node:1.20130426141258.3788: *3* getLastForceSnap
    def getLastForceSnap(self):
        """
            get the before forced snap type
        """
        return self.getDummyBefore(self.getForceSnap)
    #@+node:1.20130426141258.3789: *3* correctPositionForcedDirection
    def correctPositionForcedDirection(self, point, force):
        """
            correct the POINT coords
            FORCE is the angle the defines the correction direction

            return the projection point of the POINT to the straight line defined by FORCE angle

            FORCE angle, in current inplementation, is setted by polarguides module when the mouse cursor is over a guide item
        """
        if point ==None:
            return None
        if force==None:
            return point
        lastSnap=self._scene.fromPoint
        pF=point
        if force!=None and lastSnap!=None:
            v=Vector(lastSnap, Point(lastSnap.x+10.0*math.cos(force),  lastSnap.y+10.0*math.sin(force)))
            v1=Vector(lastSnap,point)
            pF=v.map(v1.point).point
            pF=pF+lastSnap

#            if abs(x-lastSnap.x)>abs(y-lastSnap.y):
#                y=lastSnap.y
#            else:
#                x=lastSnap.x

        return pF #Point(x, y)
    #@+node:1.20130426141258.3790: *3* getIntersection
    def getIntersection(self, entity, point):
        """
            this function compute the  snap intersection point
        """
        returnVal=None
        distance=None
        if entity!=None:
            geoEntityFrom=entity.geoItem
            entityList=self._scene.collidingItems(entity)
            for ent in entityList:
                intPoint=find_intersections(ent.geoItem,geoEntityFrom)
                for tp in intPoint:
                    iPoint=Point(tp[0], tp[1])
                    if distance==None:
                        distance=iPoint.dist(point)
                        returnVal=iPoint
                    else:
                        spoolDist=iPoint.dist(point)
                        if distance>spoolDist:
                            distance=spoolDist
                            returnVal=iPoint
        return returnVal
    #@-others
#@-others
#@-leo
