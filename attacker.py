#!/usr/bin/python
#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

import plugins
import copy
from logging import Logger,Handler
import threading

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

	def setProxy(self,str):
		self.__proxy=str

	
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
		plugs=[i for i in dir(plugins) if "AttackMod_" in i]
		for i in plugs:
			pl=getattr(plugins,i)()
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

			
		

