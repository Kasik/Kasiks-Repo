import urllib,urllib2,base64,cookielib,sys
import re, string, os, urlresolver
import HTMLParser
h = HTMLParser.HTMLParser()
from t0mm0.common.net import Net
import xbmc,xbmcgui, xbmcaddon, xbmcplugin
from BeautifulSoup import MinimalSoup as BeautifulSoup
import main
net = Net()

base_url='http://megabox.li/'
art = main.art

def XXX_URL(url):
    req = urllib2.Request(url)
    #req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    #response = urllib2.urlopen(req)
    req.add_header('Cookie', 'xxx_access=1; path="/"; domain="megabox.li"; path_spec;')
    response = urllib2.urlopen(req)
    link=response.read()
    return link


def XXX(url):
     link=XXX_URL(url)
     link=link
     #match=re.compile('src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="([^"]*)">([^"]*)</a></div><ul class=\'star-rating\'><li class="current-rating" style="width:0%"></li>').findall(link)
     match=re.compile('<div class="item"><a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a>').findall(link)
     for url,thumb,name in match:
      url = base_url + url   
      main.addDir(name,url,71,thumb,'')

     nexturl=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
     for url in nexturl:
      url = base_url + url  
      main.addDir('Next Page >',url,70,'','')


def SEARCHXXX(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Search Megabox Adult" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title + '&xxx=&x=0&y=0'
	print "Searching URL: " + searchUrl 
	XXX(searchUrl)


def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

def AZXXX():
    main.addDir('#','http://megabox.li/?xxx&letter=1/',70,art+'/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,'http://megabox.li/?xxx&letter='+i.lower(),70,art+'/'+i.lower()+'.png')
   



def GRABXXX(url):
    link=XXX_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    #main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    moviename=re.compile('watch-xxx.php[?]id=[^"]*&movie=([^"]*)&link=[^"]*&type=xxx&ref=1').findall(link)
    for moviename in moviename:
     match=re.compile('href="info.php[?]id=([^"]*)&xxx&link=([^"]*)&host=([^"]*)"><div class="[^"]*"><span class="([^"]*)">').findall(link)
     for link1,link2,host,quality in match:
      if 'epornik' in host:
       url = base_url + 'watch-xxx.php?id='+link1+'&movie='+moviename+'&link='+link2+'&type=xxx&ref=1'
       main.addDir(moviename.replace('+',' ').strip()+" [COLOR yellow]"+host.upper()+"[/COLOR]",url,73,'.png','.png')   
      else:
       url = base_url + 'watch-xxx.php?id='+link1+'&movie='+moviename+'&link='+link2+'&type=xxx&ref=1'
       main.addDown2(moviename.replace('+',' ').strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,72,'.png','.png')   
             
     

def PLAYXXX(name,url):
        sources = []
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,2000)")
        match=re.compile('<IFRAME SRC="([^"]*)" FRAMEBORDER').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src="([^"]*)"></iframe>').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('action=\'([^>]*)\'>').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src="([^>]*)" frameborder="0" allowfullscreen=""></iframe></textarea></p>').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)        
        match=re.compile('src=\'([^>]*)\' scrolling=\'no\'></iframe></textarea>').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        if (len(sources)==0):
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Show doesn't have playable links,5000)")
      
        else:
                source = urlresolver.choose_source(sources)
                if source:
                        stream_url = source.resolve()
                        if source.resolve()==False:
                                xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Cannot Be Resolved,5000)")
                                return
                else:
                      stream_url = False
                      return
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                listitem.setInfo('video', {'Title': name, 'Year': ''} )       
                xbmc.Player().play(str(stream_url), listitem)
                main.addDir('','','','')      


def Epornik1(url):
    link=main.OPENURL(url)
    main.addLink("[COLOR red]-  Epornik -[/COLOR]",'','')
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    firstmatch=re.compile('src="([^"]*)"></iframe>').findall(link)
    for url in firstmatch:
     main.addDown2("[COLOR blue]PLAY[/COLOR]",url,74,'.png','.png')

def Epornik2(url,name):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    match=re.compile('file: "([^"]*)",').findall(link)
    for url in match:
      xbmc.Player().play(url)

###################################################################################################################
