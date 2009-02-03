#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)


from Gazpacho import *
import sqPyfia
import htmlout

##############################################################
##############################################################
from pluginSkel import AttackPlugin

# AttackPlugin is the plug-in superclass
#
# Next i'll explain how to create a plugin:
# 
#		AttackMod_MyPLugin(AttackPlugin)                  --> Your class must inherit from AttackPlugin :D
#																and the name of the class must begin with AttackMod_ !!!!
#			def __init__(self):	
#				AttackPlugin.__init__(self, ... PARAMETERS ...) You must invoke superclass constructor 
#			
#		+++ Constructor Parameters (in order): 
#				name: Name of the module (will be shown in Proxystrike)		
#
#				variableSet(True or False):
#					True: Process one time the same variable set (proxystrike handles a cache)   
#					False: Process all the requests processed by proxystrike
#
#				iface(True or False): Specify if the plugin will be shown in the GUI (plugin may not have interface)
#
#				infoType: infotype is the output format of the plugin. in can be "tree" or "text"
#					tree: Information will be structured in a TreeView widget
#					text: Information will be appended in a textEdit widget
#
#				fields: if infoType="tree", the tree widget need the text on the fileds shown in the header, so
#					this parameter is a list of strings containing the header fields
#
#
#
#
# Once the constructur is defined you have to overload some functions:
#	
#	def process(request)	---		Required
#		This function receives directly request objects from ProxyStrike
#
#	def getHTML()			---		Optional	(Beta and deprecated ??? WTF?!?!?! I dnt knw...)
#		This function returns data to create an html output of the plugin
#
#	def getXML()			---		Optional
#		This function returns data to create an XML output of the plugin
#		it is a list of Element objects of minidom Python API
#
#
#
#
# Implementing PROCESS method:
#	After processing the request and/or its response, the information gathered using self.putRESULTS(result,request=None) method
#	but the format depends on INFOTYPE variable. If you append a request moreover when doubleclick it in the tree it will be 
#	forwarded to the REPEATER module.
#	
#	infotype==text --> The data type passed to self.putRESULTS() can be of any type, because proxystrike will 
#						perform an str() call to the data type and will append the result to de textArea
#
#	infotype==tree --> For filling a tree structure is used a tree of dicts :S (it seems hard to explain)
#					
#			!!! Trees can be only 1 level depht, and the root node is allways the first field
#
#		example of tree:
#
#								Headers:	A		B		C		D
#											info1
#											|_		info2	info3	info4						
#
#						Data structure of a result:	['info1',['info2','info3',info4']]
#
#								Headers:	A		B		C		D
#											info1
#											|_		info2	info3	info4						
#											|_		info21	info32	info43						
#
#						Data structure of a result:	['info1',['info2','info3',info4'],['info21','info32','info43']]
#					



###############################################################################################################
###################################           SQPYFIA          ################################################
###############################################################################################################


class AttackMod_sqPyfia(AttackPlugin):
	def __init__(self):
		# Name, variableSet ,iface, infoType, fields
		AttackPlugin.__init__(self,"Sql attacks",True,True,"tree",["Url","Variable","Method","Injection Type","DB Fingerprint","DB Error"])

	def process(self,req):
		sq=sqPyfia.sqPyfia(req)
		sq.setThreaded(1)
		try:
			sq.launch()
			a=sq.getLogs()
			if a:
				raise Exception," ".join(a)
	
			res=sq.getRAWResults()
			xml=sq.getXMLResults()
	
			if res:
				self.Semaphore_Mutex.acquire()
				self.putRESULTS(res,sq.getRequestExample())
				self.xmlRESULTS.append(xml.childNodes[0].childNodes[0])
				self.Semaphore_Mutex.release()

		except Exception,a:
			raise Exception,"SqlInj Engine: "+str(a)+" - "+"Fallo en SQL, REQ="+str(req)


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

###############################################################################################################
###################################           GAZPACIO         ################################################
###############################################################################################################


class AttackMod_gazpacio(AttackPlugin):
	def __init__(self):
		# Name, variableSet ,iface, infoType, fields
		AttackPlugin.__init__(self,"XSS attacks",True,True,"tree",["Url","Variable","Method","Injections Available"])
		
		
	def process(self,req):
		c=crossiter(req,"gp")
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

