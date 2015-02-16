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

from PyQt4 import QtGui,QtCore
import Xlib
import sys
import subprocess
import os
import dbus
import shutil
import traceback
import Config

#####
####
def dbus_login1(bus):
	bus_object = bus.get_object("org.freedesktop.login1", "/org/freedesktop/login1")
	iface = dbus.Interface(bus_object, 'org.freedesktop.login1.Manager')
	return iface
def dbus_upower(bus):
	bus_object = bus.get_object("org.freedesktop.UPower", "/org/freedesktop/UPower")
	iface = dbus.Interface(bus_object, 'org.freedesktop.UPower')
	return iface
def dbus_consolekit(bus):
	bus_object = bus.get_object("org.freedesktop.ConsoleKit", "/org/freedesktop/ConsoleKit/Manager")
	iface = dbus.Interface(bus_object, 'org.freedesktop.ConsoleKit.Manager')
	return iface
def dbus_lightdm(bus):
	seat_path=os.environ.get('XDG_SEAT_PATH')
	bus_object = bus.get_object("org.freedesktop.DisplayManager", seat_path)
	iface = dbus.Interface(bus_object, 'org.freedesktop.DisplayManager.Seat')
	return iface

def Sleep():
	bus = dbus.SystemBus()
	try:
		i = dbus_login1(bus)
		if i.CanHybridSleep()=="yes":
			print "sleep"
			i.HybridSleep(0)
		elif i.CanHibernate()=="yes":
			print "hibernate"
			i.Hibernate(0)
		elif i.CanSuspend()=="yes":
			print "suspend"
			i.Suspend(0)
		else:
			raise Exception("'org.freedesktop.login1' somehow doesn't work.")
	except:
		print traceback.print_exc()
		print "Trying with org.freedesktop.UPower"
		i=dbus_upower(bus)
		if i.HibernateAllowed():
			print "hibernate"
			i.Hibernate(0)
		elif i.SuspendAllowed():
			print "suspend"
			i.Suspend(0)
		else:
			print "Error: could not sleep, sorry."

def Shutdown():
	bus = dbus.SystemBus()
	try:
		i = dbus_login1(bus)
		if i.CanPowerOff()=="yes":
			print "power off"
			i.PowerOff(0)
		else:
			raise Exception("'org.freedesktop.login1' somehow doesn't work.")
	except:
		print traceback.print_exc()
		i  = dbus_consolekit(bus)
		if i.CanStop():
			print "shutdown"
			i.Stop(0)
		else:
			raise Exception("'org.freedesktop.Consolekit' somehow doesn't work.")
def Reboot():
	bus = dbus.SystemBus()
	try:
		i = dbus_login1(bus)
		if i.CanReboot()=="no":
			print "reboot"
			i.Reboot(0)
		else:
			raise Exception("'org.freedesktop.login1' somehow doesn't work.")
	except:
		print traceback.print_exc()
		i  = dbus_consolekit(bus)
		if i.CanRestart():
			print "reboot"
			i.Restart(0)
		else:
			raise Exception("'org.freedesktop.Consolekit' somehow doesn't work.")
def Logout():
	bus = dbus.SystemBus()
	try:
		i= dbus_lightdm(bus)
		print "switch"
		i.SwitchToGreeter(0)
	except:
		print traceback.print_exc()
####
####
class AreYouSure(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self, None,QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setWindowTitle("ducklauncher!!")
		d = QtGui.QDesktopWidget()
		self.w=350
		self.h=250
		self.height =d.availableGeometry().height()
		self.width =d.availableGeometry().width()
		self.top_pos= d.availableGeometry().y()
		self.r=int(Config.get()["r"])
		self.g=int(Config.get()["g"])
		self.b=int(Config.get()["b"])
		self.state=""
		self.buttonRect=None
		self.drawButtonRect=False
		self.setGeometry(self.width/2-self.w/2,self.height/2-self.h/2+self.top_pos, self.w+3,self.h+3)
	def paintEvent(self, e):
		qp=QtGui.QPainter()
		qp.begin(self)
		qp.setFont(QtGui.QFont(Config.get()["font"],12))
		qp.setRenderHint(QtGui.QPainter.Antialiasing)
		qp.setPen(QtCore.Qt.NoPen)
		#shadows
		qp.setBrush(QtGui.QColor(0,0,0,80))
		qp.drawRoundedRect(QtCore.QRectF(0,2,self.w+1,self.h),3,3)
		qp.setBrush(QtGui.QColor(0,0,0,60))
		qp.drawRoundedRect(QtCore.QRectF(0,1,self.w+2,self.h+2),4,4)
		qp.setBrush(QtGui.QColor(0,0,0,30))
		qp.drawRoundedRect(QtCore.QRectF(0,0,self.w+3,self.h+4),5,5)
		#background
		qp.setBrush(QtGui.QColor(self.r,self.g,self.b))
		qp.drawRect(QtCore.QRectF(0,0,self.w,self.h))
		#title
		if self.drawButtonRect==True and self.buttonRect!=None:
			qp.setPen(QtGui.QColor(0,0,0,0))
			qp.setBrush(QtGui.QColor(254,254,255,50))
			qp.drawRect(self.buttonRect)
			
		textRect=QtCore.QRectF(0,0,self.w,40)
		qp.setPen(QtGui.QColor(250,250,250))
		if self.state=="logout":
			qp.drawText(textRect,QtCore.Qt.AlignCenter,"Log out from your computer?")
			i = QtGui.QIcon("/usr/share/duck-launcher/default-theme/logout.svg")
			i.paint(qp, self.w/2-40,self.h/2-50,80,80)
		if self.state=="restart":
			qp.drawText(textRect,QtCore.Qt.AlignCenter,"Restart your computer?")
			i = QtGui.QIcon("/usr/share/duck-launcher/default-theme/restart.svg")
			i.paint(qp, self.w/2-40,self.h/2-50,80,80)
		if self.state=="shutdown":
			qp.drawText(textRect,QtCore.Qt.AlignCenter,"Shut down your computer?")
			i = QtGui.QIcon("/usr/share/duck-launcher/default-theme/shutdown.svg")
			i.paint(qp, self.w/2-40,self.h/2-50,80,80)
		##Yes No
		qp.drawText(QtCore.QRectF(0,self.h-50,self.w/2-6,50),QtCore.Qt.AlignCenter, "No")
		qp.drawText(QtCore.QRectF(self.w/2+2,self.h-50,self.w/2,50),QtCore.Qt.AlignCenter, "Yes")
	def mouseMoveEvent(self,e):
		self.mousePressEvent(e)
	def mousePressEvent(self,e):
		self.drawButtonRect=False
		if self.h-50<e.y()<self.h:
			if e.x()<self.w/2-6:
				self.drawButtonRect=True
				self.buttonRect=QtCore.QRectF(0,self.h-49,self.w/2,49)
			elif e.x()>self.w/2+2:
				self.drawButtonRect=True
				self.buttonRect=QtCore.QRectF(self.w/2,self.h-49,self.w/2,49)
		self.update()
	def mouseReleaseEvent(self, e):
		self.drawButtonRect=False
		if self.h-50<e.y()<self.h:
			if e.x()<self.w/2-6:
				self.close()
			elif e.x()>self.w/2+2:
				##
				if self.state=="logout":
					Logout()
				elif self.state=="restart":
					Reboot()
				elif self.state=="shutdown":
					Shutdown()
				self.close()
	def update_all(self,conf):
		self.r=int(conf["r"])
		self.g=int(conf["g"])
		self.b=int(conf["b"])
		self.update()
class Window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self, None,QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)#|QtCore.Qt.X11BypassWindowManagerHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setAttribute(QtCore.Qt.WA_X11NetWmWindowTypeDock)
		#Values
		self.conf=Config.get()
		self.size=int(self.conf['size'])
		d = QtGui.QDesktopWidget()
		self.height =d.availableGeometry().height()
		self.top_pos= d.availableGeometry().y()
		self.r=int(self.conf["r"])
		self.g=int(self.conf["g"])
		self.b=int(self.conf["b"])
		self.buttonRect=None
		self.drawButtonRect=False
		self.win_len=4
		self.move(self.size+10,self.height-self.size*1.5-4+self.top_pos)
		self.resize(self.size*self.win_len*1.5,self.size*1.5+3)
		self.sure=AreYouSure()
	def paintEvent(self,e):
		qp=QtGui.QPainter()
		qp.begin(self)
		qp.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
		qp.setPen(QtCore.Qt.NoPen)
		#shadow
		qp.setBrush(QtGui.QColor(0,0,0,60))
		qp.drawRoundedRect(QtCore.QRectF(10,0,self.size*self.win_len*1.3+11,self.size*1.5+2),3,3)
		qp.setBrush(QtGui.QColor(0,0,0,30))
		qp.drawRoundedRect(QtCore.QRectF(8,0,self.size*self.win_len*1.3+13,self.size*1.5+3),4,4)
		#background
		qp.setBrush(QtGui.QColor(int(self.r),int(self.g),int(self.b)))
		qp.drawRect(QtCore.QRectF(10,0,self.size*self.win_len*1.3+10,self.size*1.5))
		qp.setBrush(QtGui.QColor(250,250,250))
		qp.drawRect(9,0,5,self.size*1.5)
		half_height=self.size*1.1
		icon=QtGui.QIcon("/usr/share/duck-launcher/default-theme/win.svg")
		icon.paint(qp, -10,self.size*1.5-22, 20,20)
		if self.drawButtonRect==True and self.buttonRect!=None:
			qp.setPen(QtGui.QColor(0,0,0,0))
			qp.setBrush(QtGui.QColor(254,254,255,50))
			qp.drawRect(self.buttonRect)
		#Sleep
		sl=QtGui.QIcon("/usr/share/duck-launcher/default-theme/sleep.svg")
		sl.paint(qp, 20,10,self.size,self.size)
		#Log out
		lo=QtGui.QIcon("/usr/share/duck-launcher/default-theme/logout.svg")
		lo.paint(qp, self.size*1.3+20,10,self.size,self.size)
		#Restart
		re=QtGui.QIcon("/usr/share/duck-launcher/default-theme/restart.svg")
		re.paint(qp, self.size*2*1.3+20,10,self.size,self.size)
		#Shutdown
		sd=QtGui.QIcon("/usr/share/duck-launcher/default-theme/shutdown.svg")
		sd.paint(qp, self.size*3*1.3+20,10,self.size,self.size)
	def mouseMoveEvent(self,e):
		self.mousePressEvent(e)
	def mousePressEvent(self,e):
		x_m,y_m=e.x(),e.y()
		self.drawButtonRect=False
		if 10<y_m<self.size+10:
			if 20<x_m<self.size+20:
				#sleep
				self.buttonRect=QtCore.QRectF(15,0,self.size+10,self.size*1.5)
				self.drawButtonRect=True
				self.update()
				QtGui.QApplication.processEvents()
			if self.size*1.3+20<x_m<self.size*1.3+20+self.size:
				self.buttonRect=QtCore.QRectF(self.size*1.3+15,0,self.size+10,self.size*1.5)
				self.drawButtonRect=True
				self.update()
				QtGui.QApplication.processEvents()
			if self.size*2*1.3+20<x_m<self.size*2*1.3+20+self.size:
				self.buttonRect=QtCore.QRectF(self.size*2*1.3+15,0,self.size+10,self.size*1.5)
				self.drawButtonRect=True
				self.update()
				QtGui.QApplication.processEvents()
			if self.size*3*1.3+20<x_m<self.size*3*1.3+20+self.size:
				self.buttonRect=QtCore.QRectF(self.size*3*1.3+15,0,self.size+10,self.size*1.5)
				self.drawButtonRect=True
				self.update()
				QtGui.QApplication.processEvents()
	def mouseReleaseEvent(self,e):
		x_m,y_m=e.x(),e.y()
		self.drawButtonRect=False
		if 10<y_m<self.size+10:
			self.close()
			if 20<x_m<self.size+20:
				Sleep()
			if self.size*1.3+20<x_m<self.size*1.3+20+self.size:
				self.sure.state="logout"
				self.sure.show()
			if self.size*2*1.3+20<x_m<self.size*2*1.3+20+self.size:
				self.sure.state="restart"
				self.sure.show()
			if self.size*3*1.3+20<x_m<self.size*3*1.3+20+self.size:
				self.sure.state="shutdown"
				self.sure.show()
			##Update conf
			Config.check_dict(self.conf)
			##Remove duck-launcher image cache
			path = os.path.join(os.path.expanduser("~"),".duck/")
			if os.path.isdir(path):
				shutil.rmtree(path,ignore_errors=True)
			self.sure.update_all(self.conf)
	def update_all(self,conf):
		self.conf=conf
		self.size=int(self.conf['size'])
		self.move(self.size+10,self.height-self.size*1.5-4+self.top_pos)
		self.resize(self.size*self.win_len*1.5,self.size*1.5+3)
		self.r=int(self.conf["r"])
		self.g=int(self.conf["g"])
		self.b=int(self.conf["b"])
		if self.sure.isHidden==False:
			self.sure.update_all(self.conf)
		self.update()
