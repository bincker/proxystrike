#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

from urlparse import *
import re

from xml.dom.minidom import Document


XSS_SET=[
["<!--%23echo%20var='HTTP_USER_AGENT'%20-->" , "XSSIPWNR" , "SERVER SIDE INCLUDE"],
['XSS\'PWNR', 'XSS\'PWNR', "' (Single Quotes)"],
['XSS"PWNR','XSS"PWNR' ,'" (Double Quotes)'],
['XS<SP>WNR','XS<SP>WNR' ,'<, > (Less than and great than symbols)'],
['XS(SP)WNR','XS(SP)WNR' ,'( ) (Parenthesis)'],
['XS-<SCRIPT>alert(document.cookie)</SCRIPT>-SPWNR','XS-<SCRIPT>alert(document.cookie)</SCRIPT>-SPWNR' ,'Scripting keywords enabled']
]

ENCODING=[
('%hex', 'url encoding (%hex)'),
('%25hex', 'doble url encoding (%25hex)'),
('%2525hex', 'triple url encoding (%25hex)'),
('\\xhex', 'utf8 encoding (\\xhex)'),
('\\u00hex', 'utf8 encoding (\\u00Hex)')
]

STRENCODED="XSSPWNR"
for x,y in ENCODING:
	STRENCODED+="-"+x.replace("hex","41")
STRENCODED+="-XSSPWNR2"


######################################################################################################
######################################################################################################
######################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################

class Xss:
	XID=1
	def __init__(self):
		self.results=[]
		self.cache={}
	
	def addRequest(self,req):
		if req.response:
			if self.recoverPrevious(req.response):
				return

		if self.updateCache(req):
			self.launchXss(req)
		
	def recoverPrevious(self,response):	
		return

	def launchXss(self,req):
		for i in self.req.getGETVars():
			self.test(req,var)
		for i in self.req.getPOSTVars():
			self.test(req,var)


	def test(self,req,var):
		var.update("XSSPWNR")

		for i in range(5):
			try:
				req.perform()
				break
			except:
				pass

		var.restore()

		if req.response.getContent().count("XSSPWNR"):
			setout=[]

			AVAIL_ENCS=self.testEncoding(var)
	
			
			for x,z,y in XSS_SET:
				for enco, desc in AVAIL_ENCS:
					xx = ''
					if enco:
						for car in x:
							xx += enco.replace("hex",hex(ord(car))[2:])
					else:
						xx=x

					if self.perform(xx, z,var):
						setout.append(y + " " + "(%s)" %(desc))

						break;

			return (True,method,var.name,setout,var.value)
		else:
			return (False,method,var.name,[],var.value)


	def testEncoding(self,req,var):
		global STRENCODED

		var.update(STRENCODED)

		for i in range (5):
			try:
				req.perform()
				break
			except:
				pass

		var.restore()


		res=[('','Normal Encoding')]
		encodings=re.findall("XSSPWNR(.*)XSSPWNR2",req.response.getContent())
		if encodings:
			encodings=encodings[0].replace("%2D","-")
			encodings=encodings.replace("%2d","-")
			encodings=re.findall("-[^-]+",encodings)

			for i in range(len(ENCODING)):
				try:
					if encodings[i][1:]=='A':
						res.append(ENCODING[i])
				except:
					print "-----------------EXCEPCION PUTA!----------------"

		return res


	def updateCache(self,req):
		key=req.urlWithoutVariables
		dicc={}
		for j in [i.name for i in req.getGETVars()]:
			dicc[j]=True
		for j in [i.name for i in req.getPOSTVars()]:
			dicc[j]=True

		vars=dicc.keys()

		if not vars:
			return False

		vars.sort()

		key+="-"+"-".join(vars)


		if not key in self.cache:
			self.cache[key]=True
			return True
		return False

	
		
		
		

class crossiter:
	''' Container of request variants ''' 
	def __init__(self,req,str="gp"):
		self.req=req
		self.req.addHeader("User-Agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.XSSIPWNR)")
		self.GET=False
		self.POST=False

		self.GETvars=self.req.getGETVars()
		self.POSTvars=self.req.getPOSTVars()

		self.posGET=0
		self.posPOST=0

		if 'g' in str.lower():
			self.GET=True
		if 'p' in str.lower():
			self.POST=True

		self.req.setTotalTimeout(15)
		self.resultSet=[]
		self.success=False

	def launch(self):
		for i in self:
			if i[0]:
				self.success=True
				self.resultSet.append(i)

	def getXMLResults(self):
		success=False

		doc=Document()
		wml = doc.createElement("GazpacioResults")
		doc.appendChild(wml)
		result=doc.createElement("XssResult")
		wml.appendChild(result)
		result.appendChild(self.req.getXML(doc))
		for i in self.resultSet:
			if i[0]:
				success=True
				var = doc.createElement("variable")
				var.setAttribute("name",i[2])
				var.setAttribute("method",i[1])
				inj = doc.createElement("InjectionsAvailable")
				inj.appendChild(doc.createTextNode("\r\n".join(i[3])))
				var.appendChild(inj)
				result.appendChild(var)

		if success:
			return doc

		return None


	def getRAWResults(self):
		if self.success:
			return self.resultSet
		else:
			return []

	def __iter__ (self):
		self.posGET=0
		self.posPOST=0
		return self

	def perform(self, pattern, searchPatt,var):
		matchPatt = False

		var.update(pattern)
	
		for i in range (5):
			try:
				self.req.perform()
				break
			except:
				pass

		var.restore()


		if self.req.response.getContent().count(searchPatt):
			matchPatt = True

		return matchPatt

	def testEncoding(self,var):
		global STRENCODED

		var.update(STRENCODED)

		for i in range (5):
			try:
				self.req.perform()
				break
			except:
				pass

		var.restore()


		res=[('','Normal Encoding')]
		encodings=re.findall("XSSPWNR(.*)XSSPWNR2",self.req.response.getContent())
		if encodings:
			encodings=encodings[0].replace("%2D","-")
			encodings=encodings.replace("%2d","-")
			encodings=re.findall("-[^-]+",encodings)

			for i in range(len(ENCODING)):
				try:
					if encodings[i][1:]=='A':
						res.append(ENCODING[i])
				except:
					print "-----------------EXCEPCION PUTA!----------------"

		return res
		

	def next(self):
		if self.GET and self.posGET < len (self.GETvars):
			var=self.GETvars[self.posGET]
			method="GET"
			self.posGET+=1

		elif self.POST and self.posPOST < len (self.POSTvars):
			var=self.POSTvars[self.posPOST]
			method="POST"
			self.posPOST+=1

		else:
			raise StopIteration

		var.update("XSSPWNR")

		for i in range(5):
			try:
				self.req.perform()
				break
			except:
				pass

		var.restore()
		
		

		if self.req.response.getContent().count("XSSPWNR"):
			setout=[]

			AVAIL_ENCS=self.testEncoding(var)
	
			
			for x,z,y in XSS_SET:
				for enco, desc in AVAIL_ENCS:
					xx = ''
					if enco:
						for car in x:
							xx += enco.replace("hex",hex(ord(car))[2:])
					else:
						xx=x

					if self.perform(xx, z,var):
						setout.append(y + " " + "(%s)" %(desc))

						break;

			return (True,method,var.name,setout,var.value)
		else:
			return (False,method,var.name,[],var.value)



