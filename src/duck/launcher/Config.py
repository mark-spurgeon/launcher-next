import os
import defaultConfig
import Apps
import dbus
import yaml
CONFIG={}
defaultDict=defaultConfig.Dict
def check_dict(d):
	new_d={}
	if d.has_key("r"):
		new_d["r"]=int(d["r"])
	else:
		new_d["r"]=int(defaultDict["r"])
	if d.has_key("g"):
		new_d["g"]=int(d["g"])
	else:
		new_d["g"]=int(defaultDict["g"])
	if d.has_key("b"):
		new_d["b"]=int(d["b"])
	else:
		new_d["b"]=int(defaultDict["b"])
	if d.has_key("r2"):
		new_d["r2"]=int(d["r2"])
	else:
		new_d["r2"]=int(defaultDict["r2"])
	if d.has_key("g2"):
		new_d["g2"]=int(d["g2"])
	else:
		new_d["g2"]=int(defaultDict["g2"])
	if d.has_key("b2"):
		new_d["b2"]=int(d["b2"])
	else:
		new_d["b2"]=int(defaultDict["b2"])
	if d.has_key("icon-size"):
		new_d["icon-size"]=int(d["icon-size"])
	else:
		new_d["icon-size"]=int(defaultDict["icon-size"])
	if d.has_key("size"):
		new_d["size"]=int(d["size"])
	else:
		new_d["size"]=int(defaultDict["size"])
	if d.has_key("alpha"):
		new_d["alpha"]=int(d["alpha"])
	else:
		new_d["alpha"]=int(defaultDict["alpha"])
	if d.has_key("animation-speed"):
		new_d["animation-speed"]=float(d["animation-speed"])
	else:
		new_d["animation-speed"]=float(defaultDict["animation-speed"])
	if d.has_key("dock-apps"):
		new_d["dock-apps"]=[]
		for n in d["dock-apps"]:
			new_d["dock-apps"].append(str(n))
	else:
		new_d["dock-apps"]=list(defaultDict["dock-apps"])
	if d.has_key("blocks"):
		new_d["blocks"]=str(d["blocks"])
	else:
		new_d["blocks"]=list(defaultDict["blocks"])
	if d.has_key("font"):
		new_d["font"]=str(d["font"])
	else:
		new_d["font"]=str(defaultDict["font"])
	if d.has_key("font-r"):
		new_d["font-r"]=int(d["font-r"])
	else:
		new_d["font-r"]=int(defaultDict["font-r"])
	if d.has_key("font-g"):
		new_d["font-g"]=int(d["font-g"])
	else:
		new_d["font-g"]=int(defaultDict["font-g"])
	if d.has_key("font-b"):
		new_d["font-b"]=int(d["font-b"])
	else:
		new_d["font-b"]=int(defaultDict["font-b"])
	if d.has_key("init-manager"):
		new_d["init-manager"]=str(d["init-manager"])
	else:
		new_d["init-manager"]=str(defaultDict["init-manager"])
	create_from_info(new_d)
	return d
def create_from_info(_dict):
	HOME = os.path.expanduser("~")
	_dir =os.environ.get('XDG_CONFIG_HOME',os.path.join(HOME,'.config'))
	cfg= _dir+'/duck-launcher.config'
	the_file=open(cfg,"wb")
	d = yaml.dump(_dict)
	the_file.write(d)
	the_file.close()
def get():
	global CONFIG
	HOME = os.path.expanduser("~")
	_dir =os.environ.get('XDG_CONFIG_HOME',os.path.join(HOME,'.config'))
	cfg= _dir+'/duck-launcher.config'
	if "duck-launcher.config" not in os.listdir(_dir):
		create_from_info(defaultDict)
	the_file=open(cfg,"rb")
	try:
		theDict=yaml.load(the_file)
		if isinstance(theDict, basestring): 
			raise Exception
		else:
			CONFIG=theDict
	except:
		if CONFIG!={}:
			theDict=CONFIG
		else:
			theDict=defaultDict
	the_file.close()
	return check_dict(theDict)
def get_from_block(block):
	_all=[]
	if block.has_key("apps"):
		for f in block['apps']:
			i = Apps.info(f)
			if len(i)>0:
				data = {}
				data['value']=f
				data['type']='app'
				_all.append(data)
	if block.has_key("directories"):
		for f in block['directories']:
			if os.path.isdir(str(f)):
				data = {}
				data['value']=f
				data['type']='directory'
				_all.append(data)
	if block.has_key("files"):
		for f in block['files']:
			if os.path.isfile(str(f)):
				data = {}
				data['value']=f
				data['type']='file'
				_all.append(data)
	return _all
def removeFromDockApps(a):
	conf = get()
	dlist = conf["dock-apps"]
	dlist = [x for x in dlist if x != a]
	conf["dock-apps"]=dlist
	lastDict = check_dict(conf)
	
