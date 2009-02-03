#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

import threading
import time

###############################################################################################################
###################################           Plugins interface             ###################################
###############################################################################################################

class AttackPlugin:
	def __init__(self,name,variableSet,iface,type,fields=[],):

		self.variableSet=variableSet               # if Variable set== True --> All traffic is processed, else only requests with uniq variable sets

		self.pluginName=name
		self.iface=iface

		self.enabled=False

		self.cache={}
		self.reqpool=[]

		self.nthreads=1
		self.diff=0
		self.Semaphore_Threads=threading.BoundedSemaphore(value=20)
		for i in range(20-self.nthreads):
			self.Semaphore_Threads.acquire()

		self.Semaphore_Mutex=threading.BoundedSemaphore(value=1)
		self.Semaphore_Mutex2=threading.BoundedSemaphore(value=1)

		self.runningThreads=0

		self.attackThreads=[]

		self.infoType=type
		self.fields=fields

		self.RESULTS=[]                     ## Raw Results
		self.newRESULTS=[]                  ## new raw results (volatil)

		self.xmlRESULTS=[]                  ## Xml Results (xml nodes)
		self.htmlRESULTS=[]                 ## free
		self.reqRESULTS=[]                  ## request result objects (optional)

		self.LOG=[]
		
	def getLOG(self):
		res=self.LOG[:]
		self.LOG=[]
		return res
		

	def putRESULTS(self,res,req=None):
		self.RESULTS.append(res)
		self.newRESULTS.append(res)
		if req:
			self.reqRESULTS.append(req)


	def setThreads(self,n):
		self.Semaphore_Mutex2.acquire()
		if n>self.nthreads:
			for i in range(n-self.nthreads):
				self.Semaphore_Threads.release()
		elif n<self.nthreads:
			for i in range(self.nthreads-n):
				self.Semaphore_Threads.acquire()

		self.nthreads=n
		self.Semaphore_Mutex2.release()

	def setEnabled(self,bl):
		if bl:
			self.enabled=True
			self.processThread=threading.Thread(target=self.__processor, kwargs={})
			self.processThread.start()
		else:
			self.enabled=False
			self.processThread.join()

	def launch(self,req):
		if self.enabled and req:
			if self.__updateCache(req):
				self.reqpool.append(req)

	# Se encarga de lanzar y controlar los threads de ataque (EN UN THREAD APARTE self.processThread)
	def __processor(self):
		while self.enabled:
			if self.reqpool:
				req=self.reqpool.pop(0)

				while self.diff>0:
					time.sleep(1)
				self.Semaphore_Threads.acquire()
				self.Semaphore_Mutex.acquire()
				self.runningThreads+=1
				self.Semaphore_Mutex.release()
				
				th=threading.Thread(target=self.__preprocess,kwargs={"req":req})
				self.attackThreads.append(th)
				th.start()


			time.sleep(1)
			tmp=[]
			for i in self.attackThreads:
				if not i.isAlive():
					tmp.append(i)
			for i in tmp:
				i.join()
				self.attackThreads.remove(i)

	# Lanza un thread para cada peticion, controla los semaforos
	def __preprocess(self,req):
		try:
			self.process(req)
		except Exception,a:
			self.LOG.append(str(a))
			
	
		self.Semaphore_Mutex.acquire()
		self.Semaphore_Threads.release()
		self.runningThreads-=1
		self.Semaphore_Mutex.release()

	def process(self,req):
		return


	def __updateCache(self,req):

		key=req.urlWithoutVariables
		dicc={}
		for j in [i.name for i in req.getGETVars()]:
			dicc[j]=True
		for j in [i.name for i in req.getPOSTVars()]:
			dicc[j]=True

		vars=dicc.keys()

		if self.variableSet:
			if not vars:
				return False

		vars.sort()

		key+="-"+"-".join(vars)


		if not key in self.cache:
			self.cache[key]=True
			return True
		return False

	def __clearCache(self):
		self.cache={}

	def getResults(self):
		return self.RESULTS[:]

	def getResultRequest (self,n):
		if n>len(self.reqRESULTS) or n<0:
			return None
		return self.reqRESULTS[n]

	def getNewResults(self):
		self.Semaphore_Mutex.acquire()
		a=self.newRESULTS[:]
		self.newRESULTS=[]
		self.Semaphore_Mutex.release()
		return a

	def getXML(self):
		raise Exception,"Feature not available in plugin '%s'" % (self.pluginName)

	def getHTML(self):
		raise Exception,"Feature not available in plugin '%s'" % (self.pluginName)

