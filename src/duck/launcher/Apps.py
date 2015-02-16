#! /usr/bin/python
# -*- coding: utf-8 -*-
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
import Config

import os
from PyQt4.QtGui import QIcon
import glob
from xdg import DesktopEntry as _d
from xdg import IconTheme
import gtk


from duck import datadir
ICON_DIR=datadir.getDir()+"icons/default/"


app_dirs= [ "/usr/share/applications/*.desktop",
		"/usr/share/applications/kde4/*.desktop",
		"{}/.local/share/applications/*.desktop".format(os.path.expanduser("~"))]

def info(filter_):
	appList=[]
	all_apps=[]
	for d in app_dirs:
		ap=glob.glob(d)
		all_apps+=ap
	for f in all_apps:
		f=unicode(f)
		desk = _d.DesktopEntry(f)
		try:
			dName=str(desk.getName())
			if filter_ !="" and filter_.lower() in dName.lower():
				show=True
			elif filter_=='':
				show=True
			else:show=False
			
			if show==True:
				showTerminal= desk.getTerminal()
				dNotShowIn= desk.getNotShowIn()
				dNoDisplay = desk.getNoDisplay()
				dHidden = desk.getHidden()
				dType = desk.getType()
				dIcon = desk.getIcon()
				if dNoDisplay==False and dHidden==False and dType=="Application" and os.environ.get("XDG_CURRENT_DESKTOP") not in dNotShowIn:  
					app={}
					OnlyShowIn =  desk.getOnlyShowIn()
					current_desk=os.environ.get('XDG_CURRENT_DESKTOP')
					if len(OnlyShowIn)==0 or current_desk in OnlyShowIn:
						app["name"]=str(desk.getName())
						e = str(desk.getExec())
						#prevent '"' in exec
						if e[0] == '"' and e[-1] == '"':
							e = e[:-1][1:]
						try:
							pos= e.index("%")
							e= e[:pos-1]
						except:
							pass
						if showTerminal==True:
							app["exec"]="xterm -e {}".format(e)
						else:
							app["exec"]=e
						app["icon"]=str(dIcon)
						app["icon_path"]=ico_from_name(str(dIcon))
						appList.append(app)
					else:pass
				else:
					pass
			else:
				pass
		except:
			pass
	return sorted(appList,key=lambda x:x["name"].lower())
def ico_from_name(name,size="small"):
	icon_theme = gtk.icon_theme_get_default()
	icon_=icon_theme.lookup_icon(name, 48, 0).get_filename()
	if icon_!=None and isinstance(icon_,basestring):
		return str(icon_)
	elif os.path.isfile(name):
		return str(name)
	else:
		found=False 
		dir_list=IconTheme.icondirs
		for d in dir_list:
			if os.path.isdir(d):
				for i in os.listdir(d)[::-1]:
					if i.startswith(name):
						path=os.path.join(d,i)
						found=True
						break
		if found==True:
			return str(path)
		else:
			return ICON_DIR+"apps.svg"
def ico_from_app(app_name):
	i = info(app_name)
	if len(i)>0:
		if app_name.lower() in i[0]["name"].lower():
			return i[0]["icon_path"]
		else:
			return None
	else:
		return None
def find_info(apps):
	a_list=[]
	if isinstance(apps,list):
		for a in apps:
			i = info(str(a))
			if isinstance(i,list) and len(i)>0:
				for l in i:
					if str(l["name"])==str(a):
						a_list.append(l)
			else:
				Config.removeFromDockApps(a)
	return a_list
