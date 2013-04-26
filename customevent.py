#@+leo-ver=5-thin
#@+node:1.20130426141258.2396: * @file customevent.py
#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.2397: ** <<declarations>> (customevent)
from PyQt4 import QtCore, QtGui
from Kernel.document     import *
from Kernel.exception    import *
from Kernel.GeoEntity.point         import Point
from Kernel.Command.basecommand     import BaseCommand
from Interface.pycadapp             import PyCadApp
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.2398: ** class testCmdLine
class testCmdLine(object):
    #@+others
    #@+node:1.20130426141258.2399: *3* __init__
    def __init__(self, dialog, scene):
        self.dialog=dialog
        self.scene=scene
        self._addCustomEvent()
        self._inizializeCommand()
        self.activeCommand=None
    #@+node:1.20130426141258.2400: *3* _inizializeCommand
    def _inizializeCommand(self):    
        """
            inizialize all the command class
        """
        self.__command={}
        self.__applicationCommand={}
        self.__pyCadApplication=PyCadApp.Application()
        # Application Command
        self.__applicationCommand['Documents']=GetDocuments(self.__pyCadApplication.getDocuments(), self.outputMsg)
        self.__applicationCommand['CreateStyle']=CreateStyle(self.__pyCadApplication.ActiveDocument)
        #self.__applicationCommand['SetActiveDoc']=SetActiveDoc(self.__pyCadApplication)
        self.__applicationCommand['GetActiveDoc']=GetActiveDoc(self.__pyCadApplication, self.outputMsg)
        self.__applicationCommand['GetEnts']=GetEnts(self.__pyCadApplication.ActiveDocument, self.outputMsg)
        self.__applicationCommand['EntExsist']=EntityExsist(self.__pyCadApplication.ActiveDocument,self.outputMsg )
        self.__applicationCommand['Delete']=DeleteEntity(self.__pyCadApplication.ActiveDocument,self.outputMsg )
        self.__applicationCommand['UnDo']=UnDo(self.__pyCadApplication, self.outputMsg)
        self.__applicationCommand['ReDo']=ReDo(self.__pyCadApplication, self.outputMsg)
        self.__applicationCommand['T']=TestKernel(self.__pyCadApplication, self.outputMsg)
        self.__applicationCommand['ET']=EasyTest(self.__pyCadApplication, self.outputMsg)
        self.__applicationCommand['Info']=EntityInfo(self.__pyCadApplication.ActiveDocument, self.outputMsg)
        # Document Commandf
        for command in self.__pyCadApplication.getCommandList():
            self.__applicationCommand[command]=self.__pyCadApplication.getCommand(command)
        self.__applicationCommand['?']=PrintHelp(self.__applicationCommand, self.outputMsg)    
    #@+node:1.20130426141258.2401: *3* _addCustomEvent
    def _addCustomEvent(self):
        """
            add custom event at the user interface
        """
        QtCore.QObject.connect(self.dialog.ImputCmd, QtCore.SIGNAL("returnPressed()"),self.imputCommand)
        #QtCore.QObject.connect(self.dialog.uiTextEditor, QtCore.SIGNAL("textChanged()"),self.imputCommand)
        #QtCore.QObject.connect(self.uiTextEditor, QtCore.SIGNAL("textChanged()"), self.uiTextEditor.update)
    #@+node:1.20130426141258.2402: *3* imputCommand
    def imputCommand(self):
        """
            imput dialog
        """
        text=self.dialog.ImputCmd.text()
        self.outputMsg(">>> "+str(text))
        if self.activeCommand:
            try:
                if not self.performCommand(self.activeCommand, text):
                    self.activeCommand=None
                    #self.scene.populateScene(self.__pyCadApplication.ActiveDocument)
                else:
                    self.outputMsg(self.activeCommand.getActiveMessage())
            except:
                self.outputMsg("Unable to perfor the command")
                self.activeCommand=None
        else:
            cmdObject=None
            if text in self.__applicationCommand:
                cmdObject=self.__applicationCommand[text]
                cmdObject.reset()
                self.outputMsg(cmdObject.getActiveMessage())
            else:
                self.outputMsg('Command not avaiable write ? for command list')
            self.activeCommand=cmdObject
        self.dialog.ImputCmd.setText("")
    #@+node:1.20130426141258.2403: *3* performCommand
    def performCommand(self,cObject, text):
        """
            Perform a Command
            cObject is the command object
        """
        try:
            iv=next(cObject)
            exception,message=iv
            try:
                raise exception(None)
            except ExcPoint:
                cObject[iv]=self.convertToPoint(text)  
                return cObject
            except (ExcLenght, ExcAngle, ExcInt):
                cObject[iv]=self.convertToFloat(text)
                return cObject
            except (ExcBool):
                cObject[iv]=self.convertToBool(text)
                return cObject
            except (ExcText):
                cObject[iv]=text
                return cObject
            except (ExcEntity):
                cObject[iv]=self.convertToInt(text)
                return cObject
            except:
                msg="Error on command imput"
                self.outputMsg(msg)
                raise CommandException(msg)
            
        except (StopIteration):
            cObject.applyCommand()
            return None
        except PyCadWrongCommand:
            self.outputMsg("Wrong Command")
    #@+node:1.20130426141258.2404: *3* convertToBool
    def convertToBool(self, msg):   
        """
            return an int from user
        """        
        if msg=="Yes":
            return True
        else:
            return False
    #@+node:1.20130426141258.2405: *3* convertToInt
    def convertToInt(self, msg):   
        """
            return an int from user
        """        
        if msg:
            return int(msg)
        return None
    #@+node:1.20130426141258.2406: *3* convertToFloat
    def convertToFloat(self, msg):
        """
            return a float number
        """
        if msg:
            return float(msg)
        return None
    #@+node:1.20130426141258.2407: *3* convertToPoint
    def convertToPoint(self, msg):
        """
            ask at the user to imput a point 
        """
        if msg:
            coords=msg.split(',')
            x=float(coords[0])
            y=float(coords[1])
            return Point(x, y)
        return None
    #@+node:1.20130426141258.2408: *3* outputMsg
    def outputMsg(self, msg):   
        """
            print a message in to the self.dialog.uiTextEditor 
        """ 
        #self.dialog.uiTextEditor.moveCursor(QtGui.QTextCursor.Down)
        msg="\r<PythonCAD> : "+msg
        self.dialog.uiTextEditor.insertPlainText(msg)
    #@-others
#@+node:1.20130426141258.2409: ** printEntity
def printEntity(ents, msgFucntion):
        """
            print a query result
        """
        i=0
        for e in ents:
            msgFucntion("Entity Type %s id %s "%(str(e.eType),str(e.getId())))
            if i > 100:
                msgFucntion("There are more then 100 entitys in the select so i stop printing")
                break
            i+=1
#@+node:1.20130426141258.2410: ** class GetEnts
class GetEnts(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2411: *3* __init__
    def __init__(self, document, msgFucntion):
        BaseCommand.__init__(self, document)
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.outputMsg=msgFucntion
        self.exception=[ExcText]
        self.message=["Give Me the Document Type Enter for All"]
    #@+node:1.20130426141258.2412: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=1:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        docName=self.value[0]
        startTime=time.clock()
        if not docName:
            docName="ALL"
        ents=self.document.getEntityFromType(docName)
        endTime=time.clock()-startTime       
        printEntity(ents,self.outputMsg )
        self.outputMsg("Exec query get %s ent in %s s"%(str(len(ents)), str(endTime)))
        self.outputMsg("********************************")
    #@-others
#@+node:1.20130426141258.2413: ** class UnDo
class UnDo(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2414: *3* __init__
    def __init__(self, application, msgFunction):
        BaseCommand.__init__(self, None)
        self.__application=application
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[]
        self.message=["Press enter to perform the Undo command"]
        self.outputMsg=msgFunction
    #@+node:1.20130426141258.2415: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=0:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        doc=self.__application.ActiveDocument
        doc.unDo()
    #@-others
#@+node:1.20130426141258.2416: ** class ReDo
class ReDo(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2417: *3* __init__
    def __init__(self, application, msgFunction):
        BaseCommand.__init__(self, None)
        self.__application=application
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[]
        self.message=["Press enter to perform the ReDo command"]
        self.outputMsg=msgFunction
    #@+node:1.20130426141258.2418: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=0:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        doc=self.__application.ActiveDocument
        doc.reDo()
    #@-others
#@+node:1.20130426141258.2419: ** class GetActiveDoc
class GetActiveDoc(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2420: *3* __init__
    def __init__(self, application, msgFunction):
        BaseCommand.__init__(self, None)
        self.__application=application
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[]
        self.message=["Press enter to perform the command"]
        self.outputMsg=msgFunction
    #@+node:1.20130426141258.2421: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=0:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        docName=self.value[0]
        self.__application.ActiveDocument=docName
        doc=self.__application.ActiveDocument
        self.outputMsg("Active Document is %s"%str(doc.dbPath))
    #@-others
#@+node:1.20130426141258.2422: ** class SetActiveDoc
class SetActiveDoc(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2423: *3* __init__
    def __init__(self, application):
        BaseCommand.__init__(self, None)
        self.__application=application
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[ExcText]
        self.message=["Give Me the Document Name"]
    #@+node:1.20130426141258.2424: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=1:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        docName=self.value[0]
        self.__application.ActiveDocument=docName
    #@-others
#@+node:1.20130426141258.2425: ** class GetDocuments
class GetDocuments(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2426: *3* __init__
    def __init__(self, documents, msgFunction):
        BaseCommand.__init__(self, None)
        self.__docuemnts=documents
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[]
        self.message=["Press enter to perform the command"]
        self.outputMsg=msgFunction
    #@+node:1.20130426141258.2427: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=0:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        self.showDocuments()
    #@+node:1.20130426141258.2428: *3* showDocuments
    def showDocuments(self):
        """
            show The list of documents
        """
        try:
            self.outputMsg("Documents in the curret application")
            i=0
            for key in self.__docuemnts:
                self.outputMsg("%s File %s"%(str(i), str(key)))
                i+=1
            self.outputMsg("***********************************")
        except:
            self.outputMsg("Unable To Perform the GetDocuments") 
    #@-others
#@+node:1.20130426141258.2429: ** class CreateStyle
class CreateStyle(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2430: *3* __init__
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[ExcText]
        self.message=["Give Me the Style Name"]
    #@+node:1.20130426141258.2431: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=1:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        styleName=self.value[0]
        #self.inputMsg("Write style name")
        stl=Style(styleName)
        self.document.saveEntity(stl)
    #@-others
#@+node:1.20130426141258.2432: ** class EntityExsist
class EntityExsist(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2433: *3* __init__
    def __init__(self, document, msgFunction ):
        BaseCommand.__init__(self, document)
        self.outputMsg=msgFunction
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[ExcText]
        self.message=["Give me the entity id"]
    #@+node:1.20130426141258.2434: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=1:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        entId=self.value[0]
        #self.inputMsg("Write style name")
        if self.document.entityExsist(entId):
            self.outputMsg("Entity Found in the db")
        else:
            self.outputMsg("Entity Not Found")
    #@-others
#@+node:1.20130426141258.2435: ** class DeleteEntity
class DeleteEntity(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2436: *3* __init__
    def __init__(self, document, msgFunction ):
        BaseCommand.__init__(self, document)
        self.outputMsg=msgFunction
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[ExcText]
        self.message=["Give me the entity id"]
    #@+node:1.20130426141258.2437: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=1:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        entId=self.value[0]
        #self.inputMsg("Write style name")
        if self.document.entityExsist(entId):
            self.document.deleteEntity(entId)
    #@-others
#@+node:1.20130426141258.2438: ** class EntityInfo
class EntityInfo(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2439: *3* __init__
    def __init__(self, document, msgFunction ):
        BaseCommand.__init__(self, document)
        self.outputMsg=msgFunction
        self.exception=[ExcText]
        self.message=["Give me the entity id"]
    #@+node:1.20130426141258.2440: *3* applyCommand
    def applyCommand(self):
        if len(self.value)!=1:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        entId=self.value[0]
        if self.document.entityExsist(entId):
            ent=self.document.getEntity(entId)
            geoEnt=self.document.convertToGeometricalEntity(ent)
            self.outputMsg("Entity %s"%str(geoEnt))
        else:
            self.outputMsg("Wrong id Number")
    #@-others
#@+node:1.20130426141258.2441: ** class PrintHelp
class PrintHelp(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2442: *3* __init__
    def __init__(self, commandArray, msgFunction):
        BaseCommand.__init__(self, None)
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[]
        self.outputMsg=msgFunction
        self.message=["Print the help Press enter to ally the command "]
        self.commandNames=list(commandArray.keys())
    #@+node:1.20130426141258.2443: *3* __next__
    def __next__(self):    
        raise StopIteration
    #@+node:1.20130426141258.2444: *3* applyCommand
    def applyCommand(self):
        self.outputMsg("***********Command List******************")
        self.commandNames.sort()
        for s in self.commandNames:
            self.outputMsg(s)
    #@-others
#@+node:1.20130426141258.2445: ** class TestKernel
class TestKernel(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2446: *3* __init__
    def __init__(self, application, msgFunction):
        BaseCommand.__init__(self, None)
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[]
        self.outputMsg=msgFunction
        self.message=["Press enter to start the test"]
        self.__pyCadApplication=application
    #@+node:1.20130426141258.2447: *3* __next__
    def __next__(self):    
        raise StopIteration
    #@+node:1.20130426141258.2448: *3* applyCommand
    def applyCommand(self):
        self.outputMsg("*********** Start Test ******************")
        self.featureTest()
        self.outputMsg("*********** End   Test ******************")
    #@+node:1.20130426141258.2449: *3* featureTest
    def featureTest(self):
            """
                this function make a basic test
            """
            self.outputMsg("Create a new document 1")
            doc1=self.__pyCadApplication.newDocument()
            self.outputMsg("Create a new document 2")
            doc2=self.__pyCadApplication.newDocument()
            self.outputMsg("Set Current p1")
            self.__pyCadApplication.ActiveDocument=doc1
            self.outputMsg("Create Point")
            self.performCommandRandomly("POINT")
            self.outputMsg("Create Segment")
            self.performCommandRandomly("SEGMENT")
            self.outputMsg("Create Arc")
            self.performCommandRandomly("ARC")
            self.__pyCadApplication.ActiveDocument=doc2
            self.outputMsg("Create Ellipse")
            self.performCommandRandomly("ELLIPSE")
            self.outputMsg("Create Polyline")
            self.performCommandRandomly("POLYLINE")
            self.outputMsg("Create ACLine")
            self.performCommandRandomly("ACLINE")
            
            self.outputMsg("Get Entitys for doc 1")
            self.__pyCadApplication.ActiveDocument=doc1
            activeDoc=self.__pyCadApplication.ActiveDocument
            ents=activeDoc.getEntityFromType("ALL")
            self.printEntity(ents)
            self.outputMsg("Get Entitys for doc 2")
            self.__pyCadApplication.ActiveDocument=doc2
            activeDoc=self.__pyCadApplication.ActiveDocument
            ents=activeDoc.getEntityFromType("ALL")
            self.printEntity(ents)
            # Working with styles
            self.outputMsg("Create NewStyle")
            stl=Style("NewStyle")
            self.outputMsg("Save in document")
            activeDoc.saveEntity(stl)
            activeDoc.setActiveStyle(name='NewStyle')
            self.outputMsg("Create Segment")
            self.performCommandRandomly("SEGMENT")
            self.outputMsg("Create Arc")
            self.performCommandRandomly("ARC")
            
            self.outputMsg("Create NewStyle1")
            stl1=Style("NewStyle1")
            self.__pyCadApplication.setApplicationStyle(stl1)
            stl11=self.__pyCadApplication.getApplicationStyle(name='NewStyle1')
            styleDic=stl11.getConstructionElements()
            styleDic[list(styleDic.keys())[0]].setStyleProp('entity_color',(255,215,000))
            self.__pyCadApplication.setApplicationStyle(stl11)
            activeDoc.saveEntity(stl11)
            self.outputMsg("Create Segment")
            self.performCommandRandomly("SEGMENT")
            self.outputMsg("Create Arc")
            self.performCommandRandomly("ARC")
            
            self.outputMsg("Create NewStyle2 ")
            stl1=Style("NewStyle2")
            stl12=activeDoc.saveEntity(stl1)
            styleDic=stl11.getConstructionElements()
            styleDic[list(styleDic.keys())[0]].setStyleProp('entity_color',(255,215,000))
            self.outputMsg("Update NewStyle2")
            activeDoc.saveEntity(stl12)
            self.outputMsg("Done")
            # Test  Geometrical chamfer ent
            self.GeotestChamfer()
            # Test Chamfer Command 
            self.testChamferCommand()
    #@+node:1.20130426141258.2450: *3* testGeoChamfer
    def testGeoChamfer(self):    
        self.outputMsg("Test Chamfer")
        p1=Point(0.0, 0.0)
        p2=Point(10.0, 0.0)
        p3=Point(0.0, 10.0)
        
        s1=Segment(p1, p2)
        s2=Segment(p1, p3)
        
        cmf=Chamfer(es1.getId(), s2, 2.0, 2.0)
        cl=cmf.getLength()
        self.outputMsg("Chamfer Lengh %s"%str(cl))
        s1, s2, s3=cmf.getReletedComponent()
        if s3:
            for p in s3.getEndpoints():
                x, y=p.getCoords()
                self.outputMsg("P1 Cords %s,%s"%(str(x), str(y)))
        else:
            self.outputMsg("Chamfer segment in None")
    #@+node:1.20130426141258.2451: *3* testChamferCommand
    def testChamferCommand(self):
        """
            this function is usefoul for short test
            as soon it works copy the code into featureTest
        """
        newDoc=self.__pyCadApplication.newDocument()
        intPoint=Point(0.0, 0.0)
        
        s1=Segment(intPoint, Point(10.0, 0.0))
        s2=Segment(intPoint, Point(0.0, 10.0))
        
        ent1=newDoc.saveEntity(s1)
        ent2=newDoc.saveEntity(s2)
       
        cObject=self.__pyCadApplication.getCommand("CHAMFER")
        keys=list(cObject.keys())
        cObject[keys[0]]=ent1
        cObject[keys[1]]=ent2
        cObject[keys[2]]=2
        cObject[keys[3]]=2
        cObject[keys[4]]=None
        cObject[keys[5]]=None
        cObject.applyCommand()
    #@+node:1.20130426141258.2452: *3* getRandomPoint
    def getRandomPoint(self):
        """
            get e random point
        """
        x=random()*1000
        y=random()*1000
        return Point(x, y)
    #@+node:1.20130426141258.2453: *3* performCommandRandomly
    def performCommandRandomly(self, commandName, andLoop=10):
        """
            set some random Value at the command imput
        """
        self.outputMsg("Start Command %s"%str(commandName))
        i=0
        cObject=self.__pyCadApplication.getCommand(commandName)
        for iv in cObject:
            exception,message=iv
            try:
                raise exception(None)
            except ExcPoint:
                self.outputMsg("Add Point")
                if i>=andLoop:
                    cObject[iv]=None
                else:
                    cObject[iv]=self.getRandomPoint()
            except (ExcLenght, ExcAngle):
                self.outputMsg("Add Lengh/Angle")
                cObject[iv]=100
            except:
                self.outputMsg("Bad error !!")
                raise 
            i+=1
        else:
            self.outputMsg("Apply Command")
            cObject.applyCommand()
    #@-others
#@+node:1.20130426141258.2454: ** class EasyTest
class EasyTest(BaseCommand):
    #@+others
    #@+node:1.20130426141258.2455: *3* __init__
    def __init__(self, application, msgFunction):
        BaseCommand.__init__(self, None)
        #PyCadBaseCommand.__exception=[ExcPoint, ExcPoint]
        self.exception=[]
        self.outputMsg=msgFunction
        self.message=["Press enter to start the test"]
        self.__pyCadApplication=application
    #@+node:1.20130426141258.2456: *3* __next__
    def __next__(self):    
        raise StopIteration
    #@+node:1.20130426141258.2457: *3* applyCommand
    def applyCommand(self):
        self.outputMsg("*********** Start Test ******************")
        self.easyTest()
        
        #self.MassiveDelete()
        self.outputMsg("*********** End   Test ******************")    
    #@+node:1.20130426141258.2458: *3* MassiveDelete
    def MassiveDelete(self):
        try:
            import time 
            startTime=time.clock()
            newDoc=self.__pyCadApplication.ActiveDocument
            newDoc.startMassiveCreation()
            for i in range(1000):
                intPoint=Point(i, i)
                args={"SEGMENT_0":intPoint, "SEGMENT_1":Point(10.0, 0.0)}
                s1=Segment(args)    
                newDoc.saveEntity(s1)
            else:
                newDoc.performCommit()    
                newDoc.stopMassiveCreation()
                endTime=time.clock()-startTime
                print("Create 1000 entity in %s"%str(endTime))    
        finally:
            ents=newDoc.getAllDrawingEntity()
            ids=[ent.getId() for ent in ents]
            startTime=time.clock()
            newDoc.massiveDelete(ids)
            endTime=time.clock()-startTime
            print("Delete 1000 entity in %s"%str(endTime))    
    #@+node:1.20130426141258.2459: *3* easyTest
    def easyTest(self):
        """
            this function is usefoul for short test
            as soon it works copy the code into featureTest
        """
        newDoc=self.__pyCadApplication.ActiveDocument
        newDoc.startMassiveCreation()
        #self.testChamfer()
        #self.testFillet1()
        #self.testFillet2()
        #self.multitest()
        #self.testMirror()
        #self.testMove()
        #self.rotate()
        self.trim()
        newDoc.stopMassiveCreation()
    #@+node:1.20130426141258.2460: *3* trim
    def trim(self):    
        """
            test the trim command
        """
        newDoc=self.__pyCadApplication.ActiveDocument
        
        sArg1={"SEGMENT_0":Point(0, 0), "SEGMENT_1":Point(150, 0)}
        _st1=Segment(sArg1)
        newSeg1=newDoc.saveEntity(_st1)
        
        sArg2={"SEGMENT_0":Point(200, 0), "SEGMENT_1":Point(200, 150)}
        _st2=Segment(sArg2)
        newSeg2=newDoc.saveEntity(_st2)
        trimCmd=self.__pyCadApplication.getCommand('TRIM')
        
        keys=list(trimCmd.keys())
        trimCmd[keys[0]]=newSeg1.getId()
        trimCmd[keys[1]]=newSeg2.getId()
        trimCmd[keys[2]]=Point(140, 1)
        trimCmd[keys[3]]=Point(210, 1)
        trimCmd[keys[4]]="B"
        trimCmd.applyCommand() 
    #@+node:1.20130426141258.2461: *3* rotate
    def rotate(self):
        """
            perform a rotate operation
        """
        newDoc=self.__pyCadApplication.ActiveDocument
        ang=1.5707963267948966
        cp=Point(0, 0)
        newDoc.saveEntity(cp)
        #Point 
        centerPoint=Point(100,100)
        dbPointEnt=newDoc.saveEntity(centerPoint)
        centerPoint.rotate(cp, ang)
        dbPointEnt=newDoc.saveEntity(centerPoint)
        
        #Arc 
        centerPoint=Point(100, 100)
        arg={"ARC_0":centerPoint, "ARC_1":50, "ARC_2":0.78539816339500002,"ARC_3":1.5707963267948966}
        arc=Arc(arg)
        entArc=newDoc.saveEntity(arc)
        arc.rotate(cp,ang)
        entArc=newDoc.saveEntity(arc)
        
        #Segment
        sArg={"SEGMENT_0":Point(100, 100), "SEGMENT_1":Point(150, 150)}
        _st=Segment(sArg)
        newSeg=newDoc.saveEntity(_st)
        _st.rotate(cp, ang)
        newDoc.saveEntity(_st)
        #Ellipse
        eArg={"ELLIPSE_0":Point(100, 0), "ELLIPSE_1":100, "ELLIPSE_2":50}
        _e=Ellipse(eArg)
        newE=newDoc.saveEntity(_e)
        _e.rotate(cp, ang)
        newDoc.saveEntity(_e)
    #@+node:1.20130426141258.2462: *3* testMove
    def testMove(self):
        """
            perform a move operation
        """
        #Arc 
        newDoc=self.__pyCadApplication.ActiveDocument
        centerPoint=Point(100, 100)
        arg={"ARC_0":centerPoint, "ARC_1":50, "ARC_2":0.78539816339500002,"ARC_3":1.5707963267948966}
        arc=Arc(arg)
        entArc=newDoc.saveEntity(arc)
        
        sp=Point(0, 0)
        ep=Point(100, 100)
       
        arc.move(sp, ep)
        entArc=newDoc.saveEntity(arc)
        #Point 
        centerPoint=Point(100, 0)
        dbPointEnt=newDoc.saveEntity(centerPoint)
        centerPoint.move(sp, ep)
        dbPointEnt=newDoc.saveEntity(centerPoint)
        #Segment
        sArg={"SEGMENT_0":Point(100, 100), "SEGMENT_1":Point(150, 150)}
        _st=Segment(sArg)
        newSeg=newDoc.saveEntity(_st)
        _st.move(sp, ep)
        newDoc.saveEntity(_st)
        #Ellipse
        eArg={"ELLIPSE_0":Point(100, 0), "ELLIPSE_1":100, "ELLIPSE_2":50}
        _e=Ellipse(eArg)
        newE=newDoc.saveEntity(_e)
        _e.move(sp, ep)
        newDoc.saveEntity(_e)
    #@+node:1.20130426141258.2463: *3* testMirror
    def testMirror(self):    
        """
            perform a mirror operation of all the entity
        """
        #Arc mirror
        newDoc=self.__pyCadApplication.ActiveDocument
        centerPoint=Point(100, 100)
        arg={"ARC_0":centerPoint, "ARC_1":50, "ARC_2":0.78539816339500002,"ARC_3":1.5707963267948966}
        arc=Arc(arg)
        entArc=newDoc.saveEntity(arc)
        
        sArg={"SEGMENT_0":Point(-100, 0), "SEGMENT_1":Point(0, 100)}
        _s=Segment(sArg)
        
        mirrorSeg=newDoc.saveEntity(_s)
        arc.mirror(_s)
        entArc=newDoc.saveEntity(arc)
        #Point 
        centerPoint=Point(100, 0)
        dbPointEnt=newDoc.saveEntity(centerPoint)
        newcenterPoint=centerPoint.clone()
        newcenterPoint.mirror(_s)
        dbPointEnt=newDoc.saveEntity(newcenterPoint)
        #Segment
        sArg={"SEGMENT_0":Point(100, 100), "SEGMENT_1":Point(150, 150)}
        _st=Segment(sArg)
        newSeg=newDoc.saveEntity(_st)
        _st.mirror(_s)
        newDoc.saveEntity(_st)
        #Ellipse
        eArg={"ELLIPSE_0":Point(100, 0), "ELLIPSE_1":100, "ELLIPSE_2":50}
        _e=Ellipse(eArg)
        newE=newDoc.saveEntity(_e)
        _e.mirror(_s)
        newDoc.saveEntity(_e)
    #@+node:1.20130426141258.2464: *3* testFillet
    def testFillet(self, p1, p2, p3, pp1, pp2, R=100):
        newDoc=self.__pyCadApplication.ActiveDocument
        args={"SEGMENT_0":p1, "SEGMENT_1":p2}
        s1=Segment(args)
        args={"SEGMENT_0":p1, "SEGMENT_1":p3}
        s2=Segment(args)
        
        ent1=newDoc.saveEntity(s1)
        ent2=newDoc.saveEntity(s2)

        cObject=self.__pyCadApplication.getCommand("FILLET")
        keys=list(cObject.keys())
        cObject[keys[0]]=ent1
        cObject[keys[1]]=ent2
        cObject[keys[2]]=pp1
        cObject[keys[3]]=pp2
        cObject[keys[4]]="BOTH"
        cObject[keys[5]]=R
        cObject.applyCommand() 
    #@+node:1.20130426141258.2465: *3* testBisector
    def testBisector(self, p1, p2, p3, pp1, pp2, L=100):
        newDoc=self.__pyCadApplication.ActiveDocument
        args={"SEGMENT_0":p1, "SEGMENT_1":p2}
        s1=Segment(args)
        args={"SEGMENT_0":p1, "SEGMENT_1":p3}
        s2=Segment(args)
        
        ent1=newDoc.saveEntity(s1)
        ent2=newDoc.saveEntity(s2)
        
        cObject=self.__pyCadApplication.getCommand("BISECTOR")
        keys=list(cObject.keys())
        cObject[keys[0]]=ent1
        cObject[keys[1]]=ent2
        cObject[keys[2]]=pp1
        cObject[keys[3]]=pp2
        cObject[keys[4]]=L
        cObject.applyCommand()
    #@+node:1.20130426141258.2466: *3* multitest
    def multitest(self):    
        p1=Point(0, 0)
        p2=Point(10, 0)
        p3=Point(0, 10)
        pp1=Point(1, 0)
        pp2=Point(0, 3)
        self.testBisector(p1, p2, p3, pp1, pp2)
        self.testFillet(p1, p2, p3, pp1, pp2)
        
        p1=Point(0, 0)
        p2=Point(-10, 0)
        p3=Point(0, 10)
        pp1=Point(-1,  0)
        pp2=Point(0, 3)
        self.testBisector(p1, p2, p3, pp1, pp2)
        self.testFillet(p1, p2, p3, pp1, pp2)
        
        p1=Point(0, 0)
        p2=Point(-10, 0)
        p3=Point(0, -10)
        pp1=Point(-1, 0)
        pp2=Point(0, -3)
        self.testBisector(p1, p2, p3, pp1, pp2)
        self.testFillet(p1, p2, p3, pp1, pp2)        

        p1=Point(0, 0)
        p2=Point(10, 0)
        p3=Point(0, -10)
        pp1=Point(1, 0)
        pp2=Point(0, -3)
        self.testBisector(p1, p2, p3, pp1, pp2)   
        self.testFillet(p1, p2, p3, pp1, pp2)     
        
        p1=Point(100, 0)
        p2=Point(200, 0)
        p3=Point(200, 100)
        pp1=Point(110, -1)
        pp2=Point(112, 30)
        self.testBisector(p1, p2, p3, pp1, pp2)   
        self.testFillet(p1, p2, p3, pp1, pp2)

        p1=Point(100, 100)
        p2=Point(200, 0)
        p3=Point(200, 100)
        pp1=Point(110, -1)
        pp2=Point(112, 30)
        self.testBisector(p1, p2, p3, pp1, pp2, 30) 
        self.testFillet(p1, p2, p3, pp1, pp2, 30)   
    #@+node:1.20130426141258.2467: *3* testFillet1
    def testFillet1(self):
        newDoc=self.__pyCadApplication.ActiveDocument
        intPoint=Point(0.0, 0.0)
        args={"SEGMENT_0":intPoint, "SEGMENT_1":Point(10.0, 0.0)}
        s1=Segment(args)
        args={"SEGMENT_0":intPoint, "SEGMENT_1":Point(0.0, 10.0)}
        s2=Segment(args)
        
        ent1=newDoc.saveEntity(s1)
        ent2=newDoc.saveEntity(s2)
        
        cObject=self.__pyCadApplication.getCommand("FILLET")
        keys=list(cObject.keys())
        cObject[keys[0]]=ent1
        cObject[keys[1]]=ent2
        cObject[keys[2]]=Point(1, 0)
        cObject[keys[3]]=Point(0, 3)
        cObject[keys[4]]="BOTH"
        cObject[keys[5]]=4
        cObject.applyCommand()
    #@+node:1.20130426141258.2468: *3* testFillet2
    def testFillet2(self):    
        newDoc=self.__pyCadApplication.ActiveDocument
        intPoint=Point(0, 0)
        args={"SEGMENT_0":intPoint, "SEGMENT_1":Point(1000, 1000)}
        s1=Segment(args)
        args={"SEGMENT_0":intPoint, "SEGMENT_1":Point(1000, 0)}
        s2=Segment(args)
        
        ent1=newDoc.saveEntity(s1)
        ent2=newDoc.saveEntity(s2)
        
        cObject=self.__pyCadApplication.getCommand("FILLET")
        keys=list(cObject.keys())
        cObject[keys[0]]=ent1
        cObject[keys[1]]=ent2
        cObject[keys[2]]=Point(101, 0)
        cObject[keys[3]]=Point(0, 103)
        cObject[keys[4]]="NO_TRIM"
        cObject[keys[5]]=20
        cObject.applyCommand()

        cObject=self.__pyCadApplication.getCommand("FILLET")
        keys=list(cObject.keys())
        cObject[keys[0]]=ent1
        cObject[keys[1]]=ent2
        cObject[keys[2]]=Point(101, 0)
        cObject[keys[3]]=Point(0, 103)
        cObject[keys[4]]="NO_TRIM"
        cObject[keys[5]]=100
        cObject.applyCommand()        
        
        cObject=self.__pyCadApplication.getCommand("BISECTOR")
        keys=list(cObject.keys())
        cObject[keys[0]]=ent1
        cObject[keys[1]]=ent2
        cObject[keys[2]]=Point(101, 0)
        cObject[keys[3]]=Point(0, 103)
        cObject[keys[4]]=1000
        cObject.applyCommand()
    #@+node:1.20130426141258.2469: *3* testChamfer
    def testChamfer(self):
        newDoc=self.__pyCadApplication.ActiveDocument
        intPoint=Point(2.0, 2.0)
        args={"SEGMENT_0":intPoint, "SEGMENT_1":Point(10.0, 0.0)}
        s1=Segment(args)
        args={"SEGMENT_0":intPoint, "SEGMENT_1":Point(0.0, 10.0)}
        s2=Segment(args)
        
        ent1=newDoc.saveEntity(s1).getId()
        ent2=newDoc.saveEntity(s2).getId()
       
        cObject=self.__pyCadApplication.getCommand("CHAMFER")
        keys=list(cObject.keys())
        cObject[keys[0]]=ent1
        cObject[keys[1]]=ent2
        cObject[keys[2]]=None
        cObject[keys[3]]=None
        cObject[keys[4]]="FIRST"
        cObject[keys[5]]=2
        cObject[keys[6]]=2

        cObject.applyCommand()
    #@-others
#@-others
#@-leo
