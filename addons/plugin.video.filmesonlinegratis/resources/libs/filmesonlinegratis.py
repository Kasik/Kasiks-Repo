#-*- coding: utf-8 -*-
import urllib,re,sys,os,urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import urlresolver
from BeautifulSoup import MinimalSoup as BeautifulSoup
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
net = Net()
reload(sys)
sys.setdefaultencoding( "UTF-8" )

#Filmesonlinegratis.net - by Kasik 2014.

addon_id = 'plugin.video.filmesonlinegratis'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
base_url='http://www.filmesonlinegratis.net'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

######################################################################################################################
######################################################################################################################

def MOVIES(url):
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211; ',' - ')
        match = re.findall('title="([^"]*)">[^"]*</a></h2><divclass="capa"> <ahref="([^"]*)"><imgsrc="http://static.filmesonlinegratis.net/thumb.php[?]src=([^"]*)&amp;w=135&amp;h=185" alt="[^"]*" title="[^"]*" /></a> <spanclass="qualidade">([^"]*)</span>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for name,url,thumb,quality in match:
                #main.addDirb(name+'[COLOR blue]  Quality: '+quality+'[/COLOR]',str(url),8,thumb,'')
                main.addInfo(name+'[COLOR blue]  Quality: '+quality+'[/COLOR]',url,7,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
               
        nextpage=re.compile('href="([^"]*)">\xc2\xbb</a>').findall(link)
        for url in nextpage:
                main.addDir('Next Page >>',base_url+url,1,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()


def TV(url):
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211; ',' - ').replace('#038;','')
        match = re.findall('title="([^"]*)">[^"]*</a></h2><div class="capa"><a href="([^"]*html)"><img src="http://static.filmesonlinegratis.net/thumb.php[?]src=([^"]*)&amp;w=135&amp;h=185" alt="[^"]*" title="[^"]*" /></a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Series list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Series loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for name,url,thumb in match:
                #main.addInfo(name,url,10,thumb,'','')
                main.addDirTE(name,str(url),6,thumb,'','','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Series loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        
        
        nextpage=re.compile('href="([^"]*)">\xc2\xbb</a>').findall(link)
        for url in nextpage:
                main.addDir('[COLOR aqua]'+'Next Page >>'+'[/COLOR]',base_url+url,11,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()
        

def EPISODES(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211; ',' - ')
        match=re.compile('<a href="([^"]*)" rel=nofollow" target="_blank">([^"]*)</a>').findall(link)
        for url,name in match:
                addDir(name,str(url),7,'','')

                

def GRABLINKS(url):
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('<img src=images/star.gif>','')
        vidig = re.findall('src="http://vidig.biz/([^"]*)"',link)
        if len(vidig) > 0:
                name = '[COLOR yellow] Vidig [/COLOR]'
                main.addDown2(name,url,8,'','')
        vidig2 = re.findall('<iframesrc="http://vidig.biz/([^"]*)"',link)
        if len(vidig2) > 0:
                name = '[COLOR yellow] Vidig [/COLOR]'
                main.addDown2(name,url,8,'','')        

        vk = re.findall('title="http://vk.com/([^"]*)" ',link)
        if len(vk) > 0:                
                name = '[COLOR yellow] VK [/COLOR]'
                main.addDown2(name,url,8,'','')
        vk2 = re.findall('<iframedata-src="http://vk.com/([^"]*)"',link)
        if len(vk2) > 0:                
                name = '[COLOR yellow] VK [/COLOR]'
                main.addDown2(name,url,8,'','')        
                
        firedrive = re.findall('title=\'http://www.firedrive.com/([^"]*)\'>',link)
        if len(firedrive) > 0:                
                name = '[COLOR yellow] Firedrive [/COLOR]'
                main.addDown2(name,url,8,'','')
        firedrive2 = re.findall('data-src=\'https://www.firedrive.com/([^"]*)\'>',link)
        if len(firedrive2) > 0:                
                name = '[COLOR yellow] Firedrive [/COLOR]'
                main.addDown2(name,url,8,'','')        

        dropvideo = re.findall('title="http://dropvideo.com/([^"]*) ',link)
        if len(dropvideo) > 0:                
                name = '[COLOR yellow] Dropvideo [/COLOR]'
                main.addDown2(name,url,8,'','')
        dropvideo2 = re.findall('<iframedata-src="http://dropvideo.com/([^"]*)"',link)
        if len(dropvideo2) > 0:                
                name = '[COLOR yellow] Dropvideo [/COLOR]'
                main.addDown2(name,url,8,'','')
                
                xbmcplugin.setContent(int(sys.argv[1]), 'Shows')



def PLAY(name,url):
        sources = []
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,2000)")
        match=re.compile('http://vidig.biz/([^"]*)').findall(link)
        for url in match:
                url=url = 'http://vidig.biz/' + url
                print url
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('http://vk.com/([^"]*)').findall(link)
        for url in match:
                url = 'http://vk.com/' + url
                print url
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('http://www.firedrive.com/([^"]*)\'').findall(link)
        for url in match:
                url = 'http://www.firedrive.com/' + url
                print url
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('http://dropvideo.com/([^"]*)').findall(link)
        for url in match:
                url = 'http://dropvideo.com/' + url
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

       
















                



                


#######################
def addDir(name, url, mode, iconimage, page):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) +\
        "&name=" + urllib.quote_plus(name) + "&page=" + str(page)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=True)
    return ok                

#######################                






        

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def Seasons(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<h2>Season ([^"]*)</h2>').findall(link)
        #match.sort() # sort list so it shows season one first
        #match = f7(match)
        for season in match:
                print 'SeAsOn:'+season
                #main.addDir("Season "+season,url,13,'','')
                main.addDir('[COLOR blue]'+'SEASON '+season+'[/COLOR]',url,13,'',season=season)
        



                

  

                          


   
      
      







def Searchhistory():
    seapath=os.path.join(main.datapath,'Search')
    SeaFile=os.path.join(seapath,'SearchHistoryMB')
    if not os.path.exists(SeaFile):
        SEARCH()
    else:
        main.addDir('Search Movies','###',120,art+'/search.png')
        main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
        for seahis in reversed(searchis):
            url=seahis
            seahis=seahis.replace('%20',' ')
            main.addDir(seahis,url,120,thumb)

def Searchhistorytv():
    seapath=os.path.join(main.datapath,'Search')
    SeaFile=os.path.join(seapath,'SearchHistoryTv')
    if not os.path.exists(SeaFile):
        SEARCHTV()
    else:
        main.addDir('Search Tv Shows','###',135,art+'/search.png')
        main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
        for seahis in reversed(searchis):
            url=seahis
            seahis=seahis.replace('%20',' ')
            main.addDir(seahis,url,135,thumb)            

def SEARCH(url = ''):
        encode = main.updateSearchFile(url,'Movies')
        if not encode: return False   
        surl='http://www.filmesonlinegratis.net/?s=' + encode + '&s-btn=Buscar'
        link=main.OPEN_URL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211; ',' - ')
        match = re.findall('title="([^"]*)">[^"]*</a></h2><divclass="capa"> <ahref="([^"]*)"><imgsrc="http://static.filmesonlinegratis.net/thumb.php[?]src=([^"]*)&amp;w=135&amp;h=185" alt="[^"]*" title="[^"]*" /></a> <spanclass="qualidade">([^"]*)</span>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for name,url,thumb,quality in match:
                #main.addDirb(name+'[COLOR blue]  Quality: '+quality+'[/COLOR]',str(url),8,thumb,'')
                main.addInfo(name+'[COLOR blue]  Quality: '+quality+'[/COLOR]',url,8,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
               
        nextpage=re.compile('href="([^"]*)">\xc2\xbb</a>').findall(link)
        for url in nextpage:
                main.addDir('Next Page >>',base_url+url,1,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()

def SEARCHTV(url = ''):
        encode = main.updateSearchFile(url,'TV')
        if not encode: return False   
        surl=base_url + 'index.php?search=' + encode + '&tv=&x=0&y=0'
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match = re.findall('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div><ul class=\'star-rating\'><li class="current-rating" style="[^"]*"></li></ul><div class="item-genres"><a href="[^"]*">([^"]*)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre in match:
                name=name.replace('-','').replace('&','').replace('acute;','').strip()
                main.addDir(name+'[COLOR blue] Genre: '+genre+'[/COLOR]',base_url+url,12,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False 
        dialogWait.close()
        del dialogWait
        
        nextpage=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
        for url in nextpage:
                main.addDir('Next Page >>',base_url+url,1,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()        


     



def PLAYB(name,url):
        ok=True
        hname=name
        name  = name.split('[COLOR blue]')[0]
        name  = name.split('[COLOR red]')[0]
        infoLabels = main.GETMETAT(name,'','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }

        try:
            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
            stream_url = main.resolve_url(url)

            infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
            # play with bookmark
            from universal import playbackengine
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                from universal import watchhistory
                wh = watchhistory.WatchHistory('plugin.video.filmesonlinegratis')
                wh.add_item(hname+' '+'[COLOR green]Filmesonlinegratis[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
            player.KeepAlive()
            return ok
        except Exception, e:
            if stream_url != False:
                    main.ErrorReport(e)
            return ok

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

     
