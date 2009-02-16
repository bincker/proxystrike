#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

from reqresp import *
from TextParser import *
import sys
import re
from urlparse import urlparse
from urllib import unquote


class SearchEngine:
	retag=re.compile("<[^>]+>")
	remultag=re.compile("<[^>]+>(<[^>]+>)+")

	def __init__(self,query):
		query=query.replace(" ","%20")
		query=query.replace("+","%2b")
		query=query.replace("\"","%27")
		self.query=query
		self.cookie=None
		self.responseContent=""
		
		self.results=[]
		self.diccres={}
	
		self.startIndex=0               ## Index inicial del buscador
		self.increment=10				## incremento del index del buscador
		self.lastResult=""				
		self.start=None					## Index actual del buscador

		self.MoreResults=None
		self.proxy=None

		self.status="Ok"

		self.REQ=None


		########### Variables a modificar para cada engine #############
		self.url=None
		self.queryvar=None
		self.startvar=None
		self.urlextra=""

		self.urlRegexp=None            ## Regex para pillar las urls de los results
		self.nextRegexp=None		   ## Regex para saber si hay mas results

	def setProxy(self,proxy):
		self.proxy=proxy

	def getResponse(self):
		return self.responseContent

	def addCookie(self,c):
		self.cookie=c

	def getCookie(self):
		return self.cookie
		

	def __iter__(self):
		self.start=None
		self.MoreResults=None
		return self

	def addResult(self,res):
		res=self.trataResult(res)
		if not isinstance(res,list):
			res=[res]
		for i in res:
			if not str(i) in self.diccres:
				self.diccres[str(i)]=True
				self.results.append(i)

	def preProcess(self,raw):
		return raw

	def next(self):
		while not self.results:
			self.getNewPage()

		if not self.results:
			raise StopIteration

		self.lastResult=self.results.pop()

		if not self.lastResult:
			return self.next()

		return self.lastResult


	def fetchLast(self):
		r=Request()
		r.setUrl(self.lastResult)
		r.setTotalTimeout(10)
		r.setProxy(self.proxy)
		r.perform()
		return r.response.getContent()
	
	def limpiaString(self,res):
		res=SearchEngine.remultag.sub(" ",res)
		res=SearchEngine.retag.sub("",res)
		res=res.replace("&nbsp;"," ")
		res=res.replace("&amp;","&")
		res=res.strip()
		return res

	def trataResult (self,res):    ## Metodo hecho para sobrecargar si es necesario
		return self.limpiaString(res[0])

	def getNewPage(self):

		if self.MoreResults==False:
			raise StopIteration

		if self.start==None:
			self.start=self.startIndex
		else:
			self.start+=self.increment

		req=Request()
		req.addHeader("User-Agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.14) Gecko/20080418 Ubuntu/7.10 (gutsy) Firefox/2.0.0.14")
		url=self.url.replace("{query}",str(self.query))
		url=url.replace("{startvar}",str(self.start))


		req.setUrl(url)
		req.setTotalTimeout(10)
		req.setConnTimeout(10)
		if self.cookie:
			req.addHeader("Cookie",self.cookie)

		req.setProxy(self.proxy)
		req.setFollowLocation(True)

		trys=5
		while trys:
			try:
				req.perform()
				break
			except:
				trys-=1
				if not trys:
					self.status="Failed"
					raise StopIteration
				pass

		if not req.response.has_header('Content-Type') or not 'text' in req.response['Content-Type']:
			self.MoreResults=False
			return

		rawResponse=self.preProcess(req.response.getContent())

		self.cookie=req.response.getCookie()

		tp=TextParser()
		tp.setSource("string",rawResponse)
		if req.response.code==200:
			self.responseContent=req.response.getContent()

		while tp.readUntil(self.urlRegexp):
			for i in tp:
				self.addResult(i)

		tp.seekinit()

		if tp.readUntil(self.nextRegexp):
			self.MoreResults=True
		else:
			self.MoreResults=False

		self.REQ=req

	def getRequest(self):
		return self.REQ


	def getResult(self):
		try:
			return self.next()
		except:
			return None

	def getNResults(self,n):
		l=[]
		for i in range(n):
			try:
				l.append(self.next())
			except:
				break

		return l
			
		
	
class GoogleSearch(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)

		self.url="http://www.google.com/search?q={query}&start={startvar}&num=100"
	
		self.urlRegexp="\"([^\"]+)\" class=l"         
		self.nextRegexp=">Next<"		   
		self.increment=100


class YouTubeSearch(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)

		self.increment=1
		self.url="http://es.youtube.com/results?search_query={query}&page={startvar}"
	#	self.addCookie("PREF=f1=400000&gl=US&hl=en;")
#		self.urlRegexp='id="video-url-([^"]+)" +href="[^"]+" +rel="[^"]+"><img title="([^"]+)"'      
		self.urlRegexp='href="/watch\?v=([^"]+)"'      

		self.nextRegexp="class=\"pagerNotCurrent\">"

#	def trataResult(self,res):
#		return {res[0]:res[1]}

		


class MsnSearch(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)

		self.url="http://search.live.com/results.aspx?q={query}&first={startvar}&mkt=en-US&setlang=en-US"
	
		self.urlRegexp="<h3><a href=\"([^\"]+)\" onmousedown"         
		self.nextRegexp=">Next<"		   

		self.startIndex=1

#		self.increment=50
#		self.addCookie("SRCHUID=V=1&NRSLT=50;")

	def trataResult(self,res):
		res=self.limpiaString(res[0])

		if res[:4].lower()!="http":
			res="http://"+res

		return res

class YahooSearch(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)

		self.url="http://search.yahoo.com/search?p={query}&b={startvar}&ei=UTF-8&y=Search&xargs=0&pstart=0"
	
		self.urlRegexp="/\*\*(http[^\"]+)\""         
		self.nextRegexp=">Next &gt;"		   

		self.getCookie()
	
	def trataResult(self,res):
		res=self.limpiaString(res[0])

		if "yahoo" in res:
			return None

		res=unquote(res)

		return res
	
class YandexSearch(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)

		self.increment=1
		self.url="http://yandex.ru/yandsearch?text={query}&p={startvar}"
	
		self.urlRegexp="<a tabindex[^>]+href=\"([^\"]+)\""         
		self.nextRegexp="<a id=\"next_page\""


class TorrentzSearch(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)

		self.url="http://www.torrentz.com/search?q={query}&p={startvar}"
		self.increment=1
		self.startIndex=0

		self.nextRegexp="Next &raquo;</a>"
		self.urlRegexp="<dt><a href=[^>]+>(([^<]|<[^/]|</[^a])+)</a"         

class MininovaSearch(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)
	
		self.url="http://www.mininova.org/search/{query}/added/{startvar}"
		self.increment=1
		self.startIndex=1

		self.urlRegexp="<a href=\"/tor[^>]+>([^<]+)<"         
		self.nextRegexp="Next &raquo;</a>"

class ScrapeTorrentSearch(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)
	
		self.url="http://scrapetorrent.com/Search/index.php?search={query}&sort=seed&fz=&rd=&cat=x"
		self.increment=1
		self.startIndex=1

		self.urlRegexp="<td><a href=[^>]+>&nbsp;([^<]+)<"         
		self.nextRegexp="Deepbit is God"

class BaiduSearch(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)	

		self.url="http://www.baidu.com/s?lm=0&si=&rn=10&ie=gb2312&ct=0&wd={query}&pn={startvar}&ver=0&cl=3"
		self.increment=10
		self.startIndex=0

		self.urlRegexp="<a onclick=\"[^\"]+\" href=\"([^\"]+)"         
		self.nextRegexp="</font></a></div><br>"

class Figator(SearchEngine):
	def __init__(self,query):
		SearchEngine.__init__(self,query)	

		self.url="http://www.figator.com/search/{query}/10:{startvar}:rd"
		self.increment=10
		self.startIndex=0

		self.urlRegexp="<hr />([^<]+)<a"
		self.nextRegexp=":rd\">Next</a>"

def test(engineO,text,qty):
	try:
		sys.stdout.write( text )
		sys.stdout.flush()
		x=engineO.getNResults(qty)
		if len(x)==qty:
			print "OK"
		else:
			print "Failed"
	except KeyboardInterrupt:
		pass
	

if __name__=="__main__":
	from consoleNg import Console

	class Cli(Console):
		def __init__(self):
			Console.__init__(self,"iSearch: [ NoEngine ] > ")

			self.engines=[]
			self.cur_engine=-1
		
			for i,j in globals().items():
				if "getNResults" in dir(j) and i!='SearchEngine':
					self.engines.append(i)


		def CMD_showe(self,*args):
			'''1|showe|Show all engines'''
			j=1
			for i in self.engines:
				print str(j)+".",i
				j+=1

		def CMD_use(self,*args):
			'''2|use|Use one of the available engines'''
			j=1
			for i in self.engines:
				print str(j)+".",i
				j+=1
			try:
				n=int(raw_input("Select a number: "))
			except:
				return

			self.prompt="iSearch:[ %s ] > " % (self.engines[n-1])
			self.cur_engine=n-1

		def CMD_search(self,*args):
			'''3|search [query]|Perform a complete search using current search engine'''
			if self.cur_engine<0:
				raise Exception,"You must select an engine!! ('use' command)"

			string=" ".join(args)
			print string

			se=globals()[self.engines[self.cur_engine]](string)
			self.results=[]
			j=0
			print "Fetching results... WAIT PLEASE"
			for i in se:
				j+=1
				self.results.append(i)
			print j,"results fetched.\r\n"


					
		def CMD_searchN(self,*args):
			'''4|searchN [number] [query]|Retrieve N results using current search engine'''
			if self.cur_engine<0:
				raise Exception,"You must select an engine!! ('use' command)"
			n=int(args[0])
			string=" ".join(args[1:])

			se=globals()[self.engines[self.cur_engine]](string)
			self.results=[]
			j=0
			print "Fetching results... WAIT PLEASE"
			self.results=se.getNResults(n)
			print len(self.results),"results fetched.\r\n"



		def CMD_testall(self,*args):
			'''5|testall|Test all engines'''
			ys=YouTubeSearch("howto video")
			test(ys,"YouTube search --> \"edge\" (getting 147 results): ",147)
		
			ys=GoogleSearch("\"edge-security\"")
			test(ys,"Google search --> \"edge-security\" (getting 147 results): ",147)
			
			ys=YahooSearch("\"edge-security\"")
			test(ys,"Yahoo search --> \"edge-security\" (getting 147 results): ",147)
		
			ys=Figator("divx")
			test(ys,"Figator search --> \"divx\" (getting 147 results): ",147)
		
			ys=BaiduSearch("microsoft")
			test(ys,"Baidu search --> \"microsoft\" (getting 147 results): ",147)
		
			ys=ScrapeTorrentSearch("divx")
			test(ys,"ScrapeTorrent search --> \"divx\" (getting 95 results): ",95)
		
			ys=MininovaSearch("divx")
			test(ys,"Mininova search --> \"divx\" (getting 255 results): ",255)
		
			ys=TorrentzSearch("tomtom")
			test(ys,"Torrentz search --> \"tomtom\" (getting 147 results): ",147)
		
			ys=YandexSearch("edge-security")
			test(ys,"Yandex search --> \"edge-security\" (getting 147 results): ",147)

		def CMD_domains(self,*args):
			'''6|domains|Replace results by its domain names'''
			from urlparse import urlparse
			doms={}
			for i in self.results:
				doms[urlparse(i)[1]]=True

			self.results=doms.keys()

		def CMD_sr(self,*args):
			'''7|sr|Show results'''
			for i in self.results:
				print i

		def CMD_grep(self,*args):
			'''7|grep [regexp]|Show results matched against regexp'''
			import re
			exp=re.compile(" ".join(args))
			for i in self.results:
				if exp.findall(i):
					print i

				

	
	a=Cli()
	a.run()
	
		
