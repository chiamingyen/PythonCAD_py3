#@+leo-ver=5-thin
#@+node:1.20130426141258.3051: * @file dxf.py
#
# Copyright (c) 2009,2010,2011 Matteo Boscolo,Yagnesh Desai
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the termscl_bo of the GNU General Public License as published by
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



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3052: ** <<declarations>> (dxf)
dxfDebug=False

import math         # added to handle arc start and end point defination
import re           # added to handle Mtext
import os, sys
from Kernel.initsetting               import cgcol
from Kernel.layer                     import Layer
from Kernel.GeoEntity.point           import Point
from Kernel.GeoEntity.segment         import Segment
from Kernel.GeoEntity.arc             import Arc
from Kernel.GeoEntity.text            import Text
from Kernel.GeoEntity.ellipse         import Ellipse
from Kernel.GeoEntity.polyline        import Polyline
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3053: ** ChangeColor
def ChangeColor(x):
    try:
        newcolor = cgcol[x]
    except:
        newcolor = 256
    return newcolor
#@+node:1.20130426141258.3054: ** changeColorFromDxf
def changeColorFromDxf(col):
    if col == '256':
        newcol = layerColor[col]#Work in progress layerColor captured under readLayer needs to be used
    else:
        newcol = ChangeColor(col)
    return newcol
#@+node:1.20130426141258.3055: ** class DrawingFile
class DrawingFile(object):
    """
        This Class provide base capability to read write a  file
    """
    #@+others
    #@+node:1.20130426141258.3056: *3* __init__
    def __init__(self,fileName):
        """
            Base Constructor
        """
        dPrint( "Debug: DrawingFile constructor")
        self.__fn=fileName
        self.__fb=None
        self.__errors=[]
        self.__reading=False
        self.__writing=False
        self.__lineNumber=0
    #@+node:1.20130426141258.3057: *3* readAsci
    def readAsci(self):
        """
            Read a generic file
        """
        dPrint("Debug: Read asci File")
        self.__fb=open(self.__fn,'r')
        self.__reading=True
        self.__writing=False
    #@+node:1.20130426141258.3058: *3* createAsci
    def createAsci(self):
        """
            create the new file
        """
        self.__fb=open(self.__fn,'w')
        self.__reading=False
        self.__writing=True
    #@+node:1.20130426141258.3059: *3* fileObject
    def fileObject(self):
        """
            Return the file opened
        """
        dPrint( "Debug: GetFileObject")
        if self.__fb is not None:
          dPrint( "Debug: Return file object")
          return self.__fb
        else:
          dPrint( "Debug: None")
          return None
    #@+node:1.20130426141258.3060: *3* readLine
    def readLine(self):
        """
            read a line and return it
        """
        if self.__reading:
            self.__lineNumber=self.__lineNumber+1
            return self.__fb.readline()
        else:
            raise ("Unable to perfor reading operation")
    #@+node:1.20130426141258.3061: *3* writeLine
    def writeLine(self,line):
        """
            write a line to the file
        """
        if self.__writing:
            self.__fb.write(line)
        else:
            raise ("Unable to perfor writing operation")
    #@+node:1.20130426141258.3062: *3* writeError
    def writeError(self,functionName,msg):
        """
            Add an Error to the Collection
        """
        _msg='Error on line %s function Name: %s Message %s \n'%(
            str(self.__lineNumber, 'ASCII'),functionName,msg)
        self.__errors.append(_msg)
    #@+node:1.20130426141258.3063: *3* getError
    def getError(self):
        """
        get the import export error
        """
        if len(self.__errors)>0:
            return self.__errors
        else:
            return None
    #@+node:1.20130426141258.3064: *3* close
    def close(self):
        """
        close the active fileObject
        """
        if not self.__fb is None:
            self.__fb.close()
    #@+node:1.20130426141258.3065: *3* getFileName
    def getFileName(self):
        """
            Return The active file Name
        """
        return self.__fn
    #@-others
#@+node:1.20130426141258.3066: ** class Dxf
class Dxf(DrawingFile):
    """
        this class provide dxf reading/writing capability
    """
    #@+others
    #@+node:1.20130426141258.3067: *3* __init__
    def __init__(self,kernel,fileName):
        """
            Default Constructor
        """
        dPrint( "Debug: Dxf constructor")
        DrawingFile.__init__(self,fileName)
        self.__kernel=kernel
        self.__dxfLayer=None
    #@+node:1.20130426141258.3068: *3* exportEntitis
    def exportEntitis(self):
        """
            export The current file in dxf format
        """
        _fo=self.createAsci()               #open the file for writing
        _layersEnts=self.getAllEntitis()    #get all the entities from the file
        self.writeLine("999\nExported from Pythoncad\nSECTION\n  2\nENTITIES\n")#header section for entities
        for _key in _layersEnts:            #Looping at all layer
            #create header section#
            for _obj in _layersEnts[_key]:  #looping at all entities in the layer
                obj=_obj.toGeometricalEntity()
                if isinstance(obj,Segment):#if it's segment
                    self.writeSegment(obj, _obj.getInnerStyle()) # ad it at the dxf drawing
                    continue
                if isinstance(obj,Arc):
                    self.writeArc(obj, _obj.getInnerStyle())
                    continue
                if isinstance(obj,Polyline):
                    self.writePolyline(obj, _obj.getInnerStyle())
                    continue
                if isinstance(obj,Text):
                    self.writeText(obj, _obj.getInnerStyle())
                    continue
                # go on end implements the other case arc circle ...
        self.writeLine("  0\nENDSEC\n  0\nEOF")#writing End Of File
        self.close()
    #@+node:1.20130426141258.3069: *3* getAllEntitis
    def getAllEntitis(self):
        """
            retrive all the entitys from the drawing
        """
        _outLayers={}
        getChildrenEnt=self.__kernel.getTreeLayer.getLayerChildren
        layerNodes=self.__kernel.getTreeLayer.getLayerdbTree()
        def populateDxfStructure(layers):
            for key in layers:
                _layerEnts=[]
                layer, childs=layers[key]
                for ent in getChildrenEnt(layer):
                    _layerEnts.append(ent)
                l=self.__kernel.getTreeLayer._getLayerConstructionElement(layer)
                _outLayers[l.name]=_layerEnts
                populateDxfStructure(childs)
        populateDxfStructure(layerNodes)
        return _outLayers
    #@+node:1.20130426141258.3070: *3* writeSegment
    def writeSegment(self,e, style):
        """
           write segment to the dxf file
        """
        x1,y1=e.getP1().getCoords()
        x2,y2=e.getP2().getCoords()
        _c=style.getStyleProp('entity_color')
        _c = ChangeColor(_c)
        dPrint("debug line color are %s"%str( _c)) # TODO : replace the dprint with the logging
        self.writeLine("  0\nLINE\n100\nAcdbLine\n")
        self.writeLine(" 62\n" + str(_c) +"\n")
        self.writeLine(" 10\n" +str(x1) +"\n")
        self.writeLine(" 20\n" +str(y1) +"\n 30\n0.0\n")
        self.writeLine(" 11\n" +str(x2) +"\n")
        self.writeLine(" 21\n" +str(y2) +"\n 31\n0.0\n")
    #@+node:1.20130426141258.3071: *3* writeArc
    def writeArc(self,e, style):
        """
           Write Arc to the dxf file
        """
        x1,y1 = e.getCenter().getCoords()
        r = e.getRadius()
        sa = e.getStartAngle()
        ea = e.getEndAngle()
        _c = str(style.getStyleProp('entity_color'), 'ASCII')
        _c = ChangeColor(_c)
        dPrint("debug Arc color are %s "%str( _c, 'ASCII'))
        self.writeLine("  0\nARC\n100\nAcDbCircle\n")
        self.writeLine(" 62\n" +str(_c, 'ASCII') +"\n")
        self.writeLine(" 10\n" +str(x1, 'ASCII') +"\n")
        self.writeLine(" 20\n" +str(y1, 'ASCII') +"\n 30\n0.0\n")
        self.writeLine(" 40\n" +str(r, 'ASCII') +"\n")
        self.writeLine(" 50\n" +str(sa, 'ASCII') +"\n 51\n"+str(ea, 'ASCII')+"\n")
    #@+node:1.20130426141258.3072: *3* writePolyline
    def writePolyline(self,e, style):
        """
           Write Polyline to the dxf file
        """
        _c = str(style.getStyleProp('entity_color'), 'ASCII')
        _c = ChangeColor(_c)
        dPrint( "debug Arc color are %s"%str(_c, 'ASCII'))
        self.writeLine("  0\nLWPOLYLINE\n100\nAcDbPolyline\n")
        self.writeLine(" 62\n" +str(_c, 'ASCII') +"\n")
        count = e.getNumPoints()
        self.writeLine(" 90\n" +str(count, 'ASCII')+ "\n")
        self.writeLine(" 70\n0\n")
        self.writeLine(" 43\n0\n")
        c = 0
        points = []
        while c < count:
            x1,y1 = e.getPoint(c).getCoords()
            self.writeLine(" 10\n" +str(x1, 'ASCII') +"\n")
            self.writeLine(" 20\n" +str(y1, 'ASCII') +"\n")
            c = c + 1
    #@+node:1.20130426141258.3073: *3* writeText
    def writeText(self,e, style):
        """
           Write Text to the dxf file
        """
        x1,y1=e.location.getCoords()
        h = style.getStyleProp('text_height')
        _c = str(style.getStyleProp('entity_color'), 'ASCII')
        _c = ChangeColor(_c)
        dPrint("debug Text color are %s "%str( _c, 'ASCII'))
        txt = e.text
        txt = txt.replace(' ', '\~')
        txt = txt.replace('\n', '\P')
        self.writeLine("  0\nMTEXT\n100\nAcDbMText\n")
        self.writeLine(" 62\n" +str(_c, 'ASCII') +"\n")
        self.writeLine(" 10\n" +str(x1, 'ASCII') +"\n")
        self.writeLine(" 20\n" +str(y1, 'ASCII') +"\n 30\n0.0\n")
        self.writeLine(" 40\n" +str(h, 'ASCII') +"\n")
        self.writeLine("  1\n" +str(txt, 'ASCII') +"\n")
    #@+node:1.20130426141258.3074: *3* importEntitis
    def importEntitis(self):
        """
            Open The file and create The entity in pythonCad
        """
        dPrint( "Debug: import entitys")
        self.readAsci();
        _layerName,_ext=os.path.splitext(os.path.basename(self.getFileName()))
        _layerName="Imported_"+_layerName
        parentLayer=self.__kernel.getTreeLayer.getActiveLater()
        newLayer=self.__kernel.saveEntity(Layer(_layerName))
        self.__kernel.getTreeLayer.insert(newLayer, parentLayer)

        try:
            self.__kernel.startMassiveCreation()
            while True:
                _k = self.readLine()
                if not _k: break
                else:
                    ##print  "debug: readline", _k # TODO : replace the dprint with the logging
                    #dPrint( "Debug: Read Line line = [%s]"%str(_k)) # TODO : replace the dprint with the logging
                    if _k[0:5] == 'TABLE':
                        _k = self.readLine() # for tag "  2"
                        _k = self.readLine() # for table name
                        ##print "debug TABLE found" # TODO : replace the dprint with the logging
                        if _k[0:5] == 'LAYER':
                            self.readLayer()
                            #print "debug LAYER found" # TODO : replace the dprint with the logging
                        continue
                    if _k[0:4] == 'LINE':
                        self.createLineFromDxf()
                        ##print "debug line found" # TODO : replace the dprint with the logging
                        continue
                    if _k[0:6] == 'CIRCLE':
                        self.createCircleFromDxf()
                        continue
                    if _k[0:5] == 'MTEXT':
                        self.createTextFromDxf()
                        continue
                    if _k[0:4] == 'TEXT':
                        #self.createTextFromDxf()
                        continue
                    if _k[0:3] == 'ARC':
                        self.createArcFromDxf()
                        ##print "debug arc found"
                        continue
                    if _k[0:10] == 'LWPOLYLINE':
                        #self.createPolylineFromDxf()
                        continue
                    if _k[0:8] == 'POLYLINE':
                        #self.createPolylineFromDxf()
                        continue
                    if not _k : break
            self.__kernel.performCommit()
        finally:
            self.__kernel.stopMassiveCreation()
    #@+node:1.20130426141258.3075: *3* readLayer
    def readLayer(self):
        """
        Reading the data in the dxf file under TABLE section
        it collects the information regarding the
        Layers, Colors and Linetype
        WORK IN PROGRESS
        """
        ##print 'debug Layer found !'
        layerColor = {}
        dxfColor = 0
        layerName = '0'
        #_k = self.readLine()
        while True:
            _k = self.readLine()
            if _k[0:6] == 'ENDTAB':
                break
            if _k[0:3] == '  2':
                _k = self.readLine()
                layerName = _k.replace('\n', '')
                #print "Debug New LayerName=", layerName
            if _k[0:3] == ' 62':
                _k = self.readLine()
                dxfColor = _k.replace('\n', '')
                #print "Debug new dxfColor = ", dxfColor
            layerColor[layerName] = dxfColor
        return layerColor
    #@+node:1.20130426141258.3076: *3* createLineFromDxf
    def createLineFromDxf(self):
        """
            read the line dxf section and create the line
        """
        dPrint( "Debug createLineFromDxf" )# TODO : replace the dprint with the logging
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        g = 0 # start counter to read lines
        c = 0
        while g < 18:
            ##print "Debug g =", g
            ##print "Debug: Read line  g = %s Value = %s "%(str(g),str(line))
            _k = self.readLine()
            ##print "Debug: Read line g = %s k =  %s "%(str(g),str(k))
            #dPrint( "line value k="+_k)
            if _k[0:3] == ' 62':# COLOR
                _k = self.readLine()
                c = (int(_k[0:-1]))
            if _k[0:3] == ' 10':
                dPrint( "debug 10"+ _k)
                # this line of file contains start point"X" co ordinate
                ##print "Debug: Convert To flot x1: %s" % str(k[0:-1])
                _k = self.readLine()
                x1 = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 20':# this line of file contains start point "Y" co ordinate
                ##print "Debug: Convert To flot y1: %s" % str(k[0:-1])
                _k = self.readLine()
                y1 = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 30':# this line of file contains start point "Z" co ordinate
                ##print "Debug: Convert To flot z1: %s" % str(k[0:-1])
                _k = self.readLine()
                z1 = (float(_k[0:-1]))
                continue
                # Z co ordinates are not used in PythonCAD we can live without this line
            if _k[0:3] == ' 11':# this line of file contains End point "X" co ordinate
                ##print "Debug: Convert To flot x2: %s" % str(k[0:-1])
                _k = self.readLine()
                x2 = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 21':# this line of file contains End point "Y" co ordinate
                ##print "Debug: Convert To flot y2: %s" % str(k[0:-1])
                _k = self.readLine()
                y2 = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 31':# this line of file contains End point "Z" co ordinate
                ##print "Debug: Convert To flot z2: %s" % str(k[0:-1])
                _k = self.readLine()
                z2 = (float(_k[0:-1]))
                g = 119
                continue
                #Z coordinates are not used in PythonCAD we can live without this line
        if c == None:
            c = 7
        if not ( x1==None or y1 ==None or
           x2==None or y2 ==None ):
            self.createLine(x1,y1,x2,y2,c)
        else:
            _msg='Read parameter from file x1: [%s] y1: [%s] x2: [%s] y2: [%s]'%(
                        str(x1, 'ASCII'),str(y1, 'ASCII'),str(x2, 'ASCII'),str(y2, 'ASCII'))
            self.writeError('createLineFromDxf',_msg)
    #@+node:1.20130426141258.3077: *3* createLine
    def createLine(self,x1,y1,x2,y2,c):
        """
          Create the line into the current drawing
        """
        args={"SEGMENT_0":Point(x1, y1), "SEGMENT_1":Point(x2, y2)}
        _seg = Segment(args)
        self.__kernel.saveEntity(_seg)
    #@+node:1.20130426141258.3078: *3* createCircleFromDxf
    def createCircleFromDxf(self):
        """
            Read and create the Circle into drawing
        """
        dPrint( "Debug createCircleFromDxf" )
        g = 0 # reset g
        c = 0
        while g < 1:
            _k = self.readLine()
            dPrint( "line value k="+ _k)
            if _k[0:3] == ' 62':# COLOR
                _k = self.readLine()
                c = (int(_k[0:-1]))
            if _k[0:3] == ' 10':
                _k = self.readLine()
                x = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 20':
                _k = self.readLine()
                y = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 30':
                _k = self.readLine()
                z = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 40':
                _k = self.readLine()
                r = (float(_k[0:-1]))
                g = 10 # g > 1 for break
                'I need a "create Circle code" here to append the segment to image'
        if c == None:
            c = 7
        self.createArc(x,y,r,c)
    #@+node:1.20130426141258.3079: *3* createTextFromDxf
    def createTextFromDxf(self):
        """
            Read and create the Text into drawing
        """
        dPrint( "Debug createTextFromDxf" )
        g = 0 # reset g
        x = None
        y = None
        h = None
        _t= ''
        while g < 1:
            _k = self.readLine()
            try:
                dPrint("line value k="+ _k)
                #if _k[0:3] == ' 62':# COLOR
                #    _k = self.readLine()
                #    c = (int(_k[0:-1]))
                if _k[0:3] == ' 10':
                    _k = self.readLine()
                    x = (float(_k[0:-1]))
                    ##print "Text Loc x =", x
                    continue
                if _k[0:3] == ' 20':
                    _k = self.readLine()
                    y = (float(_k[0:-1]))
                    #rint "Text Loc y =", y
                    continue
                if _k[0:3] == ' 30':
                    _k = self.readLine()
                    z = (float(_k[0:-1]))
                    ##print "Text Loc z =", z
                    continue
                if _k[0:3] == ' 40':
                    _k = self.readLine()
                    h = (float(_k[0:-1]))
                    dPrint("Text Height =%s"%str(h, 'ASCII'))
                    continue
                if _k[0:3] == '  1':
                    _k = self.readLine()
                    _t = _k.replace('\~', ' ')
                    _t = _t.replace('\P', '\n')
                    ##print "Text itself is ", x, y, z, 'height', h, _t#
                    g = 10 # g > 1 for break
                    continue
            except:
                print("Error on reading "+str(_k, 'ASCII'))
        if not (x is None or y is None or h is None):
            self.createText(x,y,h,_t)
        else:
            _msg="Read parameter from file x: [%s] y: [%s] h: [%s] t: [%s]"%(
                        str(x, 'ASCII'),str(y, 'ASCII'),str(h, 'ASCII'),str(_t, 'ASCII'))
            self.writeError("createTextFromDxf",_msg)
    #@+node:1.20130426141258.3080: *3* createArcFromDxf
    def createArcFromDxf(self):
        """
            Read and create the ARC into drawing
        """
        g = 0 # reset g
        c = 0
        while g < 1:
            _k = self.readLine()
            if _k[0:3] == ' 62':# COLOR
                _k = self.readLine()
                c = (int(_k[0:-1]))
            if _k[0:3] == ' 10':
                _k = self.readLine()
                x = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 20':
                _k = self.readLine()
                y = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 30':
                _k = self.readLine()
                z = (float(_k[0:-1]))
            if _k[0:3] == ' 40':
                _k = self.readLine()
                r = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 50':
                _k = self.readLine()
                sa = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 51':
                _k = self.readLine()
                ea = (float(_k[0:-1]))
                g = 10 # g > 1 for break\\
                continue
        if c == None:
                c = 7
        self.createArc(x,y,r,c,sa,ea)
    #@+node:1.20130426141258.3081: *3* createArc
    def createArc(self,x,y,r,color=None,sa=None,ea=None):
        """
            Create a Arc entitys into the current drawing
        """
        _center = Point(x, y)
        if sa is None or ea is None:
            sa=ea=0 #This is the case of circle
        else:
            sa=(sa*math.pi)/180
            ea=(ea*math.pi)/180
            ea=ea-sa
        args={"ARC_0":_center, "ARC_1":r, "ARC_2":sa, "ARC_3":ea}
        _arc = Arc(args)
        self.__kernel.saveEntity(_arc)
    #@+node:1.20130426141258.3082: *3* createText
    def createText(self,x,y,h,t):
        """
            Create a Text entitys into the current drawing
        """
        try:
            _text = t.replace('\x00', '').decode('utf8', 'ignore').encode('utf8')
        except:
            self.writeError("createText","Debug Error Converting in unicode [%s]"%t)
            _text ='Unable to convert in unicode'
        _p = Point(x, y)
        args={"TEXT_0":_p,"TEXT_1":_text, "TEXT_2":0.0, "TEXT_3":""}
        _tb = Text(args)
        self.__kernel.saveEntity(_tb)
    #@+node:1.20130426141258.3083: *3* createPolylineFromDxf
    def createPolylineFromDxf(self):
        """
        Polyline creation read the line dxf section and create the line
        """
        dPrint("Exec createPolylineFromDxf")
        c = 0
        while True:
            _k = self.readLine()
            if _k[0:3] == ' 62':# COLOR
                _k = self.readLine()
                c = (int(_k[0:-1]))
            if _k[0:3] == ' 10':
                break
        points=[]
        p = ()
        t = 0
        while True:
            # this line of file contains start point"X" co ordinate
            # #print "Debug: Convert To flot x1: %s" % str(k[0:-1])
            _k = self.readLine()
            x = (float(_k[0:-1]))
            _k = self.readLine()#pass for k[0:3] == ' 20'
            _k = self.readLine()
            y = (float(_k[0:-1]))
            p = (x,y)
            points.append(p)
            dPrint( str(points, 'ASCII'))
            _k = self.readLine()
            if _k[0:3] == ' 30':
                _k = self.readLine()
                z1 = (float(_k[0:-1]))
                _k = self.readLine()
                continue
            if _k[0:3] != ' 10':
                break
            continue
        if c == None:
                c = 7
        if len(points)>1:
            self.createPolyline(points,c)
    #@+node:1.20130426141258.3084: *3* createPolyline
    def createPolyline(self,points,c):
        """
            Crate poliline into Pythoncad
        """
        pass #TODO: must be implemented

        dPrint("Exec createPolyline")
        i=0
        args={}
        for _x, _y in points:
            _p = Point(_x, _y)
            args["POLYLINE_%s"%str(i, 'ASCII')]=_p
            i+=1
        pline=Polyline(args)
        self.__kernel.saveEntity(pline)
    #@-others
#@+node:1.20130426141258.3085: ** dPrint
def dPrint(msg):
    """
        Debug function for the dxf file
    """
    if dxfDebug :
        print("Debug: %s " %str(msg, 'ASCII'))
#@-others
#@-leo
