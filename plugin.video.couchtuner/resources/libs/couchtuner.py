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
base_url = 'http://couchtuner2.to'    


def AtoZ():
    main.addDir('0-9','http://couchtuner2.to/tv/startwith/',8,art+'/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,'http://couchtuner2.to/tv/startwith/'+i.upper(),8,art+'/'+i.lower()+'.png')

def AZLIST(name,url):
    link=main.OPEN_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;',' - ').replace('<strong>','').replace('</strong>','')
    #match=re.compile('<li><a href="([^"]*)" title="[^"]*">[%s]([^"]*)</a>'% name).findall(link)
    match=re.compile('placement=.+?href="([^"]*?)" >\s*<img src="([^"]*?)" alt.+?>\s*<div class="well-sx text-center">[%s]([^"]*?)</div>'% name).findall(link)
    for url,thumb,title in match:
        title=name+title
        #url = url.replace('watch-','watch/')+'/'
        main.addInfo(title,url,9,thumb,'','')


def SEASONS(name,url,index=False):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;',' - ').replace('<br />','').replace('&#8217;',"'").replace(' rel="nofollow"','')
    seasons = re.compile('(?sim)</span>\s*(Season [0-9]+)\s*</a>\s*<a href="([^"]*?)">').findall(link)
    if not re.search('<strong>(\d+)</strong>', link): seasons = reversed(seasons)
    for season,url in seasons:
        main.addDir(name+' - '+season.strip(),url,10,'','',index=index)
                

def EPISODES(name,url,index=False):
    link=main.OPEN_URL(url)
    link=main.unescapes(link)
    match=re.compile('<td><a href="([^"]*?)"><span class=.+?></span>\s*([^"]*?)</a></td>\s*<td class>([^"]*?)</td>\s*<td class="text-center">([^"]*?)</td>').findall(link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Show list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for url,epinfo,epname,date in match:
     main.addDirTE(name+' -'+epinfo+' '+epname+' '+date,url,5,'','','','','','')
     loadedLinks = loadedLinks + 1
     percent = (loadedLinks * 100)/totalLinks
     remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
     dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
     if (dialogWait.iscanceled()):
      return False   
      dialogWait.close()
      del dialogWait

      paginate=re.compile('<a href="(http://couchtuner2.to/page/[^"]*?)">></a></li>').findall(link)
      for xurl in paginate:  
       main.addDir('[COLOR blue]Next Page >'+'[/COLOR]',xurl,1,art+'/next.png','')

    
def NewRelease(url):
        link=main.OPEN_URL(url)
        link=main.unescapes(link)
        match=re.compile('data-placement=.+?title=".+?href="([^"]*?)"><img src="([^"]*?)" alt="([^"]*?)"><div class="well-sx text-center">([^"]*?)<br>([^"]*?)</div></a></div>').findall(link)
        if match:
         dialogWait = xbmcgui.DialogProgress()
         ret = dialogWait.create('Please wait until Show list is cached.')
         totalLinks = len(match)
         loadedLinks = 0
         remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
         dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
         for url,thumb,epname,name,epinfo in match:
            main.addDirTE(name+' -'+epinfo+' '+epname,url,5,thumb,'','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
         dialogWait.close()
         del dialogWait

        paginate=re.compile('<a href="(http://couchtuner2.to/page/[^"]*?)">></a></li>').findall(link)
        for xurl in paginate:  
         main.addDir('[COLOR blue]Next Page >'+'[/COLOR]',xurl,1,art+'/next.png','')

        
def LINK(name,url):
    link=main.OPEN_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('IFRAME SRC','iframe src')
    match=re.findall('<td class="domain" ><a href="([^"]*?)" ><span class="glyphicon glyphicon-play"></span>\s*([^"]*?)</a></td>\s*<td class="text-center"><span class="">([^"]*?)</span></td>',link)
    for url,host,q in match:
      #resolveURL(name,url,host)
      host=host.replace('.me','').replace('.to','').replace('.net','').replace('.sx','').replace('.eu','').replace('.com','')        
      main.addDir(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",str(url),20,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')

def resolveURL(name,url):
    if selfAddon.getSetting("hide-download-instructions") != "true":
     main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    html = main.OPENURL(url)
    html = main.unescapes(html).replace('IFRAME SRC','iframe src')
    match = re.findall('<iframe.+?src="([^"]*?)"',html)
    for url in match:
     main.addDown2(name.strip(),str(url),2,'.png','.png')


def PLAY(name,url):
    ok=True
    url = url    
    try:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        stream_url = urlresolver.resolve(url)

        listitem = xbmcgui.ListItem(name)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Movie'})
        xbmc.Player().play(str(stream_url), listitem)
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok


#################### OLD PLAYER ########################################

def PLAYOLD(name,url):
    ok=True
    hname=name
    name  = name.split('[COLOR blue]')[0]
    name  = name.split('[COLOR red]')[0]
    #url = resolveURL(url)
    url = url
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
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok
########################################################################





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
        surl='http://couchtuner2.to/search?q=' + encode 
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('td class="col-md-1"><img src="([^"]*?)" title=".+?</td>\s*<td class="col-md-11">.+?<h4 class="media-heading" ><a href="([^"]*?)">([^"]*?)</a></h4>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for thumb,url,name in match:
            main.addDirTE(name,url,9,thumb,'','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait

        nextpage=re.compile('<a href="(http://couchtuner2.to/page/[^"]*?)">></a></li>').findall(link)
        if nextpage:
         for xurl in nextpage:
          main.addDir('Next Page',xurl,120,art+'/next.png')            


