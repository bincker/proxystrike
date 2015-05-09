This library was developed over pycurl library to make an abstraction of requests and responses.

You can download it [here](http://proxystrike.googlecode.com/svn/trunk/reqresp.py).

You also need the [TextParser](http://proxystrike.googlecode.com/svn/trunk/TextParser.py) library and [pycurl](http://pycurl.sourceforge.net/) module

Next i'll expose the reqresp API and some examples:

### examples ###
```
from reqresp import *

a=Request()                        # Create a request object
a.setUrl("http://www.google.es/")  # set google url
a.perform()                        # performs the request
print a.response.getContent()      # prints http://www.google.es/ HTML code

a.setUrl("http://example.com/login.php")
a.setVariablePOST("username","deepbit")   # add post variable username=deepbit
a.setVariablePOST("password","1234")      # add post variable password=1234
a.perform()  

print a.response.getHeaders()      # print response headers
print a.response.code              # print response code
```

### Variable Class ###
```
class Variable:
        __init__(self,name,value="",extraInfo=""):
        '''Constructor'''

        restore(self):
        '''If value is modified with _append()_ or _update()_ it can be restored'''

        change(self,newval):
        '''Changes variable value. _restore()_ has no effect'''

        update(self,val):
        '''Updates variable value'''

        append(self,val):
        '''append information in the variable`s value'''

        __str__(self):
        '''string representation of the variable'''
```

### VariablesSet Class ###

```
class VariablesSet:
        names(self):
        '''{}: returns variable names in a hash'''

        existsVar(self,name):
        '''True if variable name `name` exists in the set'''

        addVariable(self,name,value="",extraInfo=""):
        '''Add a variable to the set'''


        getVariable(self,name):
        '''Returns variable given a variable name'''

```

### Request Class ###
```
Attributes:
    - urlWithoutVariables
    - pathWithVariables
    - completeUrl
    - finalUrl
    - urlWithoutPath
    - path
    - postdata

Methods:

        __str__(self):
        '''String representation of the request'''

        getXML(self,obj):
        '''Xml representation of the request'''

        getHost(self):
        '''Host, eg: www.google.com'''

        setUrl (self, urltmp):
        '''sets an url to perform the request'''

        setProxy (self,prox):
        '''sets a proxy to perform the request'''

        setFollowLocation(self,value):
        '''True: if response is 302 follow's the location header'''

        setConnTimeout (self,time):
        '''Timeout in seconds for the connection'''

        setTotalTimeout (self,time):
        '''Timeout in seconds for total transfer'''

        setAuth (self,method,string):
        '''sets auth string (user:passwd) for a given method (digest,basic,ntlm)

        getAuth (self):

        existsGETVar(self,key):

        existPOSTVar(self,key):

        setVariablePOST (self,key,value):

        setVariableGET (self,key,value):

        getGETVars(self):
        '''return all variables passed through the URL'''

        getPOSTVars(self):
        '''return all variables passed through the body'''

        setPostData (self,pd,boundary=None):
        '''set post data passed via string'''

        addHeader (self,key,value):
        '''add a header to the request'''

        delHeader (self,key):
        '''delete a header'''

        __getitem__ (self,key):
        '''access a header'''

        perform(self):
        '''launchs the request. Response is stored in response attribute'''

        getAll (self):
        '''get the RAW request'''

        parseRequest (self,rawRequest,prot="http"):
        '''fills the request values parsing a raw request'''

```

### Response Class ###
```
Attributes:
    - protocol         # HTTP/1.1
    - code                      # 200
    - message                # OK
 
Methods:
        addHeader (self,key,value):
        '''Adds a header'''

        delHeader (self,key):
        '''Delete header'''

        addContent (self,text):
        '''Add content to the response'''

        __getitem__ (self,key):
        '''get headers'''

        getCookie (self):
        '''return the cookie if set-cookie exists'''

        has_header (self,key):
        '''True: if header exists'''

        getLocation (self):
        '''Get Location value if 302 code is returned'''

        getHeaders (self):
        '''return all headers'''

        getContent (self):
        '''get the body of the response (HTML)'''

        getAll (self):
        '''get the RAW response'''

        parseResponse (self,rawResponse,type="curl"):
        '''fills the response object through a given RAW text'''


```