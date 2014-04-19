import urllib,urllib2,re,cookielib,urlresolver,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from resources.universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
wh = watchhistory.WatchHistory('plugin.video.movie25')

def LISTTV2(murl):
        #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,7000)")
        if murl=='movintv':
            main.addDir('Search Movie1k','www.movie1k.org',132,art+'/search.png')
            #urllist=main.OPENURL('http://www.movie1k.ws/category/tv-show/')+main.OPENURL('http://www.movie1k.ws/category/tv-show/page/2/')+main.OPENURL('http://www.movie1k.ws/category/tv-show/page/3/')+main.OPENURL('http://www.movie1k.ws/category/tv-show/page/4/')+main.OPENURL('http://www.movie1k.ws/category/tv-show/page/5/')
            urllist=main.batchOPENURL(('http://www.movie1k.ws/category/tv-show/','http://www.movie1k.ws/category/tv-show/page/2/','http://www.movie1k.ws/category/tv-show/page/3/','http://www.movie1k.ws/category/tv-show/page/4/','http://www.movie1k.ws/category/tv-show/page/5/'))
        elif murl=='movin':
            #urllist=main.OPENURL('http://www.movie1k.ws/category/hindi-movies/')+main.OPENURL('http://www.movie1k.ws/category/hindi-movies/page/2/')+main.OPENURL('http://www.movie1k.ws/category/hindi-movies/page/3/')+main.OPENURL('http://www.movie1k.ws/category/hindi-movies/page/4/')+main.OPENURL('http://www.movie1k.ws/category/hindi-movies/page/5/')+main.OPENURL('http://www.movie1k.ws/category/hindi-movies/page/6/')+main.OPENURL('http://www.movie1k.ws/category/hindi-movies/page/7/')
            urllist=main.batchOPENURL(('http://www.movie1k.ws/category/hindi-movies/','http://www.movie1k.ws/category/hindi-movies/page/2/','http://www.movie1k.ws/category/hindi-movies/page/3/','http://www.movie1k.ws/category/hindi-movies/page/4/','http://www.movie1k.ws/category/hindi-movies/page/5/','http://www.movie1k.ws/category/hindi-movies/page/6/','http://www.movie1k.ws/category/hindi-movies/page/7/'))
        elif murl=='movindub':
            #urllist=main.OPENURL('http://www.movie1k.ws/category/hindi-dubbed-movies/')+main.OPENURL('http://www.movie1k.ws/category/hindi-dubbed-movies/page/2/')+main.OPENURL('http://www.movie1k.ws/category/hindi-dubbed-movies/page/3/')+main.OPENURL('http://www.movie1k.ws/category/hindi-dubbed-movies/page/4/')+main.OPENURL('http://www.movie1k.ws/category/hindi-dubbed-movies/page/5/')+main.OPENURL('http://www.movie1k.ws/category/hindi-dubbed-movies/page/6/')+main.OPENURL('http://www.movie1k.ws/category/hindi-dubbed-movies/page/7/')
            urllist=main.batchOPENURL(('http://www.movie1k.ws/category/hindi-dubbed-movies/','http://www.movie1k.ws/category/hindi-dubbed-movies/page/2/','http://www.movie1k.ws/category/hindi-dubbed-movies/page/3/','http://www.movie1k.ws/category/hindi-dubbed-movies/page/4/','http://www.movie1k.ws/category/hindi-dubbed-movies/page/5/','http://www.movie1k.ws/category/hindi-dubbed-movies/page/6/','http://www.movie1k.ws/category/hindi-dubbed-movies/page/7/'))
            murl=murl
        
        if urllist:
                urllist=urllist.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('<a class="entry-thumbnails-link" href="(.+?)"><img width=".+?" height=".+?" src="(.+?)" class=".+?" alt="Watch (.+?) Online:.+?',re.DOTALL).findall(urllist)
                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Show list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Movies/Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
                for url,thumb,name in match:
                        name=name.replace('\xc2\xa0','').replace('" ','').replace(' "','').replace('"','').replace("&#039;","'").replace("&amp;","and").replace("&#8217;","'").replace("amp;","and").replace("#8211;","-")
                        if murl=='movintv':
                                main.addPlayTE(name,url,31,thumb,'','','','','')
                        else:
                                main.addPlayM(name,url,31,thumb,'','','','','')
                
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Movies/Episodes :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                        if (dialogWait.iscanceled()):
                            return False   
        dialogWait.close()
        del dialogWait

        main.GA("TV-INT","Movie1k")


def SearchhistoryMovie1k():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        if not os.path.exists(SeaFile):
            url='M1k'
            SEARCHMovie1k(url)
        else:
            main.addDir('Search','M1k',133,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,133,thumb)
            
            
    


def SEARCHMovie1k(murl):
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        try:
            os.makedirs(seapath)
        except:
            pass
        if murl == 'M1k':
                keyb = xbmc.Keyboard('', 'Search For Shows or Movies')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText()
                        encode=urllib.quote(search)
                        surl='http://www.movie1k.ws/?s='+encode
                        if not os.path.exists(SeaFile) and encode != '':
                            open(SeaFile,'w').write('search="%s",'%encode)
                        else:
                            if encode != '':
                                open(SeaFile,'a').write('search="%s",'%encode)
                        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
                        for seahis in reversed(searchis):
                            continue
                        if len(searchis)>=10:
                            searchis.remove(searchis[0])
                            os.remove(SeaFile)
                            for seahis in searchis:
                                try:
                                    open(SeaFile,'a').write('search="%s",'%seahis)
                                except:
                                    pass
        else:
                encode = murl
                surl='http://www.movie1k.ws/?s='+encode
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<a class="entry-thumbnails-link" href="(.+?)"><img width=".+?" height=".+?" src="(.+?)" class=".+?" alt="Watch (.+?) Online:.+?',re.DOTALL).findall(link)
        for url,thumb,name in match:
                    main.addPlayc(name,url,31,thumb,'','','','','')

        main.GA("Movie1k","Search")

def VIDEOLINKST2(mname,murl,thumb):
        sources = []
        main.GA("Movie1k","Watched")
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Hosts,10000)")
        f = re.findall('(.+?) Season (.+?) Episode ([^<]+)',mname,re.I)
        if f:
            infoLabels =main.GETMETAEpiT(mname,thumb,'')
            video_type='episode'
            season=infoLabels['season']
            episode=infoLabels['episode']
        if len(f)==0:
            infoLabels =main.GETMETAT(mname,'','',thumb)
            video_type='movie'
            season=''
            episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('<td>','<td >')
        ok=True
        match=re.compile('<td >.+?</td><td >([^"]*)</td><td.+?><a.+?href="http://www.movie1k.ag/watch.php[?]idl=(.+?)" target',re.DOTALL).findall(link)

        for  host,url in match:
                print "im in"
                if 'movie1k' in url:
                                matchx=re.compile('movie1k').findall(url)
                                if len(matchx)==0:
                                        hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                                        sources.append(hosted_media)
                                match3=re.compile('movie1k').findall(url)
                                if len(match3)>0:
                                        link2=main.OPENURL(url)
                                        link2=link2.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                                        match4=re.compile('<iframe.+?src="(.+?)"').findall(link2)
                                        if len(match4)==0:
                                                match4=re.compile('<IFRAME SRC="(.+?)"').findall(link2)
                                                if len(match4)==0:
                                                        match4=re.compile("src='(.+?)'").findall(link2)
                                        for url in match4:
                                                matchx=re.compile('movie1k').findall(url)
                                                if len(matchx)==0:
                                                        hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                                                        sources.append(hosted_media)
                else:
                        matchx=re.compile('movie1k').findall(url)
                        if len(matchx)==0:
                                hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                                sources.append(hosted_media)

        match2=re.compile('<td >.+?</td><td >(.+?)</td><td ><a.+?href="http://www.linkembed.net/watch.php[?]idl=(.+?)" target',re.DOTALL).findall(link)

        for  host,url in match2:
                print "im in"
                if 'linkembed' in url:
                                matchxa=re.compile('linkembed').findall(url)
                                if len(matchxa)==0:
                                        hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                                        sources.append(hosted_media)
                                match3a=re.compile('linkembed').findall(url)
                                if len(match3a)>0:
                                        link2=main.OPENURL(url)
                                        link2=link2.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                                        match4a=re.compile('<iframe.+?src="(.+?)"').findall(link2)
                                        if len(match4a)==0:
                                                match4a=re.compile('<IFRAME SRC="(.+?)"').findall(link2)
                                                if len(match4a)==0:
                                                        match4a=re.compile("src='(.+?)'").findall(link2)
                                        for url in match4a:
                                                matchx=re.compile('linkembed').findall(url)
                                                if len(matchxa)==0:
                                                        hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                                                        sources.append(hosted_media)
                else:
                        matchxb=re.compile('linkembed').findall(url)
                        if len(matchxb)==0:
                                hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                                sources.append(hosted_media)
                
        try:
                if (len(sources)==0):
                        xbmc.executebuiltin("XBMC.Notification(Sorry!,Show doesn't have playable links,5000)")
      
                else:
                        source = urlresolver.choose_source(sources)
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                        stream_url = main.resolve_url(source.get_url())
                        if(stream_url == False):
                            return
                                  
                        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                        # play with bookmark
                        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                        #WatchHistory
                        if selfAddon.getSetting("whistory") == "true":
                            wh.add_item(mname+' '+'[COLOR green]Movie1k[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
                        player.KeepAlive()
                        return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok
