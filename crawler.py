#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)


from reqresp import *
from TextParser import *
from iSearch import SearchEngine
import sys
from urlparse import urlparse,urlunparse
import threading
from time import sleep
import os
from webanalyzer import WebAnalyzer
import re
import consoleNg
import webbrowser
try:
	import readline
except:
	pass

class SearchLinks(SearchEngine):
	reInput=re.compile("<input[^>]+>",re.I)
	reIlegalChar=re.compile("%[0189abcfef][0-9abcdef]",re.I)
	reXtensions=re.compile("^ *[/a-z0-9_\.@\$%()!-]+\.[a-z0-9]{2,5}(;[^\?]+)?(\?.*)?$",re.I)
	reDundance=re.compile("(/\./|/[^/]+/\.\./|/{2,})")
	#reDundance=re.compile("(/\.\./[^/]+/|/{2,})")

	def __init__(self,url):
		SearchEngine.__init__(self,url)
		self.url=url

		self.sch,self.dom,self.path,_,_,_=urlparse(url)

		if not self.path:
			self.path=['/']
		else:
			if self.path[-1]!='/':  # Si el path no acaba en /
				self.path=self.path.split("/")[:-1]
			else:
				self.path=self.path.split("/")

		self.urlRegexp="(\"[^\"<>]+\"|\'[^\'<>]+\')"
		self.nextRegexp="Crawler: Deepbit is <God>"
	
	def preProcess(self,raw):
		return SearchLinks.reInput.sub("",raw)

	def trataResult(self,res):
		res=res[0][1:-1]
		res=res.strip()

		if not res:
			return None


		if res[:4].lower()=="http":
			sch,dom,path,g,h,i=urlparse(res)
			path=self.reDundance.sub("/",path)
			if dom!=self.dom or sch!=self.sch:
				return None
			final=urlunparse((sch,dom,path,g,h,i))
		elif res[0]=='/':
			res=self.reDundance.sub("/",res)
			if res[0]=="/":
				res=res[1:]
			final=urlunparse((self.sch,self.dom,res,"","",""))
		elif self.reXtensions.search(res):
			pth='/'.join(self.path[:]+[res])
			pth=self.reDundance.sub("/",pth)
			final=urlunparse((self.sch,self.dom,pth,"","",""))
		else:
			return None

		final=final.replace("&amp;","&")

		sch,dom,path,_,_,_=urlparse(final)
		parts=path.split("/")

		if SearchLinks.reIlegalChar.findall(final):
			return []

		final=[ final ] 

		for i in range(1,len(parts)):
			a=urlunparse((sch,dom,"/".join(parts[:i]),"","",""))+"/"
			final.append(a)

		return final

class DCrawl(consoleNg.Console):
	def __init__(self,threads=2,reject=[],store=False,proxy=None,regexpAvoid=None,cookie=None):

		self.FormAnalysis=WebAnalyzer(forms=True)
		self.running=False
		self.stopped=False

		self.CFG_threads=threads
		self.runningThreads=0
		self.CFG_store=store
		self.CFG_reject=reject+["jpg","gif","png","zip","exe","doc","swf","rar","pdf"]

		self.totalUrls=0
		self.doneUrls=0
		self.POOL=[]
		self.Done={}
		self.CFG_proxy=proxy

		self.urlOKS=[]

		if cookie:
			self.CFG_cookie=cookie
		else:
			self.CFG_cookie=None

		self.threads_list=[]

		self.Semaphore=threading.BoundedSemaphore(value=self.CFG_threads)
		self.Semaphore_Mutex=threading.BoundedSemaphore(value=1)

		if regexpAvoid:
			self.reAvoid=re.compile(regexpAvoid)
		else:
			self.reAvoid=None

		consoleNg.Console.__init__(self,"dcrawl> ")
		self.Handler=None

		self.Requests=[]

	def reset(self):
		self.running=False
		self.stopped=True
		self.Handler.join()
		self.totalUrls=0
		self.doneUrls=0
		self.POOL=[]
		self.Done={}
		self.Requests=[]
		self.FormAnalysis=WebAnalyzer(forms=True)

		

	def continueWith(self,url):
		if url not in self.Done:
			if self.reAvoid and self.reAvoid.findall(url):
				return False
			return True
		return False

	def __setattr__(self,item,value):
		if item=="CFG_threads":
			if self.running:
				raise Exception,"Crawler running!!! Wait to finish"
			self.__dict__[item] = value
			self.Semaphore=threading.BoundedSemaphore(value=self.CFG_threads)
			return

		self.__dict__[item] = value



	def __getattr__(self,item):
		if item=="CFG_threads":
			return self.threads
		else:
			raise AttributeError(item)

	
	def CMD_append(self,*args):
		'''append [url]				- add an Url to the crawler POOL'''
		self.append(args[0])

	def CMD_setCookie(self,*args):
		'''setCookie [ck]				- Set cookie for crawling'''
		self.setCookie(args[0])
		

	def CMD_status(self,*args):
		'''status					- prints urls_done/remaining_urls'''
		print self.doneUrls,"/",self.totalUrls

	def CMD_wait(self,*args):
		'''wait					- Waits for crawler to finish'''
		try:
			while self.running:
				print self.doneUrls,"/",self.totalUrls
				sleep(3)
		except:
			print "Wait command interrupted"

	def CMD_tohtml(self,*args):
		'''tohtml					- Writes results to html and open webbrowser'''

		forms="".join([ "Form: <a href='"+i+"'>"+i+"</a><br>" for i in self.FormAnalysis.formSummary().values()])
		dynurls= "".join([ "<a href='"+i+"'>"+i+"</a><br>" for i in self.FormAnalysis.getDynPages()])
		exts=""#<br".join(["<h3>"+i+"</h3><br>"+"<br>".join(j) for i,j in self.FormAnalysis.getByextensions().items()])
		

		html="<html><body></body><h1>Uniq forms</h1><br>%s<h1>Dyn Urls</h1><br>%s<br>%s</html>" % (forms,dynurls,exts)

		f=open("temp.html","w")
		f.write(html)
		f.close()

		print "File written: temp.html"

		webbrowser.open("temp.html")

	def CMD_stop(self,*args):
		'''stop						- Stops crawling process'''
		print "Stopping..."
		self.stop()
		print "Stopped! ;D"

	def CMD_restart(self,*args):
		'''restart				- restart Crawling process'''
		self.restart()

	def CMD_testsearch(self,*args):
		'''testsearch [url]			- Perform a search to test Link detector'''
		i=SearchLinks(args[0])
		i.addCookie(self.CFG_cookie)
		for j in i:
			print j

	def CMD_dumpurls(self,*args):
		'''dumpurls 				- Dump valid url's in dumpurls.txt'''
		f=open("dumpurls.txt","w")
		for i in self.urlOKS:
			f.write(i+"\r\n")
		f.close()
		
		
		

	def status(self):
		return self.doneUrls,self.totalUrls
		
	
	def stop(self):
		self.running=False
		self.stopped=True
		if self.Handler:
			self.Handler.join()
		
	def restart(self):
		self.running=True
		self.stopped=False
		self.Launch()
	
	def append(self,url):
		if self.continueWith(url):
			self.Semaphore_Mutex.acquire()
			self.totalUrls+=1
			self.POOL.append(url)
			self.Done[url]=True
			if url[-1]!="/":
				tmp=url.split("/")
				url="/".join(tmp[:-1])+"/"
			self.Semaphore_Mutex.release()
			if not self.running and not self.stopped:
				self.running=True
				self.Launch()

	def postFetch(self,str,url):
		if str:
			if self.CFG_store:
				_,dom,path,pre,vars,_=urlparse(url)
				if path[-1]=='/' and not pre and not vars:
					path=[dom]+path.split('/')
					file="index.html"
				else:
					path=path.split('/')
					file=path[-1]
					if pre:
						file+=";"+pre
					if vars:
						file+="?"+vars
					path=[dom]+path[:-1]

				path=[i for i in path if i]
				
				dirs=""
				for i in path:
					dirs=os.path.join(dirs,i)

				try:
					os.makedirs(dirs)
					print "Making dir: ",dirs
				except:
					pass

				finalpath=os.path.join(dirs,file)

				f=open(finalpath,"w")
				f.write(str)
				print "writting: ",finalpath
				f.close()
			else:
				self.FormAnalysis.appendPage(str,url)

	def getForms(self):
		dic=self.FormAnalysis.formSummary()

		for i,j in dic.items():
			print j,i

	def getDynPages(self):
		for i in self.FormAnalysis.getDynPages():
			print i


	def getInfo(self):
		print self.FormAnalysis.infoSummary()
			
	def wait(self):
		while self.running:
			sleep(1)


	def getPool(self):
		if not self.POOL:
			return None

		a=self.POOL.pop(0)
		return a

	def getAllPools(self):
		res=self.POOL
		self.POOL=[]
		return res

	def Launch(self):
		self.Handler=threading.Thread(target=self.threadHandler, kwargs={})
		self.Handler.start()

	def threadHandler(self):
		while self.running:
			urls=self.getAllPools()
			if not urls:
				self.running=False
				break

			for url in urls:
				if not self.running:
					break
				path=urlparse(url)[2]
				if "." in path:
					ext=urlparse(url)[2].split(".")[-1]
				else: 
					ext=""

				if ext in self.CFG_reject:
					self.postFetch(None,url)
					self.doneUrls+=1
					continue

				self.Semaphore.acquire()
				
				th=threading.Thread(target=self.crawl, kwargs={"url":url})
				th.start()
				self.threads_list.append(th)


			temp=[]
			for thr in self.threads_list:
				if not thr.isAlive():
					temp.append(thr)

			for i in temp:
				i.join()
				self.threads_list.remove(i)

			if not self.running:
				for i in self.threads_list:
					i.join()
				self.threads_list=[]

	def crawl(self,url):
		try:
			sl=SearchLinks(url)
			sl.setProxy(self.CFG_proxy)
			sl.addCookie(self.CFG_cookie)
			for j in sl:
				self.append(j)
			if sl.status!="Ok":
				print "fallo en",url
			else:
				self.Semaphore_Mutex.acquire()
				self.Requests.append(sl.getRequest())
				self.Semaphore_Mutex.release()
				self.urlOKS.append(url)
				#self.CFG_cookie=sl.getCookie()
				self.postFetch(sl.getResponse(),url)
		except Exception,er:
			print "Crawler: ",er

		self.Semaphore_Mutex.acquire()
		self.doneUrls+=1
		self.Semaphore_Mutex.release()
		self.Semaphore.release()
	
	def setCookie(self,sk):
		self.CFG_cookie=sk

	def getRequests(self):
		self.Semaphore_Mutex.acquire()
		a=self.Requests[:]
		self.Requests=[]
		self.Semaphore_Mutex.release()
		return a

	def setProxy(self,proxy):
		self.CFG_proxy=proxy

if __name__=="__main__":
	a=DCrawl()
	a.run()
