#-*- coding: utf-8 -*-
import urllib,re,sys,os,urllib2,string
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
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
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;','-').replace('&#8217;',"'")
        match = re.findall('<a href="([^"]*)/" title="Watch ([^"]*) Online" ><span style="background-image: url[(]([^"]*)[)]" class="episode"></span>[^"]*<br />[^"]*</a><br /><small>[^"]*<br />',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,name,thumb in match:
                name=name.replace('-','').replace('&','').replace('acute;','').strip()
                thumb = base_url + thumb
                main.addDirTE(name,url,2,'','','','','','')
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


def Index2(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;','-').replace('&#8217;',"'")
        match = re.findall('Watch it here :.+?<a href="([^"]*)">([^"]*)</a>',link)
        for url,name in match:
                main.addDirTE(name,url,3,'','','','','','')


def TVLIST(url):
        for i in string.ascii_uppercase:
                main.addDir(i,base_url +'tv-streaming/#'+i.upper(),5,art+'/'+i.lower()+'.png')

def TVLISTB(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','')
        response.close()
        match=re.compile('<li><a href="([^"]*)" title="[^"]*">[%s]([^"]*)</a>'% name).findall(link)
        for url,title in match:
            title=name+title
            url = base_url + url
            print url
            addDir(title,url,6,'')  
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)

        xbmcplugin.endOfDirectory(int(sys.argv[1])) 
        
def Seasons(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','')
        response.close()
		
        match=re.compile('<span style="color: #339966;"><strong>([^"]*)</strong></span></p><ul><li>').findall(link)
        for season in match:
                addDir(season,url,7,'')

def Episodes(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','')
        response.close()
		
        match=re.compile('<strong><a href="([^"]*)">([^"]*)</a> &#8211;[%s]([^"]*)</strong></li>'% name).findall(link)
        for url,episode,title in match:
                title='[COLOR blue]'+episode+'[/COLOR]'+ ' - ' +'[COLOR red]'+title+'[/COLOR]'
                addDir(title,url,3,'')                


                
def VIDEOLINKS(url,name):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','').replace('YouWa','Youwatch').replace('Putlo','Putlocker').replace('Socksh','Sockshare').replace('ExaSh','Exashare').replace('AllMyV','All My Videos ')
        match=re.compile('<a href="([^"]*html)">([^"]*)</a></strong></p>').findall(link)
        for url,name in match:
                name = '[COLOR red]'+name+'[/COLOR]'
                main.addDir(name,url,6,'')
        matcha=re.compile('<b>([^"]*)</b></span><br /><IFRAME SRC="([^"]*)"').findall(link)
        for name,url in matcha:
                    main.addDir(name,url,50,'')
        matchb=re.compile('<b>([^"]*)</b></span><br /><iframe src="([^"]*)"').findall(link)
        for name,url in matchb:
                    main.addDir(name,url,50,'')




def Resolve():
    main.addLink('Play',urlresolver.resolve(str(url)),art+'/play.png')
    
