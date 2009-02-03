#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)


import re
from urlparse import urlparse,urlunparse
 
class HTMLInput:
	regexp=re.compile("<input[^>]+name=['\" ]*([^'>\" ]+)['\"> ]",re.I)
	def __init__(self,tag):
		tag=tag.strip()
		matches=HTMLInput.regexp.findall(tag)
		self.name=""

		if matches:
			self.name=matches[0].lower()

	def __str__(self):
		return self.name


class HTMLForm:
	reAction=re.compile("<form[^>]+action=['\" ]?([^'>\" ]*)['\"> ]",re.I)
	reInput=re.compile("(<input[^>]+>)",re.I)
	def __init__(self,tag):
		self.inputs=[]
		self.action="-NoAction-"

		match=HTMLForm.reAction.findall(tag)
		if match and match[0]:
			self.action=urlunparse(urlparse(match[0])[:3]+('','',''))
		
		matches=HTMLForm.reInput.findall(tag)
		for i in matches:
			self.inputs.append(HTMLInput(i))

	def __str__(self):
		a=[str(i) for i in self.inputs if str(i)]
		a.sort()
		if a:
			return str([self.action])+" - "+str(a)
		else:
			return ""


class PageAnalyzer:
	regexp=re.compile("(<form([^<]|<[^/]|</[^f]|</f[^o]|</fo[^r]|</for[^m]|</form[^>])+</form>)",re.I)
	reip=re.compile("[^0-9]([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})[^0-9]")
	remail=re.compile("([a-z\._0-9-]+(@|_at_)[a-z\._0-9-]+)",re.I)
	recomment=re.compile("<!--(([^-]|-[^-]|--[^>])+)-->",re.I)
	def __init__(self,html,url,forms=False,ip=False,mail=False,comment=False):
		self.forms=[]
		self.url=url

		self.mails={}
		self.ips={}
		self.comments={}


		if forms:
			for i in self.regexp.findall(html):
				self.forms.append(HTMLForm(i[0]))

		if mail:
			for j in [i[0] for i in self.remail.findall(html)]:
				self.mails[j]=True

		if ip:
			for j in self.reip.findall(html):
				self.ips[j]=True

		if comment:
			for j in [i[0] for i in self.recomment.findall(html) if "document" not in i[0] ]:
				self.comments[j]=True

	def formSummary(self):
		dic={}
		for i in self.forms:
			if str(i):
				dic[str(i)]=self.url

		return dic

class WebAnalyzer:
	def __init__(self,forms=False,ip=False,mails=False,comment=False):
		self.pages=[]
		self.dynurls={}
		self.extensions={}

		self.forms=forms
		self.ips=ip
		self.mails=mails
		self.comments=comment

		self.UniqForms={}

	def appendPage(self,html,url):
		if "?" in url:
#			if not url in self.dynurls:
#				print url
			self.dynurls[url]=True

		html=html.replace("\r","")
		html=html.replace("\n","")
		tmp=PageAnalyzer(html,url,forms=self.forms,ip=self.ips,mail=self.mails,comment=self.comments)

		path=urlparse(url)[2]
		if "." in path:
			ext=path.split(".")[-1]
		else:
			ext="No extension"

		if not ext in self.extensions:
			self.extensions[ext]=[]

		self.extensions[ext].append(url)

		if self.forms:
			self.UniqForms.update(tmp.formSummary())


	def getDynPages(self):
		return self.dynurls.keys()

	def formSummary(self):
		return self.UniqForms

	def infoSummary(self):
		dic={"mails":{},"ips":{},"comments":{}}

		for i in self.pages:
			dic["mails"].update(i.mails)
			dic["ips"].update(i.ips)
		#	dic["comments"].update(i.comments)

		dic["mails"]=dic["mails"].keys()
		dic["ips"]=dic["ips"].keys()
		#dic["comments"]=dic["comments"].keys()
		return dic

	def getByextensions(self):
		return self.extensions
