#@+leo-ver=5-thin
#@+node:1.20130426141258.3844: * @file widgets.py
#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.3845: ** <<declarations>> (widgets)
from PyQt4 import QtCore, QtGui

IdRole = QtCore.Qt.UserRole
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.3846: ** class BaseContainer
class BaseContainer(QtGui.QHBoxLayout):
    #@+others
    #@+node:1.20130426141258.3847: *3* __init__
    def __init__(self, parent=None, label="baseInfo"):
        super(BaseContainer, self).__init__(parent)
        label=QtGui.QLabel(label)
        self.addWidget(label)
        self.activeValue=None
        self._changed=False
    #@+node:1.20130426141258.3848: *3* value
    @property
    def value(self):
        """
            return the value of the object
        """
        return self.activeValue
    #@+node:1.20130426141258.3849: *3* changed
    @property
    def changed(self):
        """
            tells if the value is changed
        """
        return self._changed
    #@+node:1.20130426141258.3850: *3* changed
    @changed.setter  
    def changed(self, value):
        """
            tells if the value is changed
        """
        self._changed=value
    #@-others
#@+node:1.20130426141258.3851: ** class PyCadQColor
class PyCadQColor(BaseContainer):
    #@+others
    #@+node:1.20130426141258.3852: *3* __init__
    def __init__(self, parent=None, oldValue='green', label="Color"):
        super(PyCadQColor, self).__init__(parent=parent, label=label)
        r, g, b=oldValue
        self.activeValue=oldValue
        self.pushButton=QtGui.QPushButton()
        self.pushButton.clicked.connect(self.click)
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        self.colorLabel = QtGui.QLabel()
        self.colorLabel.setFrameStyle(frameStyle)
        sColor=QtGui.QColor.fromRgb(r, g, b)
        self.colorLabel.setText(sColor.name())
        self.colorLabel.setPalette(QtGui.QPalette(sColor))
        self.colorLabel.setAutoFillBackground(True)
        self.addWidget(self.colorLabel)
        self.addWidget(self.pushButton)
    #@+node:1.20130426141258.3853: *3* click
    def click(self):
        r, g, b=self.activeValue
        sColor=QtGui.QColor.fromRgb(r, g, b)
        color = QtGui.QColorDialog.getColor(sColor, parent=None)
        if color.isValid(): 
            self.colorLabel.setText(color.name())
            self.colorLabel.setPalette(QtGui.QPalette(color))
            self.colorLabel.setAutoFillBackground(True)
            self.activeValue=(color.red(), 
                              color.green(), 
                              color.blue()
                              )
            self.changed=True
    #@-others
#@+node:1.20130426141258.3854: ** class PyCadQLineType
class PyCadQLineType(BaseContainer):
    #@+others
    #@+node:1.20130426141258.3855: *3* __init__
    def __init__(self, parent=None, oldValue=QtCore.Qt.SolidLine, label="&Pen Style"):
        super(PyCadQLineType, self).__init__(parent=parent, label=label)
        self.activeValue=oldValue
        #define Active combo box
        self.penStyleComboBox = QtGui.QComboBox()
        self.penStyleComboBox.addItem("Solid", QtCore.Qt.SolidLine)
        self.penStyleComboBox.addItem("Dash", QtCore.Qt.DashLine)
        self.penStyleComboBox.addItem("Dot", QtCore.Qt.DotLine)
        self.penStyleComboBox.addItem("Dash Dot", QtCore.Qt.DashDotLine)
        self.penStyleComboBox.addItem("Dash Dot Dot", QtCore.Qt.DashDotDotLine)
        itemindex=self.penStyleComboBox.findData(oldValue)
        self.penStyleComboBox.setCurrentIndex(itemindex)
        #define label
        penStyleLabel = QtGui.QLabel("")
        penStyleLabel.setBuddy(self.penStyleComboBox)
        
        self.addWidget(penStyleLabel)
        self.addWidget(self.penStyleComboBox)
                
        self.penStyleComboBox.activated.connect(self.penChanged)
    #@+node:1.20130426141258.3856: *3* penChanged
    def penChanged(self):
        """
            change event 
        """
        value=self.penStyleComboBox.currentIndex()
        self.activeValue = QtCore.Qt.PenStyle(self.penStyleComboBox.itemData(value, IdRole).toInt()[0])
        self.changed=True
    #@-others
#@+node:1.20130426141258.3857: ** class PyCadQDouble
class PyCadQDouble(BaseContainer):
    #@+others
    #@+node:1.20130426141258.3858: *3* __init__
    def __init__(self, parent=None, oldValue='0.0', label="Double"):
        super(PyCadQDouble, self).__init__(parent, label)
        self.activeValue=oldValue
        self.penWidthSpinBox = QtGui.QSpinBox()
        self.penWidthSpinBox.setRange(0, 20)
        self.penWidthSpinBox.setValue(int(oldValue))
        self.penWidthSpinBox.setSpecialValueText("0 (cosmetic pen)")
        self.penWidthSpinBox.valueChanged.connect(self.penChanged)
        
        self.addWidget(self.penWidthSpinBox)
    #@+node:1.20130426141258.3859: *3* penChanged
    def penChanged(self):
        """
            change event 
        """
        self.activeValue=self.penWidthSpinBox.value()
        self.changed=True
    #@-others
#@+node:1.20130426141258.3860: ** class PyCadQFont
class PyCadQFont(BaseContainer ):
    #@+others
    #@+node:1.20130426141258.3861: *3* __init__
    def __init__(self, parent=None, oldValue='green', label="Font"):
        super(PyCadQFont, self).__init__(parent, label)
    #@-others
#@-others
#@-leo
