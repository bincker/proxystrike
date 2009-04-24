#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

from Proxynet import *
from attacker import *
import cPickle as pickl
import bz2
from urlparse import urlparse
from crawler import DCrawl



class Controller:
	def __init__(self):
		self.variableStats={}
		self.reqStats={}
		self.requests=[]
		self.newRequests=[]

		self.intercept=False

		self.attacker=Attacker()

		self.crawler=DCrawl()
		self.crawlerDomainInput=None
		self.crawlerOn=False

		self.uniqForms={}
		self.crawlForward=False	

	def limitPath(self,path):
		self.crawler.addNeeded(path)
		self.attacker.limitPath(path)

	def setCrawlerForward(self,bl):
		self.crawlForward=bl
		
		
	def startCrawler(self,domainInput):
		self.crawlerOn=True
		self.crawlerDomainInput=urlparse(domainInput.lower())[1]
		self.crawler.restart()
		self.crawler.append(domainInput.lower())

	def stopCrawler(self):
		self.crawler.stop()
		self.crawlerOn=False

	def resetCrawler(self):
		self.crawlerOn=False
		self.crawler.reset()
		self.uniqForms={}

	def getCrawlerStatus(self):
		return self.crawler.status()
		return None

	def getUniqForms(self):
		if not self.crawlerOn:
			return []
		res=[]

		lst=self.crawler.FormAnalysis.formSummary()
		for i,j in lst.items():
			if not i in self.uniqForms:
				self.uniqForms[i]=True
				res.append(j)

		return res


	def getVariableStats(self):
		return self.variableStats

	def getReqStats(self):
		return self.reqStats

	def updateAllStats(self):
		self.variableStats={}
		self.reqStats={}

		for i in self.requests:
			self.updateStats(i)

	def updateStats(self,req):
		i=req
		if not i:
			return

		######### ACTUALIZAMOS VARIABLE STATS ####################
		if not self.variableStats.has_key(i.urlWithoutPath):
			self.variableStats[i.urlWithoutPath]={}
		if  not self.variableStats[i.urlWithoutPath].has_key(i.path):
			self.variableStats[i.urlWithoutPath][i.path]={}

		for j in i.getGETVars():
			if not self.variableStats[i.urlWithoutPath][i.path].has_key(j.name):
				self.variableStats[i.urlWithoutPath][i.path][j.name]={}
			self.variableStats[i.urlWithoutPath][i.path][j.name][j.value]=True

		for j in i.getPOSTVars():
			if not self.variableStats[i.urlWithoutPath][i.path].has_key(j.name):
				self.variableStats[i.urlWithoutPath][i.path][j.name]={}
			self.variableStats[i.urlWithoutPath][i.path][j.name][j.value]=True
			
		######## ACTUALIZAMOS REQUEST STATS ######################
		if not self.reqStats.has_key(i.urlWithoutPath):
			self.reqStats[i.urlWithoutPath]={}
	
		if not self.reqStats[i.urlWithoutPath].has_key(i.path):
			self.reqStats[i.urlWithoutPath][i.path]=[]
	

		nomvars=[j.name for j in i.getGETVars()]
	
		if nomvars!=None and len(nomvars)>0:
			nomvars.sort()
	
			found=False
			for k in self.reqStats[i.urlWithoutPath][i.path]:
				if k[0]==nomvars:
					found=True
	
			if found==False:
				self.reqStats[i.urlWithoutPath][i.path]+=[(nomvars,i.getGETVars())]


		nomvars=[j.name for j in i.getPOSTVars()]
	
		if nomvars!=None and len(nomvars)>0:
			nomvars.sort()
	
			found=False
			for k in self.reqStats[i.urlWithoutPath][i.path]:
				if k[0]==nomvars:
					found=True
	
			if found==False:
				self.reqStats[i.urlWithoutPath][i.path]+=[(nomvars,i.getPOSTVars())]

		##########################################################

	def setProxy(self,proxy):
		self.attacker.setProxy(proxy)
		self.crawler.setProxy(proxy)

	def timer(self):
		size=Proxynet.getNumberRequests()
		if size:
			for n in range(size):
				i=Proxynet.getRequest()
				self.requests+=[i]
				self.updateStats(i)
				self.newRequests.append(i)
				self.attacker.addReq(i)

				################## Crawler
				url=i.completeUrl
				domain=urlparse(url)[1].lower()
				if domain == self.crawlerDomainInput and self.crawlerOn:
					self.crawler.append(url)
					ck=i["Cookie"]
					if ck:
						self.crawler.setCookie(ck)

		reqs=self.crawler.getRequests()
		for i in reqs:
			self.updateStats(i)
			if self.crawlForward:
				self.attacker.addReq(i)


	def getRequests(self):
		return self.requests
	
	def getNewRequests(self):
		x=self.newRequests[:]
		self.newRequests=[]
		return x

	def getNumAttacks(self):
		return 0,0

######## Plugins ####################

	def getPluginLogs(self):
		return self.attacker.getPluginLogs()
		

	def getNewResults(self):
		return self.attacker.getNewResults()

	def resetPluginCache(self,plugname):
		self.attacker.resetPluginCache(plugname)

	def getPluginResult(self,plugname,n):
		return self.attacker.getPluginResult(plugname,n)

	def getPluginStatus(self):
		return self.attacker.getPluginStatus()

	def saveXML(self,plugname,file):
		a=self.attacker.getXML(plugname)
		doc=Document()
		wml=doc.createElement("ProxyStrikeResults")
		doc.appendChild(wml)
		for i in a:
			wml.appendChild(i)

		f=open(file,"w")
		f.write(doc.toprettyxml())
		f.close()


	def saveHTML(self,plugname,file):

		htmlResults=self.attacker.getHTML(plugname)

		f=open(file,"w")
		f.write(htmlResults)
		f.close()

	def enablePlugin(self,name,bl):
		self.attacker.enablePlugin(name,bl)

	def setPluginThreads(self,name,n):
		self.attacker.setPluginThreads(name,n)

	def getPluginProperties(self):
		return self.attacker.getPluginProperties()

######## Interception ################

	def setIntercept(self,b):
		self.intercept=b
		Proxynet.setIntercept(b)

	def interceptON(self):
		return self.intercept==True

	def getIntercepted(self):
		if self.intercept:
			return Proxynet.getIntercepted()	

	def destroyIntercepted(self,r):
		Proxynet.destroyIntercepted(r)

	def processIntercepted(self,r):
		Proxynet.processIntercepted(r)

############ Repeater ############
	
	def performRepeater(self,schema,rawbody):
		schema=str(schema)
		rawbody=str(rawbody)

		r=Request()
		
		schema=schema.lower()
		if schema not in ["http","https"]:
			raise Exception,"Invalid schema (http/https)"

		try:
			r.parseRequest(rawbody,schema)
		except:
			raise Exception,"Can't parse body"

		try:
			r.setTotalTimeout(10)
			r.perform()
		except:
			raise Exception,"Can't send request, try again"

		return r.response

###########  SAVE & LOAD  ###################

	def save (self,fileName):
		f = bz2.BZ2File(fileName, 'wb')
		pickl.dump([ self.requests , self.sqlResults , self.xssResults ], f,1)
		f.close()

	def load (self,fileName):
		f = bz2.BZ2File(fileName,"rb")
		self.xssResults=[]
		self.sqlResults=[]
		self.requests ,sqlResults , xssResults = pickl.load(f)
		self.newRequests=self.requests
		self.attacker.setXssResults(xssResults)
		self.attacker.setSqlResults(sqlResults)
		f.close()

		
