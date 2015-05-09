![http://farm4.static.flickr.com/3411/3251415324_242d45c681.jpg](http://farm4.static.flickr.com/3411/3251415324_242d45c681.jpg)

**[My new security blog @ http://deesec.com/](http://deesec.com/)**

**NEW** [Plugins Howto](http://code.google.com/p/proxystrike/wiki/PluginsHowto)

**ProxyStrike v2.1** is an active Web Application Proxy.
It's a tool designed to find vulnerabilities while browsing
an application. It was created because the problems we faced
in the pentests of web applications that depends heavily
on Javascript, not many web scanners did it good in this
stage, so we came with this proxy.

Right now it has available Sql injection and XSS plugins.
Both plugins are designed to catch as many vulnerabilities
as we can, it's that why the SQL Injection plugin is a
Python port of the great DarkRaver "Sqlibf".

The process is very simple, ProxyStrike runs like a
proxy listening in port 8008 by default, so you
have to browse the desired web site setting your browser to
use ProxyStrike as a proxy, and ProxyStrike will analyze
all the paremeters in background mode. For the user is a
passive proxy because you won't see any different in the
behaviour of the application, but in the background is
very active. :)

Download sources and run with **python proxystrike.py**
or try the executable versions.

| **Sources** | [Link](http://code.google.com/p/proxystrike/source/checkout) |
|:------------|:-------------------------------------------------------------|
| **Executable Version (Linux) (March 18 2009)** | [Proxystrike-2.2.tar.bz2](http://proxystrike.googlecode.com/files/proxystrike-2.2.tar.bz2) |
| **Executable Version (Windows) (March 18 2009)** | [ProxyStrike-2.2.zip](http://proxystrike.googlecode.com/files/ProxyStrike-2.2.zip) |
<a href='http://www.youtube.com/watch?feature=player_embedded&v=l8kioy4QX7U' target='_blank'><img src='http://img.youtube.com/vi/l8kioy4QX7U/0.jpg' width='725' height=450 /></a>

### Features: ###

  * Plugin engine (Create your own plugins!)
  * Request interceptor
  * Request diffing
  * Request repeater
  * Automatic crawl process
  * Http request/response history
  * Request parameter stats
  * Request parameter values stats
  * Request url parameter signing and header field signing
  * Use of an alternate proxy (tor for example ;D )
  * Sql attacks (plugin)
  * Server Side Includes (plugin)
  * Xss attacks (plugin)
  * Attack logs
  * Export results to HTML or XML

### Requeriments: ###
  * [Python](http://www.python.org)
  * [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download)
  * [PyOpenSSL](http://sourceforge.net/project/showfiles.php?group_id=31249&package_id=23298)
  * [PyCurl](http://pycurl.sourceforge.net/)