import urllib,urllib2,re,cookielib, urlresolver,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main
import string

#CouchTuner - by Kasik04a 2013.

from t0mm0.common.addon import Addon
from resources.universal import playbackengine, watchhistory
addon_id = 'plugin.video.couchtuner'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.couchtuner', sys.argv)
art = main.art
base_url = 'http://www.couchtuner.me/'    
wh = watchhistory.WatchHistory('plugin.video.couchtuner')

def NewRelease(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&player=2','').replace("",'').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-')
        match=re.compile('<span class="tvbox"><a href="([^<]*)">.+?src="([^<]*)".+?class="tvpost">([^<]*)<br/>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name in match:
            #url = 'http://streamonline.me/' + url
            main.addDirTE(name,url,5,thumb,'','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait

        nextpage=re.compile('<div class="prev-page"><strong>Previous <a href="([^"]*)">[^"]*</a></strong>').findall(link)
        if nextpage:
         xurl=base_url+nextpage[0]
         main.addDir('Next Page',xurl,1,'')

        
def LINK(name,url):
    link=main.OPEN_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('<strong>Watch It Here :</strong> <strong></strong></span><a href="([^"]*)"').findall(link)
    if match:
     for url in match:
       LINKZ(name,url)
    else:
      match2=re.compile('>Watch it here.+?:</span><a href="([^<]*)">').findall(link)
      if match2:
       for url in match2:
        LINKZ(name,url)
      else:
       match3=re.compile('<strong>Watch It Here : </strong></span><a href="([^"]*)"').findall(link)
       for url in match3:
        LINKZ(name,url)
       
        

def LINKZ(name,url):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('<b>([^"]*)</b></span><br /><IFRAME SRC="([^"]*)"').findall(link)
    for host,url in match:
       host=host.replace('AllMyV','AllMyVideos').replace('TheVid','TheVideo').replace('YouWa','YouWatch').replace('Vidbul','Vidbull').replace('Vodlo','Vodlocker').replace('Playe','Played').replace('ExaSh','Exashare').replace('IShar','Ishare').replace('Playedd','Played').replace('VodLR','Vodlocker')
       main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    match2=re.compile('<b>([^"]*)</b></span><br /><iframe width="540" height="330" src="([^"]*)"').findall(link)
    for host,url in match2:
       host=host.replace('AllMyV','AllMyVideos').replace('TheVid','TheVideo').replace('YouWa','YouWatch').replace('Vidbul','Vidbull').replace('Vodlo','Vodlocker').replace('Playe','Played').replace('ExaSh','Exashare').replace('IShar','Ishare').replace('Playedd','Played').replace('VodLR','Vodlocker')
       main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')

    






def PLAY(name,url):
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
        stream_url = urlresolver.resolve(url)

        infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        #if selfAddon.getSetting("whistory") == "true":
        #    from resources.universal import watchhistory
        #    wh = watchhistory.WatchHistory('plugin.video.movie25')
        #    wh.add_item(hname+' '+'[COLOR green]Movie25[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
        player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok


def Searchhistory():
    seapath=os.path.join(main.datapath,'Search')
    SeaFile=os.path.join(seapath,'SearchHistoryTV')
    if not os.path.exists(SeaFile):
        SEARCH()
    else:
        main.addDir('Search Shows','###',120,art+'/search.png')
        main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
        for seahis in reversed(searchis):
            url=seahis
            seahis=seahis.replace('%20',' ')
            main.addDir(seahis,url,120,thumb)

            

def SEARCH(url = ''):
        encode = main.updateSearchFile(url,'TV')
        if not encode: return False   
        surl='http://www.couchtuner.me/?s=' + encode 
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<span class="tvbox"><a href="([^<]*)">.+?src="([^<]*)".+?class="tvpost">([^<]*)<br/>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name in match:
            #url = 'http://streamonline.me/' + url
            main.addDirTE(name,url,5,thumb,'','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait

        nextpage=re.compile('<div class="prev-page"><strong>Previous <a href="([^"]*)">[^"]*</a></strong>').findall(link)
        if nextpage:
         xurl=base_url+nextpage[0]
         main.addDir('Next Page',xurl,120,'')            







