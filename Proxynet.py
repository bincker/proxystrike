#!/usr/local/bin/python


#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

PKEY='''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCtPBY7Pg267CJl7384EqTyS3iDdn7mUCyPHnH03LsMYgzumZpm
HPYPis4kJBjcamwnOk4ybIup0c6ZRinB4x3brdzA6NzUvGHj/TWEEkXyB1GjNQvn
RrShRAzKkLC73FkDHf3EGVvfex1pOnbNXCZEgp1q06xzvm7SktxHswXy3QIDAQAB
AoGALGOeKrX+3KvPMKGKzrpwS6mtCrqdT7Sxhka92omI4GZre+QeHRZEsrzVj4s0
V55pci/Ng7wumWgqcTn6TzU8G/dIgh07SprD4m3DlXO7G1HUHEuZurvzJQjKa4A/
gS/vlKHjQuFxZlDI0H+w2dlcbdb1XO2/OKT7JGH/v0ZwND0CQQDc0bXVWiyHOkx5
ICxr48QJFbWND4RuVc5Kv7QFDoOPSq8YNk0JqlPFSFrcfDsGLrXYAEh07U5987L8
M2viuxurAkEAyNWa/N2+wNjpjTrXJlJXBFNH7EfXTWtLWFAWNxKYaRgTdIgc2WN3
pVIOZ7b0SxvWBRI+aw/X+YV0HegHB2DjlwJBAMKGRz2020chN1741ckRc49hPXcP
dWVRV5KHwEk4GPMxIoAczc626mb/r3NOSRzQJ0cqMKo4pw3TkhgUIHUyyVMCQQCj
9ohng54VkcHzdKNsfPLf7CIfDHQBl+RWgGPyqHLX8jkH/YwYCvYGeZybHioKG/q5
/zAIdlHsPAEV3XXHl1mXAkBasQa/hAIBbmDJHnOQTu2p5Ck6k2LgSbhE1ZUSCVcj
42s2iIUvH5+SqSYAT4sZc91l7uY/oqv6DoahclHEfEvl
-----END RSA PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
MIICkzCCAfwCCQCyb5PFC9XyCTANBgkqhkiG9w0BAQUFADCBjTELMAkGA1UEBhMC
U1AxDDAKBgNVBAgTA0JDTjEMMAoGA1UEBxMDQkNOMRYwFAYDVQQKEw1lZGdlLXNl
Y3VyaXR5MRYwFAYDVQQLEw1lZGdlLXNlY3VyaXR5MRAwDgYDVQQDEwdkZWVwYml0
MSAwHgYJKoZIhvcNAQkBFhFkZWVwYml0QGdtYWlsLmNvbTAeFw0wODEwMTUwODI0
MjdaFw0xMTA3MTEwODI0MjdaMIGNMQswCQYDVQQGEwJTUDEMMAoGA1UECBMDQkNO
MQwwCgYDVQQHEwNCQ04xFjAUBgNVBAoTDWVkZ2Utc2VjdXJpdHkxFjAUBgNVBAsT
DWVkZ2Utc2VjdXJpdHkxEDAOBgNVBAMTB2RlZXBiaXQxIDAeBgkqhkiG9w0BCQEW
EWRlZXBiaXRAZ21haWwuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCt
PBY7Pg267CJl7384EqTyS3iDdn7mUCyPHnH03LsMYgzumZpmHPYPis4kJBjcamwn
Ok4ybIup0c6ZRinB4x3brdzA6NzUvGHj/TWEEkXyB1GjNQvnRrShRAzKkLC73FkD
Hf3EGVvfex1pOnbNXCZEgp1q06xzvm7SktxHswXy3QIDAQABMA0GCSqGSIb3DQEB
BQUAA4GBAEl8GtQT/yBRJvU+x7k6R8SjSy4Ew+bMsRcaNWySDF570+txt8ImkTR4
w8I49REha97jnXuYkpdHAHrImpU9EsCFAMGXsd+tYVZZOZyr0/z7ooS6/YAXgKm3
jF0mwEuUUOz0lTl2Rym9ZSDE2DRMC7oqZPeuYt6ZP0ZaVWAg8sWy
-----END CERTIFICATE-----
'''

from reqresp import *
from OpenSSL import SSL,crypto
import threading
import re

mutex=1
Semaphore_Mutex=threading.BoundedSemaphore(value=mutex)


import BaseHTTPServer, select, socket, SocketServer, urlparse

class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
	__base = BaseHTTPServer.BaseHTTPRequestHandler
	__base_handle = __base.handle

	server_version = "Vapwn PROXY V4.0"
	rbufsize = 0						# self.rfile Be unbuffered

	def _connect_to(self, netloc, soc):
		i = netloc.find(':')
		if i >= 0:
			host_port = netloc[:i], int(netloc[i+1:])
		else:
			host_port = netloc, 80
		try: soc.connect(host_port)
		except socket.error, arg:
			try: 
				msg = arg[1]
			except: 
				msg = arg
				try:
					self.send_error(404, msg)
				except:
					pass
			return 0
		return 1


	def do_CONNECT(self):
		global PKEY
		try:
			self.wfile.write(self.protocol_version + " 200 Connection established\r\n")
			self.wfile.write("Proxy-agent: %s\r\n" % self.version_string())
			self.wfile.write("\r\n")
	
			ctx = SSL.Context(SSL.SSLv23_METHOD)
			ctx.set_timeout(5)
			ctx.use_privatekey(crypto.load_privatekey(crypto.FILETYPE_PEM,PKEY))
			ctx.set_verify(SSL.VERIFY_NONE,self.test)
			ctx.use_certificate(crypto.load_certificate(crypto.FILETYPE_PEM,PKEY))
			sok=SSL.Connection(ctx,self.connection)
			sok.set_accept_state()
		
			ssldat=self._read(sok,300)
				
			reqHand=RequestHandler(self.path,ssldat,sok,"https",self.connection)
			Proxynet.queueRequest(reqHand)
			reqHand.execute()

		except Exception,a:
			print "Exception in do_CONNECT\r\n-------------------------------\r\n",a,"\r\n------------------------------\r\n"

	def test():
		return ok

	def do_GET(self):
		(scm, netloc, path, params, query, fragment) = urlparse.urlparse( self.path, 'http')

		if scm != 'http' or fragment or not netloc:
			self.send_error(400, "bad url %s" % self.path)
			return

		try:
			rawrequest="%s %s %s\r\n" % ( self.command, urlparse.urlunparse(('', '', path, params, query, '')), self.request_version)
			if not "Authorization" in self.headers:
				self.headers['Connection'] = 'close'
			del self.headers['Proxy-Connection']
			for key_val in self.headers.items():
				rawrequest+="%s: %s\r\n" % key_val
			rawrequest+="\r\n"
		
			rawrequest+=self._read(self.connection,300)
	
			reqHand=RequestHandler(self.path,rawrequest,self.connection,"http")
			Proxynet.queueRequest(reqHand)
			reqHand.execute()

		except Exception,a:
			print "Exception in do_GET\r\n-------------------------------\r\n",a,"\r\n------------------------------\r\n"
			

	def _read(self, soc, max_idling=20):
		iw = [soc]
		ow = []
		count = 0
		rawrequest=""
		while 1:
			count += 1
			(ins, _, exs) = select.select(iw, ow, iw, 0.5)
			if exs: break
			if ins:
				rawrequest+= soc.recv(8192)
			else:
				break
			if count == max_idling:
				break

		return rawrequest
	

	def _read_write(self, soc, max_idling=20,rawrequest=""):
		iw = [self.connection, soc]
		ow = []
		count = 0
		rawresponse=""
		while 1:
			count += 1
			(ins, _, exs) = select.select(iw, ow, iw, 3)
			if exs: break
			if ins:
				for i in ins:
					if i is soc:
						out = self.connection
						data = i.recv(8192)
						rawresponse+=data
					else:
						out = soc
						data = i.recv(8192)
						rawrequest+=data
					if data:
						out.send(data)
						count = 0

			if count == max_idling:
				break

		if len(rawresponse)>0 and len(rawrequest)>0:
			req=Request()
			req.parseRequest(rawrequest)
			req.response=Response()
			req.response.parseResponse(rawresponse)
			Proxynet.addRequest(req)


	do_HEAD = do_GET
	do_POST = do_GET
	do_PUT  = do_GET
	do_DELETE=do_GET

class ThreadingHTTPServer (SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer): 
	pass

	
	
class proxy (threading.Thread):
	def __init__ (self,port):
		threading.Thread.__init__(self)
		self.exclude=""
		self.stop=False
		self.server_address = ('', port)
		self.httpd = ThreadingHTTPServer(self.server_address, ProxyHandler)


	def run(self):
		while not self.stop:
			self.httpd.handle_request()
		del self.httpd


class RequestHandler:
	def __init__(self,path,raw,browser_soc,protocol,soc_orig=None):
		self.__raw=raw
		self.path=path
		self.__protocol=protocol
		self.__browser_soc=browser_soc
		self.__soc_orig=soc_orig
		self.__mutex=threading.BoundedSemaphore(value=1)
		self.__destroy=False

	def acquire(self):
		self.__mutex.acquire()

	def release(self):
		self.__mutex.release()


	def destroy(self):
		self.__browser_soc.close()
		if self.__protocol=="https":
			self.__soc_orig.close()
		
		self.__destroy=True

	def getRawRequest(self):
		return self.__raw

	def setRawRequest(self,raw):
		self.__raw=raw

	def execute(self):
		self.__mutex.acquire()
		if not self.__destroy:

#			if self.__protocol=="http" and Proxynet.intercepting():
#				self.fastExecute()
#			else:
			r=Request()
			r.parseRequest(self.__raw,self.__protocol)

			self.PREPROCESS(r)

			r.perform()

			if self.__protocol=="https" and Proxynet.getProxy() and r.response.code<200:
					nr=Response()
					nr.parseResponse(r.response.getContent())
					if nr.has_header("www-authenticate"):
						nr.delHeader("connection")
					self.__browser_soc.sendall(nr.getAll())
					r.response=nr
			else:
					if r.response.has_header("www-authenticate"):
						r.response.delHeader("connection")
					self.__browser_soc.sendall(r.response.getAll())

			Proxynet.addRequest(r)
# 			fin else

			self.__browser_soc.close()
			if self.__protocol=="https":
				self.__soc_orig.close()

		self.__mutex.release()

	def fastExcute(self):
		host=urlparse.urlparse(self.path)[1]
		pair=host.split(":")
		if len(pair)==1:
			port=80
		else:
			host,port=pair

		sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM) 
		sock.connect((host, port))

		iw = [self.__browser_soc, sock]
		ow = []
		count = 0
		rawresponse=""
		while 1:
			count += 1
			(ins, _, exs) = select.select(iw, ow, iw, 3)
			if exs: break
			if ins:
				for i in ins:
					if i is soc:
						out = self.connection
						data = i.recv(8192)
						rawresponse+=data
					else:
						out = soc
						data = i.recv(8192)
						rawrequest+=data
					if data:
						out.send(data)
						count = 0

			if count == max_idling:
				break

	def _read(self, soc, max_idling=20):
		iw = [soc]
		ow = []
		count = 0
		rawrequest=""
		while 1:
			count += 1
			(ins, _, exs) = select.select(iw, ow, iw, 0.5)
			if exs: break
			if ins:
				rawrequest+= soc.recv(8192)
			else:
				break
			if count == max_idling:
				break

		return rawrequest

	def PREPROCESS(self,req):
			if Proxynet.get_signGET():
				req.addVariableGET(Proxynet.get_signGET(),"")

			if Proxynet.get_headersign():
				h,v=Proxynet.get_headersign()
				req.addHeader(h,v)

			if Proxynet.getProxy():
				req.setProxy(Proxynet.getProxy())





class Proxynet:
	__PROXY_REQUESTS=[]
	__nreqs=0
	exclude=None
	__header={}
	__get_sign=""
	__USEPROXY=None

	__port=8008
	__prox=None
	__start=False

	__intercept=False
	__INTERCEPT_REQS=[]

	@staticmethod
	def changePort(port):
		if port!=Proxynet.__port:
			if not Proxynet.__prox:
				Proxynet.__port=port
			else:
				Proxynet.stop()
				Proxynet.__port=port
				Proxynet.__prox=proxy(Proxynet.__port)
				Proxynet.__prox.start()



	@staticmethod
	def init (exclude=""):
		Proxynet.__prox=proxy(Proxynet.__port)
		Proxynet.exclude=exclude.lower()

		Proxynet.__prox.start()

	@staticmethod
	def stop ():
		if Proxynet.__prox:
			Proxynet.__prox.stop=True
			a=Request()
			a.setUrl("http://localhost:%d"%(Proxynet.__port))
			a.perform()
			Proxynet.__prox.join()	
			del Proxynet.__prox
			Proxynet.__prox=None
	
############ LIMITACION Y FIRMAS ##################

	@staticmethod
	def signGET(var):
		Proxynet.__get_sign=var

	@staticmethod
	def signHeaders(var,value):
		Proxynet.__header={}
		if not var:
			Proxynet.__header={}
		else:
			Proxynet.__header[var]=value



	@staticmethod
	def get_signGET():
		return Proxynet.__get_sign

	@staticmethod
	def get_headersign():
		if len  (Proxynet.__header):
			return  Proxynet.__header.items()[0]
		else:
			return ()



############# PROXY STUFF ######################

	@staticmethod
	def setProxy(p):
		Proxynet.__USEPROXY=p

	@staticmethod
	def getProxy():
		return Proxynet.__USEPROXY

############### INTERCEPT STUFF #################

	@staticmethod
	def setIntercept(b):
		Proxynet.__intercept=b
		if b==False:
			for i in Proxynet.__INTERCEPT_REQS:
				i.release()
			Proxynet.__INTERCEPT_REQS=[]

	@staticmethod
	def intercepting():
		return Proxynet.__intercept



	@staticmethod
	def queueRequest(r):
		if Proxynet.__intercept:
			r.acquire()
			Proxynet.__INTERCEPT_REQS.append(r)

	@staticmethod
	def processIntercepted(r):
		r.release()

	@staticmethod
	def destroyIntercepted(r):
		r.destroy()
		r.release()

	@staticmethod
	def getIntercepted():
		if  Proxynet.__INTERCEPT_REQS:
			return Proxynet.__INTERCEPT_REQS.pop(0)
		else:
			return None
		

################################################

	@staticmethod
	def addRequest(r):
		if not re.search(Proxynet.exclude,r.urlWithoutVariables.lower()):	
			Semaphore_Mutex.acquire()
			Proxynet.__PROXY_REQUESTS+=[r]
			Proxynet.__nreqs+=1
			Semaphore_Mutex.release()
		
		
	@staticmethod
	def getRequest():
		Semaphore_Mutex.acquire()
		if Proxynet.__nreqs:
			Proxynet.__nreqs-=1
			a=Proxynet.__PROXY_REQUESTS.pop(0)
			Semaphore_Mutex.release()
			return a
		else:
			Semaphore_Mutex.release()
			return None

	@staticmethod
	def getNumberRequests ():
		return Proxynet.__nreqs

	@staticmethod
	def clearRequests ():
			Semaphore_Mutex.acquire()
			Proxynet.__PROXY_REQUESTS
			Proxynet.__nreqs=0
			Semaphore_Mutex.release()

	@staticmethod
	def addRequests (reqs):
		Semaphore_Mutex.acquire()
		for i in reqs:
			if not re.search(Proxynet.exclude,i.urlWithoutVariables.lower()):	
				Proxynet.__PROXY_REQUESTS+=[i]
				Proxynet.__nreqs+=1
		Semaphore_Mutex.release()
			
	
if __name__=="__main__":
	p=Proxynet()
	
	p.init("\.(jpg|gif|swf|ico|png|bmp|zip|rar|t?gz)$")
	
	print "Escuchando en 8008"
	try:
		while True:
			pass
	except:
		pass
	print "exiting..."
	p.stop()
