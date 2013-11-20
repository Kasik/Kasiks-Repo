import xbmc, xbmcgui, xbmcplugin, os
import urllib, urllib2, mechanize
import re, string, urlresolver, xbmcaddon
from metahandler import metahandlers
try:
    from addon.common.addon import Addon
    from addon.common.net import Net
except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("CouchTuner Import Failure", "Failed to import addon.common", "A component needed by CouchTuner is missing on your system", "Please visit www.xbmchub.com for support")

addon_id = 'plugin.video.couchtuner'
local = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.couchtuner', sys.argv)
net = Net()
Dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.couchtuner', ''))
grab = metahandlers.MetaData(preparezip = False)
metaget = metahandlers.MetaData()

#Art Setting
art = xbmc.translatePath('special://home/addons/plugin.video.couchtuner/resources/art/')
error_logo = xbmc.translatePath('special://home/addons/plugin.video.couchtuner/resources/art/sadface.png')
    
 
#Common Cache
import xbmcvfs
dbg = False # Set to false if you don't want debugging

#Common Cache
try:
  import StorageServer
except:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer('plugin.video.couchtuner')

from BeautifulSoup import MinimalSoup as BeautifulSoup

#PATHS
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/"

def icon_path(filename):
    return IconPath + filename

######################
#Metahandler
def GRABMETA(name,types):
        type = types
        EnableMeta = local.getSetting('Enable-Meta')
        if EnableMeta == 'true':
                if 'Movie' in type:
                        meta = grab.get_meta('movie',name,'',None,None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                          'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
                          'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                elif 'tvshow' in type:
                        meta = grab.get_meta('tvshow',name,'','',None,overlay=6)
                        infoLabels = {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                              'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
                              'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
                              'backdrop_url': meta['backdrop_url'],'status': meta['status']}
        return infoLabels

#########################
    


def MAIN():
        addDir('New Release',base_url,1,art+'/new.png')
        addDir('Tv Show List',base_url+'tv-streaming/',2,art+'/allshows.png')
        
       

def NEWRELEASE(url):
        EnableMeta = local.getSetting('Enable-Meta')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('&#8230;','-...').replace('&#8217;',"'").replace('\t','').replace('\n','').replace('\r','')
        response.close()
		
        match=re.compile('<span class="tvbox">.+?<a href="([^"]*)" title="[^"]*&#8211;([^"]*)" ><span style="background-image: url([^"]*)" class="episode"></span>([^"]*)<br />([^"]*)</a>').findall(link)
        for url, episode, thumb, show, season in match:
                name = '[COLOR blue]'+show+'[/COLOR]' +' ' + ' ' +'[COLOR yellow]'+ season+ '[/COLOR]' + ' ' + '[COLOR green]'+ episode + '[/COLOR]'
                thumb = base_url + thumb
                name = name.replace('Online','')
                print url
                if EnableMeta == 'true':
                               addDirB(name,url,6,thumb,'tvshow')
                if EnableMeta == 'false':
                               addDirB(name,url,6,thumb,None)                               
               
                       

        matchpage=re.compile('<div class="prev-page"><strong>Previous <a href="([^"]*)">[^"]*</a></strong>').findall(link)
        for nexturl in matchpage: 
                addDir('Next Page >>',base_url + nexturl, 1,art+'/next.png')


def TVLIST(url):
        for i in string.ascii_uppercase:
                addDir(i,base_url +'tv-streaming/#'+i.upper(),3,art+'/'+i.lower()+'.png')

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
            addDir(title,url,4,'')  
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
                addDir(season,url,5,'')

def Episodes(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','')
        response.close()
		
        match=re.compile('<strong><a href="([^"]*)">([^"]*)</a> &#8211;[%s]([^"]*)</strong></li>'% name).findall(link)
        for url,episode,title in match:
                title='[COLOR blue]'+episode+'[/COLOR]'+ ' - ' +'[COLOR red]'+title+'[/COLOR]'
                addDir(title,url,6,'')        



def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','').replace('YouWa','Youwatch').replace('Putloc','Putlocker').replace('Socksh','Sockshare')
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
    addLink('Play',urlresolver.resolve(url),art+'/play.png')
    
                
                

                
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

###################################################################################

def addDirB(name,url,mode,iconimage,types):
        ok=True
        type = types
        if type != None:
                infoLabels = GRABMETA(name,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img= iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)

        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

######################


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


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
thumb=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        thumb=urllib.unquote_plus(params["thumb"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

base_url='http://www.couchtuner.eu/'



print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        print base_url 
        MAIN()
       
elif mode==1:
        print " "+url
        NEWRELEASE(url)

elif mode==2:
        print " "+url
        TVLIST(url)

elif mode==3:
        print " "+url
        TVLISTB(url)

elif mode==4:
        print " "+url
        Seasons(url)

elif mode==5:
        print " "+url
        Episodes(url)        
       
elif mode==6:
        print " "+url
        VIDEOLINKS(url,name)
        

        
elif mode==50:
        print " "+url
        Resolve()       


        
   

        

xbmcplugin.endOfDirectory(int(sys.argv[1]))
