import os
import sys
sys.dont_write_bytecode=True
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

import webbrowser
import subprocess
import pickle
import dbus
import dbus.service
import dbus.mainloop.glib
from jinja2 import Template
import math
#Import local modules
import Pages
#Imports from Duck Launcher's libs
from duck.launcher import Apps
from duck import datadir
ICON_DIR=datadir.getDir()+"icons/default/"

def getDuckLauncherConfig():
	config={}
	iface=None
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	# Get the session bus
	bus = dbus.SessionBus()
	 
	try:
		# Get the remote object
		remote_object = bus.get_object("org.duck.Launcher","/DBusWidget")		
		# Get the remote interface for the remote object
		iface = dbus.Interface(remote_object, "org.duck.Launcher")
		config["r1"]=int(iface.getR1())
		config["g1"]=int(iface.getG1())
		config["b1"]=int(iface.getB1())
		config["r2"]=int(iface.getR2())
		config["g2"]=int(iface.getG2())
		config["b2"]=int(iface.getB2())
		config["alpha"]=int(iface.getAlpha())
		config["font"]=str(iface.getFont())
		config["font-r"]=str(iface.getFontR())
		config["font-g"]=str(iface.getFontG())
		config["font-b"]=str(iface.getFontB())
		config["size"]=int(iface.getLauncherWidth())
		config["icon-size"]=int(iface.getIconSize())
		config["animation-speed"]=int(iface.getAnimationSpeed())
		config["dock-apps"]=[str(d) for d in iface.getDockApps()]
		config["blocks"]=pickle.loads(str(iface.getBlocks()))
	except Exception as e:
		print e
	return config
def setConfig(*args):
	# Enable glib main loop support
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	# Get the session bus
	bus = dbus.SessionBus()
	try:
		# Get the remote object
		remote_object = bus.get_object("org.duck.Launcher","/DBusWidget")
		# Get the remote interface for the remote object
		iface = dbus.Interface(remote_object, "org.duck.Launcher")
	except dbus.DBusException:
		print_exc()
    		sys.exit(1)
						
	for arg in args:
		if arg.has_key('r1'):
			iface.setR1(arg["r1"])
		elif arg.has_key('g1'):
			iface.setG1(arg["g1"])
		elif arg.has_key('b1'):
			iface.setB1(arg["b1"])
		elif arg.has_key('r2'):
			iface.setR2(arg["r2"])
		elif arg.has_key('b2'):
			iface.setB2(arg["b2"])
		elif arg.has_key('g2'):
			iface.setG2(arg["g2"])
		elif arg.has_key('alpha'):
			iface.setAlpha(arg["alpha"])
		elif arg.has_key("size"):
			iface.setLauncherWidth(arg["size"])
		elif arg.has_key("icon-size"):
			iface.setIconSize(int(arg["icon-size"]))
		elif arg.has_key("font"):
			iface.setFont(arg["font"])
		elif arg.has_key("font-r"):
			iface.setFontR(arg["font-r"])
		elif arg.has_key("font-g"):
			iface.setFontG(arg["font-g"])
		elif arg.has_key("font-b"):
			iface.setFontB(arg["font-b"])
		elif arg.has_key("animation-speed"):
			iface.setAnimationSpeed(arg["animation-speed"])
		elif arg.has_key("dock-apps"):
			if arg["dock-apps"]==[]:
				arg["dock-apps"]=None
			iface.setDockApps(arg["dock-apps"])
		elif arg.has_key("blocks"):
			new_blocks=[]
			for b in arg["blocks"]:
				if not b["apps"] or b.has_key("apps")==False:
					b["apps"]=[]
				if not b["files"] or b.has_key("files")==False:
					b["files"]=[]
				if not b["directories"] or b.has_key("directories")==False:
					b["directories"]=[]
				new_blocks.append(b)
			new_blocks_pickle = pickle.dumps(new_blocks)
			iface.setBlocks(new_blocks_pickle)
			Dict={
				"r":iface.getR1(),
				"g":iface.getG1(),
				"b":iface.getB1(),
				"r2":iface.getR2(),
				"g2":iface.getG2(),
				"b2":iface.getB2(),
				"alpha":iface.getAlpha(),
				"font":iface.getFont(),
				"font-b":iface.getFontR(),
				"font-g":iface.getFontG(),
				"font-r":iface.getFontB(),
				"animation-speed":iface.getAnimationSpeed(),
				"size":iface.getLauncherWidth(),
				"dock-apps":iface.getDockApps(),
				"icon-size":iface.getIconSize(),
				"blocks":iface.getBlocks(),
				"init-manager":iface.getInit()
				}
			d_cfg.check_dict(Dict)
########
## Widgets
########
class ResizeButton(QWidget):
	def __init__(self,parent):
		QWidget.__init__(self,parent)
		self.parent=parent
		self.setCursor(QCursor(Qt.SizeFDiagCursor))
		#
		self.moving=False
		self.offset=None
	def paintEvent(self,e):
		qp = QPainter()
		qp.begin(self)
		qp.fillRect(e.rect(), Qt.transparent)
		qp.setRenderHints(QPainter.Antialiasing |QPainter.SmoothPixmapTransform)

		qp.setPen(Qt.NoPen)
		qp.setBrush(QColor(self.parent.red,self.parent.green,self.parent.blue))
		r = e.rect()
		qp.drawPolygon(QPoint(0,r.height()),QPoint(r.width(),0),QPoint(r.width(),r.height()))
	def mousePressEvent(self,e):
		if e.button()==Qt.LeftButton:
			self.moving=True
			self.offset=e.pos()
	def mouseMoveEvent(self,e):
		if self.moving==True and self.parent.width()>300 and self.parent.height()>200:
			p = e.pos()-self.offset
			x=self.parent.width()+p.x()
			y=self.parent.height()+p.y()
			self.parent.resize(x,y)
		if self.parent.width()<=300:
			self.parent.resize(303,self.parent.height())
		if self.parent.height()<=200:
			self.parent.resize(self.parent.width(),202)
class PicButton(QPushButton):
	def __init__(self,parent, pixmap):
		QPushButton.__init__(self,parent)
		self.pixmap = pixmap
		self.setFlat(True)
		self.setIcon(QIcon(pixmap))
		self.setStyleSheet('''QPushButton {background-color: rgba(0,0,0,0);border:none;outline:none;}
					QPushButton:hover {background-color: rgba(30,30,30,20)}
					QPushButton:pressed {background-color: rgba(30,30,30,40)}''')
	def sizeHint(self):
		return self.pixmap.size()
class TitleBar(QWidget):
	def __init__(self,parent):
		QWidget.__init__(self,parent)
		self.parent=parent
		self.titleContent="Duck Launcher Settings"
		self.titleRectShadow=QRect(11,1,250,25)
		self.titleRect=QRect(10,0,250,25)
		#
		self.moving=False
		self.offset=None
		#
		self.closeButton=PicButton(self,"{}remove.svg".format(ICON_DIR))
		self.closeButton.setGeometry(self.parent.width()-30,0,25,26)
		self.closeButton.setIconSize(QSize(12,12))
		self.closeButton.clicked.connect(self.closeWindow)
		self.closeButton.show()

		self.maxButton=PicButton(self,"{}open.svg".format(ICON_DIR))
		self.maxButton.setGeometry(self.parent.width()-55,0,25,26)
		self.maxButton.setIconSize(QSize(12,12))
		self.maxButton.clicked.connect(self.maximizeWindow)
		self.maxButton.show()

		self.minButton=PicButton(self,"{}minimize.svg".format(ICON_DIR))
		self.minButton.setGeometry(self.parent.width()-80,0,25,26)
		self.minButton.setIconSize(QSize(12,12))
		self.minButton.clicked.connect(self.minimizeWindow)
		self.minButton.show()
	def paintEvent(self,e):
		qp = QPainter()
		qp.begin(self)
		qp.fillRect(e.rect(), Qt.transparent)
		qp.setRenderHints(QPainter.Antialiasing |QPainter.SmoothPixmapTransform)

		qp.setPen(Qt.NoPen)
		qp.setBrush(QColor(self.parent.red,self.parent.green,self.parent.blue))
		qp.drawRect(e.rect())
		qp.setPen(QColor(0,0,0,30))
		qp.setFont(QFont("Droid Sans",10))
		qp.drawText(self.titleRectShadow,Qt.AlignVCenter,self.titleContent)
		qp.setPen(QColor(255,255,255,255))
		qp.drawText(self.titleRect,Qt.AlignVCenter,self.titleContent)
	def mousePressEvent(self,e):
		if e.button()== Qt.LeftButton and e.y()<25:
			self.moving=True
			self.offset=e.pos()
			self.setCursor(Qt.ClosedHandCursor)
	def mouseMoveEvent(self,e):
		if self.moving:
			self.parent.move(e.globalPos()-self.offset)
	def mouseReleaseEvent(self,e):
		self.setCursor(Qt.ArrowCursor)
	def resizeEvent(self,e):
		self.closeButton.move(self.width()-30,0)
		self.maxButton.move(self.width()-55,0)
		self.minButton.move(self.width()-80,0)
	def closeWindow(self):
		self.parent.close()
	def maximizeWindow(self):
		if self.parent.windowState()==Qt.WindowNoState:
			self.parent.setWindowState(Qt.WindowMaximized)
		elif self.parent.windowState()==Qt.WindowMaximized:
			self.parent.setWindowState(Qt.WindowNoState)
	def minimizeWindow(self):
		self.parent.setWindowState(Qt.WindowMinimized)
class PagesBar(QWidget):
	def __init__(self,parent):
		QWidget.__init__(self,parent)
		self.parent=parent
		self.setContentsMargins(10,0,10,0)
		self.setStyleSheet("""
			QPushButton {
				height:25px;
				margin:0px;
				margin-left:10px;
				margin-right:10px;
				background-color:transparent;
				border:solid;
				border-color:transparent;
				color:rgba(255,255,255,230);
				border-width:0px;
				border-bottom-width:0px;
				border-bottom-color:rgba(255,255,255,230);
				outline:none;
			}
			QPushButton:hover {
				border-bottom-width:1px;

			}
			""")
		self.inactiveButtonStyle="QPushButton {border-bottom-width:0px} QPushButton:hover {border-bottom-width:1px}"
		#
		self.layout = QHBoxLayout(self)
		self.layout.setContentsMargins(0,0,0,0)


		self.btn1=QPushButton("Appearance")
		self.btn1.setStyleSheet("border-bottom-width:3px;")
		#self.btn1.setIcon(QIcon("/usr/share/duck-launcher/default-theme/appearance.svg"))
		self.btn1.clicked.connect(self.setToFirstPage)
		self.layout.addWidget(self.btn1)

		self.btn2=QPushButton("Dock Apps")
		self.btn2.clicked.connect(self.setToSecondPage)
		#self.btn2.setIcon(QIcon("/usr/share/duck-launcher/default-theme/dock-apps.svg"))
		self.layout.addWidget(self.btn2)

		self.btn3=QPushButton("Favourites")
		#self.btn3.setIcon(QIcon("/usr/share/duck-launcher/default-theme/star.svg"))
		self.btn3.clicked.connect(self.setToThirdPage)
		self.layout.addWidget(self.btn3)


		self.setLayout(self.layout)
	def setToFirstPage(self):
		self.btn1.setStyleSheet("border-bottom-width:2px;")
		self.btn2.setStyleSheet(self.inactiveButtonStyle)
		self.btn3.setStyleSheet(self.inactiveButtonStyle)

		self.parent.firstpage.show()
		self.parent.secondpage.hide()
		self.parent.thirdpage.hide()
	def setToSecondPage(self):
		self.btn2.setStyleSheet("border-bottom-width:2px;")
		self.btn1.setStyleSheet(self.inactiveButtonStyle)
		self.btn3.setStyleSheet(self.inactiveButtonStyle)

		self.parent.secondpage.show()
		self.parent.firstpage.hide()
		self.parent.thirdpage.hide()
	def setToThirdPage(self):
		self.btn3.setStyleSheet("border-bottom-width:2px;")
		self.btn1.setStyleSheet(self.inactiveButtonStyle)
		self.btn2.setStyleSheet(self.inactiveButtonStyle)

		self.parent.thirdpage.show()
		self.parent.secondpage.hide()
		self.parent.firstpage.hide()
	def paintEvent(self,e):
		qp = QPainter()
		qp.begin(self)
		qp.fillRect(e.rect(), Qt.transparent)
		qp.setRenderHints(QPainter.Antialiasing |QPainter.SmoothPixmapTransform)

		qp.setPen(Qt.NoPen)
		qp.setBrush(QColor(self.parent.red,self.parent.green,self.parent.blue))
		qp.drawRect(e.rect())
class Container(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		#self.setAttribute(Qt.WA_TranslucentBackground, True)
		#self.setAttribute(Qt.WA_X11NetWmWindowTypeDock, True)
		self.setWindowTitle("Duck Launcher Settings")
		self.setWindowIcon(QIcon().fromTheme("duck-settings"))
		self.setWindowFlags(Qt.CustomizeWindowHint)
		self.resize(650,500)
		self.setStyleSheet("""
			QWidget {
				background-color:#ffffff
			}
			QScrollArea {
        		background-color:#ffffff;
        		border:solid;
        		border-color:transparent;
        		margin-left:20px;
        		margin-right:20px;
        	}
        	QLabel {
        		color:rgb(65,65,65)
        	}
        	QSlider::groove:horizontal {
        		border:1px solid #fff;
        		background:white;
        		height:10px;

        	}
        	QSlider::sub-page:horizontal {
        		background:rgb(80,80,80);
        		margin-top:4px;
        		margin-bottom:4px;
        	}
        	QSlider::add-page:horizontal {
        		background:rgb(255,255,255);
        	}
        	QSlider::handle:horizontal {
        		background:rgb(100,100,100);
        		border-radius:20px;
        		margin-left:4px;
        		margin-right:4px;
        	}
        	QSlider::groove:vertical {
        		border:1px solid #fff;
        		background:white;
        		width:10px;

        	}
        	QSlider::sub-page:vertical {
        		background:rgb(80,80,80);
        		margin-left:4px;
        		margin-right:4px;
        	}
        	QSlider::add-page:vertical {
        		background:rgb(255,255,255);
        	}
        	QSlider::handle:vertical {
        		background:rgb(100,100,100);
        		border-radius:20px;
        		margin-top:4px;
        		margin-bottom:4px;
        	}
        	QSpinBox {
        		border-style:solid;
        		border-width:1px;
        		border-radius:1px;
        		border-color:rgb(80,80,80);

        	}
        	QSpinBox:up-button {
        		subcontrol-origin: border;
     			subcontrol-position: top right;
     			background-color:rgb(80,80,80);
        		border-style:solid;
        		border-color:rgb(80,80,80);
        	}
        	QSpinBox:up-arrow {image:url("""+ICON_DIR+"""up.png);}
        	QSpinBox:down-button {
        		subcontrol-origin: border;
     			subcontrol-position: bottom right;
     			background-color:rgb(80,80,80);
        		border-style:solid;
        		border-color:rgb(80,80,80);
        	}
        	QSpinBox:down-arrow {image:url("""+ICON_DIR+"""down.png);}
        	QDoubleSpinBox {
        		border-style:solid;
        		border-width:1px;
        		border-radius:1px;
        		border-color:rgb(80,80,80);

        	}
        	QDoubleSpinBox:up-button {
        		subcontrol-origin: border;
     			subcontrol-position: top right;
     			background-color:rgb(80,80,80);
        		border-style:solid;
        		border-color:rgb(80,80,80);
        	}
        	QDoubleSpinBox:up-arrow {image:url("""+ICON_DIR+"""up.png);}
        	QDoubleSpinBox:down-button {
        		subcontrol-origin: border;
     			subcontrol-position: bottom right;
     			background-color:rgb(80,80,80);
        		border-style:solid;
        		border-color:rgb(80,80,80);
        	}
        	QDoubleSpinBox:down-arrow {image:url("""+ICON_DIR+"""down.png);}
        	QComboBox {
        		border-style:solid;
        		border-width:1px;
        		border-radius:1px;
        		border-color:rgb(80,80,80);
        		selection-background-color:rgb(100,100,100)
        	}
        	QComboBox:drop-down {
        		background-color:rgb(80,80,80);
        	}
        	QComboBox:down-arrow {
        		image:url("""+ICON_DIR+"""down.png);
        	}
        	QComboBox QAbstractItemView {
        		border:2px solid rgb(80,80,80);
        		selection-background-color:rgb(150,150,150);
        	}
			""")
		#Values
		self.config=getDuckLauncherConfig()
		if self.config!=None:
			self.red=int(self.config["r1"])
			self.green=int(self.config["g1"])
			self.blue=int(self.config["b1"])
		#Title Bar
		self.titlebar=TitleBar(self)
		self.titlebar.setGeometry(0,0,self.width(),25)
		self.titlebar.show()
		#Bar showing the three pages
		self.pagesbar = PagesBar(self)
		self.pagesbar.setGeometry(0,25,self.width(),25)
		self.pagesbar.show()
		##
		self.firstpage=Pages.FirstPage(self)
		self.firstpage.setGeometry(0,50,self.width(),self.height()-40)
		self.firstpage.show()
		#
		self.secondpage=Pages.SecondPage(self)
		self.secondpage.setGeometry(0,50,self.width(),self.height()-40)
		self.secondpage.hide()
		#
		self.thirdpage=Pages.ThirdPage(self)
		self.thirdpage.setGeometry(0,50,self.width(),self.height()-40)
		self.thirdpage.hide()		
		#Resize Button
		self.resizer=ResizeButton(self)
		self.resizer.setGeometry(self.width()-8,self.height()-8,8,8)
		self.resizer.show()

	def resizeEvent(self,e):
		self.titlebar.resize(self.width(),25)
		self.pagesbar.resize(self.width(),25)
		self.firstpage.resize(self.width(),self.height()-50)
		self.secondpage.resize(self.width(),self.height()-50)
		self.thirdpage.resize(self.width(),self.height()-50)
		self.resizer.move(self.width()-8,self.height()-8)
if __name__=="__main__":
	app = QApplication(sys.argv)
	w = Container()
	w.show()
	sys.exit(app.exec_())