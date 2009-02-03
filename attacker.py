#!/usr/bin/python
#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

import logging
import plugins
import copy

#logging.basicConfig(level=logging.DEBUG,format='%(levelname)s ==> \t%(message)s')

class Attacker():

	def __init__ (self):
		self.__proxy=None
		self.plugins={}
		self.getPlugins()

	def setProxy(self,str):
		self.__proxy=str

	
	def clearCache(self):
		self.__paths={}

	def getLogs(self):
		return self.__LOGGER.values()

	def enablePlugin(self,name,bl):
		self.plugins[name].setEnabled(bl)

	def setPluginThreads(self,name,n):
		self.plugins[name].setThreads(n)

	def resetPluginCache(self,name):
		self.plugins[name].clearCache()

	def getPluginLogs(self):
		res=[]
		for i in self.plugins.values():
			res+=i.getLOG()

		return res


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

			
		

