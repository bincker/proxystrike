#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)
# This is a port of sqlibf to python, # sqlibf is a SQL injection 
# tool that was coded by Ramon Pinuaga (www.open-labs.org)

from injection import *
from misc import *
from sqResult import *
import urllib
import sys
import copy
import database



class Test:
	def __init__(self):
		pass

class InjectTry:
	def __init__(self,type,logger):
		self.type=type
		self.tryTests=[]
		self.logger=logger

	def addTry (self,pattern,tryCompareEqual):
		self.tryTests.append((urllib.quote(pattern),tryCompareEqual))
	
	def MakeTry(self,sqRObj):

		var=sqRObj.getVar()
		req=sqRObj.getReq()
		method=sqRObj.getMethod()

		testFailed=False

		for payload,result in self.tryTests:
			var.append(payload)

			self.logger.debug("Trying injection in - %s - %s - %s" % (method,var.name,urllib.unquote(payload)))

			req.perform()
			req.response.Substitute(payload," ")

			for i in database.FingerTests:       ### Este bucle es para buscar errores de SQL en los resultados
				if i.searchError(req.response):
					self.logger.debug("Error Message FOUND - %s" % (i.getName()))
					sqRObj.setError(i.getName())

			tmpreq=copy.deepcopy(req)

			var.restore()
					
			if sqRObj.equalResponse(req.response)!=result:
				testFailed=True
				self.logger.debug("FAILED")
				break
			self.logger.debug("DONE")



		if not testFailed:
			self.logger.debug("Parameter INJECTABLE - %s - %s - %s" % (str(self.type),method,var.name))
			sqRObj.setType(self.type)


		if not testFailed or sqRObj.getError():
			return True,tmpreq

		return False,None

		

class InjectionTest(Test):
	def __init__(self,tests):
		self.tests=tests

	def launch(self,sqRObj):
		result=False
		for i in self.tests:
			result,req=i.MakeTry(sqRObj)
			if result:
				return True,req
		return False,None
		

		

class FingerprintTest:
	def __init__(self,tests,logger):
		self.tests=tests
		self.logger=logger

	def launch(self,sqRObj):
		res=False
		for i in self.tests:
			self.logger.debug("Trying %s" % (str(i)))
			res=self.TryDB(i,sqRObj)
			if res:
				return True,None
		return False,None

	def TryDB(self,db,sqRObj):

		try:
			payload1=db.getTestPattern(sqRObj.getType())
			payload2=db.getConfirmPattern(sqRObj.getType())
		except:
			return False

		var=sqRObj.getVar()
		method=sqRObj.getMethod()
		req=sqRObj.getReq()

		self.logger.debug("Variable - %s - %s" % (method,var.name))
		self.logger.debug("Payloads to try: %s - %s" % (urllib.unquote(payload1),urllib.unquote(payload2)))

	
		var.append(payload1)		

		req.perform()
		req.response.Substitute(payload1," ")


		testPassed=False

		if sqRObj.equalResponse(req.response):
			self.logger.debug("Payloads one DONE" )
			var.restore()
			var.append(payload2)
	
			req.perform()
			req.response.Substitute(payload2," ")

			if sqRObj.equalResponse(req.response):
				self.logger.debug("Payload two DONE - Fingerprint on variable - %s - %s - %s" % (method,var.name,db.getName()))
				testPassed=True
			else:
				self.logger.debug("Payload two FAILED!!!! - Not fingerprint on variable - %s - %s - %s" % (method,var,db.getName()))

		var.restore()

		if testPassed:
			sqRObj.setDB(db.getName())
			return True

		return False

