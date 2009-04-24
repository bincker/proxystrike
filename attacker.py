#!/usr/bin/python
#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

import copy
from logging import Logger,Handler
import threading
import re
import os
import imp
import inspect


class PluginLogger(Logger):
	def __init__(self):
		Logger.__init__(self,"PluginLogger")

	def getInfo(self):
		return self.handlers[0].getAllInfo()

class PluginLogHandler(Handler):
	def __init__(self):
		self.mutex=threading.BoundedSemaphore(value=1)
		Handler.__init__(self)
		self.info=[]

	def handle(self,record):
		self.mutex.acquire()
		self.info.append(record.msg)
		self.mutex.release()

	def getAllInfo(self):
		self.mutex.acquire()
		a=self.info
		self.info=[]
		self.mutex.release()
		return a


class Attacker():

	def __init__ (self):
		self.__proxy=None
		self.plugins={}
		self.__LOGGER=PluginLogger()
		self.__LOGGER.addHandler(PluginLogHandler())
		self.getPlugins()
		self.limitpath=None

	def setProxy(self,str):
		self.__proxy=str

	def limitPath(self,regex):
		if regex:
			self.limitpath=re.compile(regex,re.I)
		else:
			self.limitpath=None

	
	def clearCache(self):
		self.__paths={}


	def enablePlugin(self,name,bl):
		self.plugins[name].setEnabled(bl)

	def setPluginThreads(self,name,n):
		self.plugins[name].setThreads(n)

	def resetPluginCache(self,name):
		self.plugins[name].clearCache()

	def getPluginLogs(self):
		return self.__LOGGER.getInfo()


	def addReq(self,req):
		if req:
			if self.limitpath and not self.limitpath.findall(req.completeUrl):
				return
			req.setProxy(self.__proxy)
			for i in self.plugins.values():
				i.launch(copy.deepcopy(req))

	def getPluginResult(self,pluginame,n):
		return self.plugins[pluginame].getResultRequest(n)

	def getXML(self,pluginame):
		return self.plugins[pluginame].getXML()

	def getHTML(self,pluginame):
		return self.plugins[pluginame].getHTML()

	def getPlugins(self):               
		files=[os.path.join("plugins",i).split(".")[0] for i in  os.listdir(os.path.join("plugins")) if os.path.isfile(os.path.join("plugins",i)) and i[-2:].lower()=="py"]
		
		plugs=[]
		
		for i in files:
			j,k,l= imp.find_module(i)
			m= imp.load_module(i, j,k,l)
			j.close()
			for j in dir (m):
				if inspect.isclass(getattr(m,j)):
					if '_AttackPlugin__processor' in dir(getattr(m,j)) and j!="AttackPlugin":
						plugs.append(getattr(m,j)) 
		
		for i in plugs:
			pl=i()
			pl.setLogger(self.__LOGGER)
			self.plugins[pl.pluginName]=pl

	def getNewResults(self):
		ur={}
		for i,j in self.plugins.items():
			if j.iface:
				plugres=j.getNewResults()
				if plugres:
					ur[i]=[j.infoType,plugres]

		return ur

	def getPluginStatus(self):
		dret={}
		for i,j in self.plugins.items():
			if j.runningThreads:
				dret[i]=j.runningThreads

		return dret



	def getPluginProperties(self):          # Utilizado solo por el interface!
		prp={}
		for i,j in self.plugins.items():
			if j.iface:
				nwpl={}
				nwpl["type"]=j.infoType
				nwpl["fields"]=j.fields
				prp[i]=nwpl

		return prp

			
		

