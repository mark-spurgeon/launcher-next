#! /usr/bin/python
# -*- coding: utf-8 -*-
#########
#########
#Copyright (C) 2014-2015  Mark Spurgeon <theduck.dev@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import os
import webbrowser
import notify2 
import subprocess
import Files
import Plugins
import Apps

class Launch(QThread):
	def __init__(self,parent=None):
		QThread.__init__(self,parent)
		self.app=""
		self.parent=parent
	def run(self):
		exec_list=self.app.split(" ")
		subprocess.call(exec_list)
		QApplication.processEvents()

class installPlugin(QThread):
	def __init__(self,parent=None):
		QThread.__init__(self,parent)
		self.plugin=""
		self.parent=parent
	def run(self):
		rep=Plugins.Repo()
		rep.installPlugin(str(self.plugin))
		QApplication.processEvents()
class removePlugin(QThread):
	def __init__(self,parent=None):
		QThread.__init__(self,parent)
		self.plugin=""
		self.parent=parent
	def run(self):
		rep=Plugins.Repo()
		rep.removePlugin(str(self.plugin))
		QApplication.processEvents()


class imgWidget(QWidget):
	def __init__(self,parent=None,img=None):
		QWidget.__init__(self,parent)
		self.img=img
		self.ico=QtGui.QIcon(self.img)
		self.setUpdatesEnabled(True)
		self.pixmap_opacity=0.0
	def showEvent(self,e):
		self.timeline =QTimeLine()
		self.timeline.valueChanged.connect(self.animate)
		self.timeline.finished.connect(self.animateFinished)
		self.timeline.setDuration(200)
		self.timeline.start()
	def hideEvent(self,e):
		self.pixmap_opacity=0
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		qp.setClipRegion(event.region())
		qp.setOpacity(self.pixmap_opacity)
		qp.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
		qp.fillRect(event.rect(), QtCore.Qt.transparent)
		if self.ico!=None:
			self.ico.paint(qp,event.rect())
		else:
			pass
		qp.end()

	def sizeHint(self):
		return QtCore.QSize(100, 100)
	def moveEvent(self,e):
		pass
	def animate(self,val):
		self.pixmap_opacity +=0.3
		if self.pixmap_opacity>1:
			self.pixmap_opacity=1
		self.repaint()
		QtGui.qApp.processEvents()
	def animateFinished(self):
		self.pixmap_opacity=1
		self.repaint()
		QtGui.qApp.processEvents()
class WebPluginFactory(QWebPluginFactory):

    def __init__(self, parent = None):
        QWebPluginFactory.__init__(self, parent)
    def create(self, mimeType, url, names, values):
        if mimeType == "duck/image":
        	src=url
        	
        	return imgWidget(img=src)
    
    def plugins(self):
        plugin = QWebPluginFactory.Plugin()
        plugin.name = "Duck image"
        plugin.description = "Lets all the svg files to be rendered"
        mimeType = QWebPluginFactory.MimeType()
        mimeType.name = "duck/image"
        mimeType.description = "PyQt widget"
        mimeType.fileExtensions = ["JPG"]
        plugin.mimeTypes = [mimeType]
        return [plugin]

class pluginView(QWebView):
	def __init__(self, parent = None):
		QWebView.__init__(self, parent)
		self.parent=parent
		self.thePage = self.page()
		self.theFrame=self.thePage.mainFrame()
		#Transparency
		palette = self.palette()
		palette.setBrush(QPalette.Base, Qt.transparent)
		self.thePage.setPalette(palette)
		#
		self.thePage.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
		self.theFrame.javaScriptWindowObjectCleared.connect(self._populateJavaScriptWindowObject)
		self.setAttribute(Qt.WA_OpaquePaintEvent, False)
		self.setContextMenuPolicy(Qt.NoContextMenu)
		self.connect(self, SIGNAL("linkClicked(const QUrl&)"), self._linkClicked)
		self.setHtml("<body style='background:rgb(230,100,80);'><input type='text' placehodler='aaa'></input></body>")
		self.hide()	

		#self.factory=WebPluginFactory()
		#self.thePage.setPluginFactory(self.factory)
	def showEvent(self,e):
		palette = self.palette()
		palette.setBrush(QPalette.Base, Qt.transparent)
		self.thePage.setPalette(palette)
		self.parent.setAttribute(Qt.WA_X11NetWmWindowTypeDock,False)
		self.setAttribute(Qt.WA_X11NetWmWindowTypeDock,False)
		self.parent.update()
		self.update()
	def _linkClicked(self, url):
		str_url=str(url.toString())
		#Links are all external, for now.
		webbrowser.open(str(url.toString()))
		self.parent.close_it()
	def _populateJavaScriptWindowObject(self):
		self.theFrame.addToJavaScriptWindowObject('Duck', self)
	@pyqtSlot()
	def submitForm(self):
		elements=[]
		for e in self.theFrame.findAllElements("*"):
			el={}
			el["type"] = str(e.localName())
			if e.hasAttribute("id"):
				el["id"]=str(e.attribute("id"))
			if e.hasAttribute("name"):
				el["name"]=str(e.attribute("name"))
			val= e.evaluateJavaScript('this.value').toPyObject()
			if val!=None:
				el["value"]=val
			elements.append(el)


		if "#" in self.parent.current_text.split(" ")[0]:
			plugins_list=[]						
			for p in Plugins.get_plugin_names():
				if str(self.parent.current_text.split(" ")[0]).lower().replace("#","") in p:
					plugins_list.append(p)
			if plugins_list:
				plugin_name=plugins_list[0]
				pl=Plugins.getCurrentPluginModule(plugin_name)
				try:
					pl.onFormSubmit(elements)
				except:
					print("[Duck Launcher] No 'onFormSubmit()' method present in the plugin.")
	@pyqtSlot(str,str)
	def sendData(self, thing, value):
		print "data : " , thing, value
		if "#" in self.parent.current_text.split(" ")[0]:
			plugins_list=[]						
			for p in Plugins.get_plugin_names():
				if str(self.parent.current_text.split(" ")[0]).lower().replace("#","") in p:
					plugins_list.append(p)
			if plugins_list:
				plugin_name=plugins_list[0]	
				pl=Plugins.getCurrentPluginModule(plugin_name)
				try:
					pl.onDataSent(thing, value)
				except:
					print("[Duck Launcher] No 'onDataSent()' method present in the plugin.")
	@pyqtSlot(str)
	def _filesGetFromPath(self,path):
		if str(self.parent.current_text).lower().startswith("#files"):
			if os.path.isdir(path):
				stuff = Files.getFilesFromPath(path)
			elif path=="HOME":
				home=os.path.expanduser("~")
				stuff= Files.getFilesFromPath(home)
			else:
				stuff=[]
			self.theFrame.evaluateJavaScript("setNewFiles({})".format(stuff))
	@pyqtSlot(str)
	def _pluginInstallPlugin(self,plugin):
		notify2.init("duck-launcher")
		n=notify2.Notification("Installing this plugin: '{}'".format(plugin),
			"Duck Launcher",
			"dialog-information")
		n.show()
		self.parent.close_it()
		t = installPlugin(parent=self.parent)
		t.plugin=plugin
		t.start()
		self.parent.close_it()
	@pyqtSlot(str)
	def _pluginRemovePlugin(self,plugin):
		notify2.init("duck-launcher")
		n=notify2.Notification("Removing this plugin: '{}'".format(plugin),
			"Duck Launcher",
			"dialog-information")
		n.show()
		self.parent.close_it()
		t = removePlugin(parent=self.parent)
		t.plugin=plugin
		t.start()
class customScrollBar(QScrollBar):
	def __init__(self,parent): 
		QScrollBar.__init__(self)
		self.setTracking(True)
		self.parent=parent
	def paintEvent(self,e):
		qp=QPainter(self)
		qp.fillRect(e.rect(), Qt.transparent)
		qp.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
		qp.setPen(Qt.NoPen)
		qp.setBrush(QColor(self.parent.parent.fg_color[0],self.parent.parent.fg_color[1],self.parent.parent.fg_color[2]))
		d = float(self.maximum())/float(self.height()-200)
		if d!=0:
			qp.drawRect(0,self.value()/d,self.width(),200)
		else:
			pass
class appItem(QStandardItem):
	def __init__(self,parent, app): 
		QStandardItem.__init__(self)
		self.parent=parent
		self.app=app#dict
		self.setText(self.app["name"])
		self.setIcon(QIcon(Apps.ico_from_name(self.app["icon"])))
		self.setEditable(False)
		self.setSizeHint(QSize(self.parent.size*2,self.parent.size*2))
		self.setFont(QFont(self.parent.font))
		self.setData(self.app["exec"],Qt.UserRole+1)
class AppList(QListView): 
    def __init__(self, parent): 
        QListView.__init__(self, parent)
        #Values
        self.parent=parent
        self.mousepos=None
        self.size=60
    	self.bg_r=5
    	self.bg_g=5
    	self.bg_b=5
        self.r=255
        self.g=255
        self.b=255
        #
       	self.scrollbar=customScrollBar(self)
        self.setVerticalScrollBar(self.scrollbar)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setMovement(QListView.Static)
        self.setUniformItemSizes(True)
        self.setGridSize(QSize(self.size*2+5,self.size*2+5))
        self.setIconSize(QSize(self.size,self.size))
        self.setSelectionRectVisible(False)
        self.clicked.connect(self.appClicked)
        self.model=QStandardItemModel(self)
        self.setModel(self.model)
        #self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        #
        self.updateStyle()
        #
        self.update()
    def setApps(self,apps):
    	self.model.clear()
        for o in apps:
        	item=appItem(self,o)
        	self.model.appendRow(item)   
        #self.model.update()
        self.update()
    def setAppIconSize(self, ico):
    	self.size=ico
        self.setGridSize(QSize(ico*2+5,ico*2+5))
        self.setIconSize(QSize(ico,ico))
        self.update()   
    def setFont(self, f):
    	self.font=f
    	self.update()
    def setFontColor(self, r,g,b):
    	self.r=r
    	self.g=g
    	self.b=b
    	self.updateStyle()
    def setBackgroundColor(self, r,g,b):
    	self.bg_r=r
    	self.bg_g=g
    	self.bg_b=b
    	self.updateStyle()
    def updateStyle(self):
    	self.style="""
        		QListView {{ background-color:transparent;show-decoration-selected: 1;}}
        		QListView::item {{ background-color: transparent; color:rgb({red},{green},{blue});padding:8px}}
        		QListView::item:hover {{ background-color: rgba({red},{green},{blue},20); color:rgb({red},{green},{blue});}}
        		QListView::item:selected {{ background-color: rgba({red},{green},{blue},50); color:rgb({red},{green},{blue});}}
        		QScrollBar:vertical {{border:none;width:3px;background-color:rgb({red},{green},{blue});margin: 0px 0px 0px 0px; }}
        	""".format(red=self.parent.conf["font-r"],green=self.parent.conf["font-g"],blue=self.parent.conf["font-b"],bg_red=self.parent.conf["r"],bg_green=self.parent.conf["g"],bg_blue=self.parent.conf["b"])
        self.setStyleSheet(self.style)
        self.font=self.parent.conf["font"]
        self.update()
    def appClicked(self,index):
    	item = self.model.itemFromIndex(index)
    	data = self.model.itemData(index)
    	_exec = str(data[Qt.UserRole+1].toString())
    	#ex_l = _exec.split(" ")
    	#self.setApps([])
    	#subprocess.call(ex_l)
    	t = Launch(self)
    	t.app=_exec
    	t.start()
    	self.hide()
    	self.parent.close_it()
    def mouseMoveEvent(self,e):
    	if self.mousepos!=None:
    		delta=e.globalY()-self.mousepos
    		new_val=self.scrollbar.value()-delta*2
    		self.scrollbar.setValue(new_val)
    		self.mousepos=None
    	else:
    		self.mousepos=e.globalY()