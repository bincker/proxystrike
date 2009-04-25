from tools.gazpacho.Gazpacho import *
from tools.htmlout import *
from tools.pluginSkel import AttackPlugin

class AttackMod_gazpacio(AttackPlugin):
	def __init__(self):
		# Name, variableSet ,iface, infoType, fields
		AttackPlugin.__init__(self,"XSS & SSI attacks",True,True,"tree",["Url","Variable","Method","Injections Available"])
		
		
	def process(self,req):
		c=crossiter(req,"gp",self.LOG)
		try:
			c.launch()
	
			xml=c.getXMLResults()
			if not xml:
				return
			htmlres=[req.completeUrl,c.getRAWResults()]
	
			self.htmlRESULTS.append(htmlres)
			
			restratados=htmlres[1]
			#[(True, 'GET', 'nIdNoticia', ['<, > (Less than and great than symbols) (Normal Encoding)', '( ) (Parenthesis) (Normal Encoding)', "' (Single Quotes) (Normal Encoding)", '" (Double Quotes) (Normal Encoding)'], '2475')]
			newres=[]
			for i in restratados:
				if i[0]:
					newres.append([i[2],i[1],"\r\n".join(i[3])])
	
			newres=[req.completeUrl,newres]
			
	
			self.xmlRESULTS.append(xml.childNodes[0].childNodes[0])
			self.newRESULTS.append(newres)
			self.RESULTS.append([req.completeUrl,newres])
	
		except Exception,a:
			raise Exception,"Xss Engine: "+str(a)+" - "+"Fallo en XSS, REQ="+str(req)+"\r\n--------------------------------------------\r\n"

	def getXML(self):
		return self.xmlRESULTS

	def getHTML(self):
		output=htmlout.html(title=self.pluginName+" results")

		for r in self.htmlRESULTS:
			t=htmlout.XssTable()
			t.setTitle(r[0])
			for j in r[1]:
				t.addRow(j)
			output.appendTable(t)
		output.flush()

		return str(output)

