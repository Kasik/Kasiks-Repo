#-*- coding: utf-8 -*-
import urllib,re,sys,os,urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import string
import urlresolver
from BeautifulSoup import MinimalSoup as BeautifulSoup
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
net = Net()


#CouchTuner - by Kasik 2014.

addon_id = 'plugin.video.couchtuner'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
base_url='http://www.couchtuner.eu/'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

######################################################################################################################


def NEWRELEASE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;','-').replace('&#8217;',"'").replace('season-','s').replace('episode-','e').replace('#038;','')
        response.close()
		
        match=re.compile('<a href="http://www.couchtuner.eu/([^"]*)/" title="Watch ([^"]*) Online" ><span style="background-image: url[(]([^"]*)[)]" class="episode"></span>[^"]*<br />[^"]*</a>').findall(link)
        for url, name, thumb in match:
                thumb = base_url + thumb
                url = 'http://www.zzstream.li/'+url+'.html'
                print "Starting Here"+url
                main.addInfo(name,url,75,thumb,'','')
                
                                           
               
                       

        matchpage=re.compile('<div class="prev-page"><strong>Previous <a href="([^"]*)">[^"]*</a></strong>').findall(link)
        for nexturl in matchpage: 
                main.addDir('Next Page >>',base_url + nexturl, 1,art+'/next.png')


     

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\t','').replace('\r','').replace('\n','').replace('&#8211;','-').replace('&#8217;',"'").replace('IFRAME SRC','iframe src')
        response.close()
        putlocker=re.compile('<b>Putlo</b></span><br /><iframe src="([^"]*)" width').findall(link)
        if len(putlocker) > 0:
                addDownLink("[COLOR blue]Play[/COLOR]",url,75,'')
        



def Play(url,name):
        sources = []
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('IFRAME SRC','iframe src')
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,2000)")
        match=re.compile('[^"]*</b></span><br /><iframe src="([^"]*)"').findall(link)
        for url in match:
                url=url
                print url
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

       
       
                      

                
def Resolve():
    addLink('Play',urlresolver.resolve(url),art+'/play.png')


###########################################################################################################################################################################
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
        return ok

def addDownLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        ok=True
	name=BeautifulSoup(name, convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
###########################################################################################################################################################################
    
    
                
                
