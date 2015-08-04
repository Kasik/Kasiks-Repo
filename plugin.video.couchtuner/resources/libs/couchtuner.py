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
base_url = 'http://www.couchtuner.la/'    


def AtoZ():
    main.addDir('0-9','http://www.couchtuner.la/tv-list/#',8,art+'/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,'http://www.couchtuner.la/tv-list/#'+i.upper(),8,art+'/'+i.lower()+'.png')

def AZLIST(name,url):
    link=main.OPEN_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;',' - ').replace('<strong>','').replace('</strong>','')
    #match=re.compile('<li><a href="([^"]*)" title="[^"]*">[%s]([^"]*)</a>'% name).findall(link)
    match=re.compile('<li><a.+?href="(http://www.couchtuner.la/[^"]*?)">[%s]([^"]*?)</a></li>'% name).findall(link)
    for url,title in match:
        title=name+title
        #url = url.replace('watch-','watch/')+'/'
        main.addInfo(title,url,9,'','','')


def SEASONS(name,url,index=False):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;',' - ').replace('<br />','').replace('&#8217;',"'")
    seasons = re.compile('(?sim)(Season [0-9]+)</strong>.+?<ul>(.*?)(?=<ul|/ul)').findall(link)
    if not re.search('<strong>(\d+)</strong>', link): seasons = reversed(seasons)
    for season,data in seasons:
        episodes = re.compile('<li><strong><a href="([^"]*?)" rel="nofollow">([^"]*?)</a>([^"]*?)</strong></li>',re.DOTALL).findall(data)
        if len(episodes) > 0:
         main.addDir(name+' '+season.strip(),urllib.quote(str(episodes)),10,'','',index=index)
        else:
         episodes = re.compile('<strong><a href="([^"]*?)">([^"]*?)</a>\s*([^"]*?)</strong></li>',re.DOTALL).findall(data)
         main.addDir(name+' '+season.strip(),urllib.quote(str(episodes)),10,'','',index=index)
        
        

def EPISODES(name,url,index=False):
    #name = name.partition('Season')[0].strip()
    episodes = eval(urllib.unquote(url))
    totalLinks = len(episodes)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Episode list is cached.')
    loadedLinks = 0
    remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for url,epname,eptitle in episodes:
        if index == 'True':
            main.addDirTE(epname+eptitle,url,5,'','','','','','')
        else:
            main.addDirTE(epname+eptitle,url,5,'','','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False    
    dialogWait.close()
    del dialogWait



def NewRelease(url):
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;',' - ')
        match=re.compile('class="tvbox">.+?<a href="([^"]*?)" title="Watch([^"]*?)Online" ><span style="background-image: url[(]([^"]*?)[)]" class.+?').findall(link)
        if match:
         dialogWait = xbmcgui.DialogProgress()
         ret = dialogWait.create('Please wait until Show list is cached.')
         totalLinks = len(match)
         loadedLinks = 0
         remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
         dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
         for url,name,thumb in match:
            name=name.replace('&#8211;',' - ').replace('&#8230;','...')     
            thumb='http://www.couchtuner.la'+thumb
            main.addDirTE(name,url,5,thumb,'','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
         dialogWait.close()
         del dialogWait
         pagetwo=re.compile('content="Page 2:').findall(link)
         if len(pagetwo) > 0:
          xurl='http://www.couchtuner.la/page/3/'
          main.addDir('Page 3',xurl,1,'')
         pagethree=re.compile('content="Page 3:').findall(link)
         if len(pagethree) > 0:
          xurl='http://www.couchtuner.la/page/4/'
          main.addDir('Page 4',xurl,1,'')
         pagefour=re.compile('content="Page 4:').findall(link)
         if len(pagefour) > 0:
          xurl='http://www.couchtuner.la/page/5/'
          main.addDir('Page 5',xurl,1,'')  
         else:
          main.addDir('Page 2','http://www.couchtuner.la/page/2/',1,'')         
        else:
         match=re.compile('class="tvbox">.+?<a href="([^"]*?)" title="Watch([^"]*?)Online" ><span style="background-image: url[(]([^"]*?)[)]" class.+?').findall(link)
         dialogWait = xbmcgui.DialogProgress()
         ret = dialogWait.create('Please wait until Show list is cached.')
         totalLinks = len(match)
         loadedLinks = 0
         remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
         dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
         for url,name,thumb in match:
            name=name.replace('&#8211;',' - ').replace('&#8230;','...')     
            thumb='http://www.couchtuner.la'+thumb
            main.addDirTE(name,url,5,thumb,'','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
         dialogWait.close()
         del dialogWait
                
         nextpage=re.compile('<strong>Previous <a href="([^"]*?)">').findall(link)
         for url in nextpage:
          xurl=base_url+url
          main.addDir('Next Page',xurl,1,'')

        
def LINK(name,url):
    link=main.OPEN_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('IFRAME SRC','iframe src')
    match=re.compile('>Watch it here :</span>.+?<a href="([^"]*?)">').findall(link)
    for url in match:
       LINKZ(name,str(url))
       
    matchtwo=re.compile('>Update :</span> If you dont see any Player. Refresh <br />').findall(link)
    if len(matchtwo) > 0:
       LINKZ(name,str(url)) 
        

               
    
def LINKZ(name,url):
    main.addLink("[COLOR orange]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('IFRAME SRC','iframe src')
    match=re.compile('<b>([^"]*?)</b></span><br /><iframe.+?src="([^"]*?)"').findall(link)
    for host,url in match:
        host=host.replace('AllMyV','allmyvideos').replace('VSpot','vidspot').replace('TheVid','thevideo').replace('Vodlo','vodlocker').replace('Vidbul','vidbull').replace('IShar','ishared').replace('allmyvideosid','allmyvideos')
        main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')

       
        

def LINKZB(name,url):
    #main.addLink("[COLOR yellow]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    vodlocker=re.compile('"http://vodlocker.com/embed-([^"]*?)-.+?.html"').findall(link)
    for url in vodlocker:
        url='http://vodlocker.com/'+url    
        host='vodlocker'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')    
    played=re.compile('http://played.to/embed-([^"]*?)-.+?.html').findall(link)
    for url in played:
        url='http://played.to/'+url    
        host='played'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    thevideo=re.compile('"http://www.thevideo.me/embed-([^"]*?)-.+?.html').findall(link)
    for url in thevideo:
        url='http://www.thevideo.me/'+url    
        host='thevideo'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    vidbull=re.compile('http://vidbull.com/embed-zvfcf9rs2kid-540x318.html').findall(link)
    for url in vidbull:
        url='http://vidbull.com/'+url    
        host='vidbull'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    youwatch=re.compile('http://youwatch.org/embed-([^"]*?)-.+?.html').findall(link)
    for url in youwatch:
        url='http://youwatch.org/'+url    
        host='youwatch'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    vidto=re.compile('"http://vidto.me/embed-([^"]*?)-.+?.html"').findall(link)
    for url in vidto:
        url='http://vidto.me/'+url    
        host='vidto'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')     
    vshare=re.compile('http://vshare.eu/embed-([^"]*?)-.+?.html').findall(link)
    for url in vshare:
        url='http://vshare.eu/'+url    
        host='vshare'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')     
    vidspot=re.compile('"http://vidspot.net/embed-([^"]*?).html').findall(link)
    for url in vidspot:
        url='http://vidspot.net/'+url    
        host='vidspot'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    allmyvideos=re.compile('"http://allmyvideos.net/embed-([^"]*?)-.+?.html"').findall(link)
    for url in allmyvideos:
        url='http://allmyvideos.net/'+url    
        host='allmyvideos'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    vkmobile=re.compile('http://videoapi.my.mail.ru/videos/embed/mail/geek.tv/_myvideo/([^"]*?).html').findall(link)
    for url in vkmobile:
        url='http://videoapi.my.mail.ru/videos/embed/mail/geek.tv/_myvideo/'+url    
        host='VK-Mobile'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    fhoot=re.compile('http://filehoot.com/embed-([^"]*?)-.+?.html').findall(link)
    for url in fhoot:
        url='http://filehoot.com/'+url    
        host='filehoot'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')     
    exashare=re.compile('"http://www.exashare.com/embed-([^"]*?)-.+?.html"').findall(link)
    for url in exashare:
        url='http://www.exashare.com/'+url    
        host='exashare'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')     

    


def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))


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
        surl='http://www.couchtuner.la/?s=' + encode 
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<h2><a href="([^"]*?)" rel="bookmark" title="Watch.+?Online">([^"]*?)</a></h2>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url,name in match:
            main.addDirTE(name,url,9,'','','','','','')
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



def Seasons(url):
    link=main.OPEN_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;',' - ')
    match=re.compile('<strong>Season([^"]*?)</strong></span></p><ul><li>').findall(link)
    for season in match:
        print season
        name=season
        main.addDir('Season '+season,url,9,'','','')



