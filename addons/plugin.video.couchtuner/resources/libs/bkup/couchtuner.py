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
reload(sys)
sys.setdefaultencoding( "UTF-8" )


#CouchTuner - by Kasik 2014.

addon_id = 'plugin.video.couchtuner'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
base_url='http://www.couchtuner.eu/'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

######################################################################################################################
def Index(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;','-').replace('&#8217;',"'").replace('season-','s').replace('episode-','e')
        response.close()
	match = re.findall('<a href="([^"]*)/" title="Watch ([^"]*) Online" ><span style="background-image: url[(]([^"]*)[)]" class="episode"></span>[^"]*<br />[^"]*</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url, name, thumb in match:
                thumb = base_url + thumb
                main.addInfo(name,'http://www.zzstream.li/'+url+'.html',3,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        
        
        nextpage=re.compile('<strong>Previous <a href="([^"]*)">[[][^"]*[]]</a>').findall(link)
        for url in nextpage:
                main.addDir('Next Page >>',base_url+url,1,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()



def TVLIST(url):
        for i in string.ascii_uppercase:
                main.addDir(i,base_url +'tv-streaming/#'+i.upper(),5,art+'/'+i.lower()+'.png')

def TVLISTB(url):
        link=main.OPENURL(url)
        link=link.replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','')
        match=re.compile('<li><a href="([^"]*)" title="[^"]*">[%s]([^"]*)</a>'% name).findall(link)
        for url,title in match:
            title=name+title
            url = base_url + url
            print url
            main.addDir(title,url,6,'')  
        
def Seasons(url):
        link=main.OPENURL(url)
        link=link.replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','')
        match=re.compile('<span style="color: #339966;"><strong>([^"]*)</strong></span></p><ul><li>').findall(link)
        for season in match:
                main.addDir(season,url,7,'')

def Episodes(url):
        link=main.OPENURL(url)
        link=link.replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','')
        match=re.compile('<strong><a href="([^"]*)">([^"]*)</a>[%s]([^"]*)</strong></li>'% name).findall(link)
        for url,episode,title in match:
                title='[COLOR blue]'+episode+'[/COLOR]'+ ' - ' +'[COLOR red]'+title+'[/COLOR]'
                main.addDir(title,url,3,'')

                
def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','').replace('YouWa','Youwatch').replace('Putlo','Putlocker').replace('Socksh','Sockshare')
        response.close()
        match=re.compile('<a href="([^"]*html)">([^"]*)</a></strong></p>').findall(link)
        for url,name in match:
                name = '[COLOR red]'+name+'[/COLOR]'
                addDir(name,url,6,'')
        matcha=re.compile('<b>([^"]*)</b></span><br /><IFRAME SRC="([^"]*)"').findall(link)
        for name,url in matcha:
                    addDir(name,url,50,'')
        matchb=re.compile('<b>([^"]*)</b></span><br /><iframe src="([^"]*)"').findall(link)
        for name,url in matchb:
                    addDir(name,url,50,'')



def Resolve():
    main.addLink('Play',urlresolver.resolve(url),art+'/play.png')


####################################
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

              
params=get_params()
url=None
name=None
mode=None
season=None

try:
        season=urllib.unquote_plus(params["season"])
except:
        pass
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Season: "+str(season)        
####################################        

     
