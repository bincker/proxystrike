from tools.sqpyfia.sqPyfia import sqPyfia
from tools.htmlout import *
from pluginSkel import AttackPlugin

class AttackMod_sqPyfia(AttackPlugin):
	def __init__(self):
		# Name, variableSet ,iface, infoType, fields
		AttackPlugin.__init__(self,"Sql attacks",True,True,"tree",["Url","Variable","Method","Injection Type","DB Fingerprint","DB Error"])

	def process(self,req):
		sq=sqPyfia(req,self.LOG)
		sq.setThreaded(1)
		try:
			sq.launch()
	
			res=sq.getRAWResults()
			xml=sq.getXMLResults()
	
			if res:
				self.putRESULTS(res,sq.getRequestExample())
				self.xmlRESULTS.append(xml.childNodes[0].childNodes[0])

		except Exception,a:
			self.LOG.debug("SqlInj Engine: "+str(a)+" - "+"Fallo en SQL, REQ="+str(req))


	def getXML(self):
		return self.xmlRESULTS

	def getHTML(self):
		output=htmlout.html(title=self.pluginName+" results")

		for r in self.RESULTS:
			t=htmlout.SqlTable()
			t.setTitle(r[0])
			for j in r:
				t.addRow(j)
			output.appendTable(t)
		output.flush()

		return str(output)

