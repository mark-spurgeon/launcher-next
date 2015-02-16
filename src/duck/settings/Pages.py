import os
import sys
sys.dont_write_bytecode=True
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import Main
import Widgets 

from duck.launcher import Apps
from duck import datadir
ICON_DIR=datadir.getDir()+"icons/default/"

def hexToRgb(triplet):
	triplet= str(triplet).replace("#","")
	_NUMERALS = '0123456789abcdefABCDEF'
	_HEXDEC = {v: int(v, 16) for v in (x+y for x in _NUMERALS for y in _NUMERALS)}
	return ( _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]])
def moveUpList(app_name, dock_apps):
	new_l=None
	dock_apps=[str(a["name"]) for a in dock_apps]

	if dock_apps.index(app_name) >0 and app_name in dock_apps:
		index=None
		for i, d in enumerate(dock_apps):
			if str(d)==str(app_name):
				index=i
				break
		if index!=None:
			new_l=dock_apps
			new_l.pop(index)
			new_l.insert(index-1,app_name)
	return new_l
def moveDownList(app_name, dock_apps):
	new_l=None
	dock_apps=[str(a["name"]) for a in dock_apps]
	if dock_apps.index(app_name) < len(dock_apps) and app_name in dock_apps:

		index=None
		for i, d in enumerate(dock_apps):
			if str(d)==str(app_name):
				index=i
				break
		if index!=None:
			new_l=dock_apps
			new_l.pop(index)
			new_l.insert(index+1,app_name)
	return new_l
######
#Widgets
######
class FirstPage(QScrollArea):
    def __init__(self,parent):
        QScrollArea.__init__(self,parent)
        self.parent=parent

        self.layout=QVBoxLayout(self)

        lay1=QHBoxLayout(self)
        label1=QLabel("Foreground Color:")
        lay1.addWidget(label1)
        self.colorButton1 = Widgets.QColorButton(self)
        self.colorButton1.setColor("rgb({0},{1},{2})".format(self.parent.red,self.parent.green,self.parent.blue))
        self.colorButton1.colorChanged.connect(self.onForegroundColor)
        lay1.addWidget(self.colorButton1)
        self.layout.addLayout(lay1)

        lay2=QHBoxLayout(self)
        label2=QLabel("Background Color:")
        lay2.addWidget(label2)
        self.colorButton2 = Widgets.QColorButton(self)
        self.colorButton2.setColor("rgb({0},{1},{2})".format(self.parent.config["r2"],self.parent.config["g2"],self.parent.config["b2"]))
        self.colorButton2.colorChanged.connect(self.onBackgroundColor)
        lay2.addWidget(self.colorButton2)
        self.layout.addLayout(lay2)

        lay2_2=QHBoxLayout(self)
        label2_2=QLabel("Font Color:")
        lay2_2.addWidget(label2_2)
        self.colorButton2_2 = Widgets.QColorButton(self)
        self.colorButton2_2.setColor("rgb({0},{1},{2})".format(self.parent.config["font-r"],self.parent.config["font-g"],self.parent.config["font-b"]))
        self.colorButton2_2.colorChanged.connect(self.onFontColor)
        lay2_2.addWidget(self.colorButton2_2)
        self.layout.addLayout(lay2_2)

        lay3=QHBoxLayout(self)
        label3=QLabel("Background Opacity:")
        lay3.addWidget(label3)
        self.num1=QSpinBox(self)
        self.num1.setMinimum(0)
        self.num1.setMaximum(255)
        self.num1.setValue(self.parent.config["alpha"])
        self.num1.valueChanged.connect(self.onBackgroundOpacity)
        lay3.addWidget(self.num1)
        self.layout.addLayout(lay3)

        lay4=QHBoxLayout(self)
        label4=QLabel("Launcher Width:")
        lay4.addWidget(label4)
        self.num2=QSpinBox(self)
        self.num2.setMinimum(10)
        self.num2.setMaximum(80)
        self.num2.setValue(self.parent.config["size"])
        self.num2.valueChanged.connect(self.onLauncherWidth)
        lay4.addWidget(self.num2)
        self.layout.addLayout(lay4)

        lay5=QHBoxLayout(self)
        label5=QLabel("Icon Size:")
        lay5.addWidget(label5)
        self.num3=QSpinBox(self)
        self.num3.setMinimum(20)
        self.num3.setMaximum(80)
        self.num3.setValue(self.parent.config["icon-size"])
        self.num3.valueChanged.connect(self.onIconSize)
        lay5.addWidget(self.num3)
        self.layout.addLayout(lay5)

        lay6=QHBoxLayout(self)
        label6=QLabel("Animation Speed:")
        lay6.addWidget(label6)
        self.num4=QDoubleSpinBox(self)
        self.num4.setMinimum(0.0)
        self.num4.setMaximum(10.0)
        self.num4.setValue(self.parent.config["animation-speed"])
        self.num4.valueChanged.connect(self.onAnimationSpeed)
        lay6.addWidget(self.num4)
        self.layout.addLayout(lay6)
        
        lay7=QHBoxLayout(self)
        label7=QLabel("Font:")
        lay7.addWidget(label7)
        self.combo1 = QComboBox(self)
        for i,a in  enumerate(QFontDatabase().families()):
        	self.combo1.addItem(a)
        	if str(self.parent.config["font"])==str(a):
        		self.combo1.setCurrentIndex(i)
        self.combo1.currentIndexChanged.connect(self.onFont)
        lay7.addWidget(self.combo1)
        self.layout.addLayout(lay7)    
        self.setLayout(self.layout)
    ##
    ##Events
    def onForegroundColor(self):
    	hexColor= self.colorButton1.color()
    	r,g,b = hexToRgb(hexColor)
    	self.parent.red=r
    	self.parent.green=g
    	self.parent.blue=b
    	self.parent.update()
    	Main.setConfig({"r1":r},{"g1":g},{"b1":b})
    def onBackgroundColor(self):
    	hexColor= self.colorButton2.color()
    	r,g,b = hexToRgb(hexColor)
    	Main.setConfig({"r2":r},{"g2":g},{"b2":b})
    def onFontColor(self):
    	hexColor= self.colorButton2_2.color()
    	print hexColor
    	r,g,b = hexToRgb(hexColor)
    	Main.setConfig({"font-r":r},{"font-g":g},{"font-b":b})
    def onBackgroundOpacity(self):
    	val = self.num1.value()
    	Main.setConfig({"alpha":int(val)})
    def onLauncherWidth(self):
    	val = self.num2.value()
    	Main.setConfig({"size":int(val)})
    def onIconSize(self):
    	val = self.num3.value()
    	Main.setConfig({"icon-size":int(val)})
    def onAnimationSpeed(self):
    	val = self.num4.value()
    	Main.setConfig({"animation-speed":int(val)})
    def onFont(self,i):
    	font = self.combo1.currentText()
    	Main.setConfig({"font":str(font)})
class AddButton(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.parent=parent
        self.layout=QHBoxLayout(self)
        self.button=Widgets.PicButton(self,"{}settings-plus.svg".format(ICON_DIR))
        self.button.setIconSize(QSize(30,30))
        self.button.clicked.connect(self.onPlus)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
    def onPlus(self):
    	addappwindow = Widgets.AddAppWindow(None)
    	addappwindow.show()
    	addappwindow.appChosen.connect(self.appChosen)
    def appChosen(self,data):
    	i=QListWidgetItem()
    	w=DockAppWidget(self.parent,data,i)
    	self.parent.addItem(i)
    	self.parent.setItemWidget(i,w)
    	#
    	self.parent.dock_apps.append(data)
    	#config
    	dock_apps_list= [a["name"] for a in self.parent.dock_apps]
        Main.setConfig({"dock-apps":dock_apps_list})
class DockAppWidget(QWidget):
    def __init__(self,parent,app,item):
        QWidget.__init__(self,parent)
        self.parent=parent
        self.item=item
        #self.resize(self.parent.width(),40)
        self.app=app
        self.layout = QHBoxLayout(self)
       	self.appIcon=Widgets.PicButton(self,Apps.ico_from_name(app["icon"])	)
       	self.appIcon.setIconSize(QSize(32,32))
       	self.appIcon.setMaximumWidth(40)
       	self.appIcon.setMinimumHeight(32)
       	self.layout.addWidget(self.appIcon)
    	self.label=QLabel(self)
    	self.label.setText(app["name"])
    	self.layout.addWidget(self.label)

    	self.moveUpButton=Widgets.PicButton(self,"{}settings-up.svg".format(ICON_DIR))
    	self.moveUpButton.move(self.width(),0)
    	self.moveUpButton.setMaximumWidth(40)
    	self.moveUpButton.setIconSize(QSize(25,25))
    	self.moveUpButton.clicked.connect(self.moveAppUp)
    	self.layout.addWidget(self.moveUpButton)

    	self.moveDownButton=Widgets.PicButton(self,"{}settings-down.svg".format(ICON_DIR))
    	self.moveDownButton.move(self.width(),0)
    	self.moveDownButton.setMaximumWidth(40)
    	self.moveDownButton.setIconSize(QSize(25,25))
    	self.moveDownButton.clicked.connect(self.moveAppDown)
    	self.layout.addWidget(self.moveDownButton)

    	self.removeButton=Widgets.PicButton(self,"{}settings-remove.svg".format(ICON_DIR))
    	self.removeButton.move(self.width(),0)
    	self.removeButton.setMaximumWidth(40)
    	self.removeButton.setIconSize(QSize(20,20))
    	self.removeButton.clicked.connect(self.removeApp)
    	self.layout.addWidget(self.removeButton)

    	self.setLayout(self.layout)
    	self.setStyleSheet("""
    		QWidget {
    			background-color:rgb(255,255,255)
    		}
    		""")
    def removeApp(self):
    	#widget
        row=self.parent.indexFromItem(self.item).row()
        self.parent.takeItem(row)    
        self.parent.dock_apps.pop(row)
        #config
        dock_apps_list= [a["name"] for a in self.parent.dock_apps]
        Main.setConfig({"dock-apps":dock_apps_list})
    def moveAppUp(self):
    	#widget
    	row=self.parent.indexFromItem(self.item).row()
    	self.parent.takeItem(row)  
    	self.parent.dock_apps.pop(row)
    	if row-1>=0:
    		self.parent.insertItem(row-1,self.item)
    		self.parent.dock_apps.insert(row-1,self.app)
    	else:
    		self.parent.insertItem(row,self.item)
    		self.parent.dock_apps.insert(row,self.app)
    	w=DockAppWidget(self.parent,self.app,self.item)
    	self.parent.setItemWidget(self.item,w)
    	#config
    	dock_apps_list= [a["name"] for a in self.parent.dock_apps]
        Main.setConfig({"dock-apps":dock_apps_list})
    def moveAppDown(self):
    	row=self.parent.indexFromItem(self.item).row()
    	self.parent.takeItem(row)  
    	self.parent.dock_apps.pop(row)
    	if row-1<=len(self.parent.dock_apps):
    		self.parent.insertItem(row+1,self.item)
    		self.parent.dock_apps.insert(row+1,self.app)
    	else:
    		self.parent.insertItem(row,self.item)
    		self.parent.dock_apps.insert(row,self.app)
    	w=DockAppWidget(self.parent,self.app,self.item)
    	self.parent.setItemWidget(self.item,w)
    	#config
    	dock_apps_list= [a["name"] for a in self.parent.dock_apps]
        Main.setConfig({"dock-apps":dock_apps_list})
class DockAppsList(QListWidget):
    def __init__(self,parent):
        QListWidget.__init__(self,parent)
        self.parent=parent
        self.setStyleSheet("""
        	QListView {
        		border:0px solid #ffffff;
        	}
        	QListView:item {
        		outline:none;
        		selection-background-color:transparent;
        		margin-left:5px;
        		height:50px;
        		color:rgb(40,40,40);
        	}
        	""")
        self.dock_apps=Apps.find_info(self.parent.parent.config["dock-apps"])
        #
        for s in self.dock_apps:
        	i = QListWidgetItem()
        	w= DockAppWidget(self,s,i)
        	self.addItem(i)
        	self.setItemWidget(i,w)
class SecondPage(QScrollArea):
    def __init__(self,parent):
        QScrollArea.__init__(self,parent)
        self.parent=parent

        self.layout=QVBoxLayout(self)

        self.dockApps=DockAppsList(self)
        self.dockApps.resize(self.width(),self.height())
        self.layout.addWidget(self.dockApps)

        self.plusItem=AddButton(self.dockApps)
        self.plusItem.setMaximumHeight(50)
        self.layout.addWidget(self.plusItem)
        self.setLayout(self.layout)

class ThirdPage(QScrollArea):
    def __init__(self,parent):
        QScrollArea.__init__(self,parent)
        self.parent=parent

        self.layout=QVBoxLayout(self)

        self.setLayout(self.layout)