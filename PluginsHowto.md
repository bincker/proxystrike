This howto aims to show how to develop your own plugins for Proxystrike.

All the plugins must be in the "plugins" folder.
If you haven't got that folder, maybe your Proxystrike version is too old, so upgrade ;D.

In this folder you can find two examples: [demoplugin.readme](http://proxystrike.googlecode.com/svn/trunk/plugins/demoplugin.readme) and [demoplugin2.readme](http://proxystrike.googlecode.com/svn/trunk/plugins/demoplugin2.readme).

Below you can see the structure of ProxyStrike plugin engine:

![http://4.bp.blogspot.com/_-xXcbzWG3ug/SfHvtf3_u4I/AAAAAAAAAHg/jovD7Ff-niw/s1600/struct.png](http://4.bp.blogspot.com/_-xXcbzWG3ug/SfHvtf3_u4I/AAAAAAAAAHg/jovD7Ff-niw/s1600/struct.png)

Each request processed by the proxy is stored in a POOL and proccesed by every plugin 'enabled' in that very moment.

Features:
  * each plugin has it's own thread controller
  * each plugin has it's own cache, implemented for not process the same requests innecessarely
  * A plugin can export to HTML and XML formats

The requirements for develop a plugin are a few:
  * Inherit from **AttackPlugin**
  * Overload the **process** method
  * _optional_: Overload getHTML and getXML to export reults

Below I show a plugin example of an email collector plugin for Proxystrike. This plugin looks for emails in the responses (html) processed by the proxy and stores it in a tree widget in the ProxyStrike GUI:

```
class email_detect(AttackPlugin):
	def __init__(self):
		AttackPlugin.__init__(self,name="email detect",variableSet=False,iface=True,type="tree",fields=["Url","Email"])

		self.emailre=re.compile("[a-z0-9_.-]+@[a-z0-9_.-]+",re.I)

	def process(self,req):
		html=req.response.getContent()

		a=self.emailre.findall(html)

		results=[]

		for i in a:
			results.append([i])

		if a:   
			self.putRESULTS([req.completeUrl,results]) 
```


So, let's explain the code:

### AttackPlugin constructor parameters ###

You need to call the constructor of AttackPlugin to configure the plugin. Next i'll explain every parameter:

  * name (_string_): The name of the plugin shown in the GUI

  * variableSet (_boolean_):
    * True: Requests with the same variable set are processed by the plugin only once. For example: index.php?a=1&b=2 - index.php?a=23&b=45. Only the first request will be processed. There are plugins that doesn't need to process all the requests, for examples SQL and XSS.
    * False: All requests are processed by the plugin (only once obviously)

  * iface (_Boolean_): True: The plugin has interface. False: The plugin doesn't have interface.

  * type (_string_): It can be "tree" or "text" depending on the interface widget you wish to use in the GUI.

  * fields (_string`[]`_): This is an array of strings that contains the header fields of the "tree" widget. (_only needed if type=='tree'_)

### Overloading process() method ###

You need to overload process method.

This method is called by the proxy if the plugin is enabled, and the request is passed as a parameter ('req').

req is an instance of a Request. I recommend you to become familiar with the ReqResp module to work with requests and reponses.

### Storing the results ###

To store the results of the plugin you must use **_putRESULTS()_** method. The parameter used in this method depends on the widget's type (tree or text).

Let's explain each case:

  * tree: You need to pass a string list, and only one format is allowed (not very flexible for the time being). Imagine we have 4 fields (A,B,C,D):
```
A       B       C       D
info1                   
|_      info2   info3   info4						

    String list passed to putRESULTS: ['info1',['info2','info3','info4']]

	
A       B       C       D
info1                   
|_      info2   info3   info4						
|_	info21  info32  info43						

    String list passed to putRESULTS: ['info1',['info2','info3','info4'],['info21','info32','info43']]
```

  * text: When text widget is used, you must to pass a string ( Simple ;) )


