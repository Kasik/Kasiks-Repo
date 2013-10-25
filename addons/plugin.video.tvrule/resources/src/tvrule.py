import urllib,urllib2,re,cookielib, urlresolver,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
from t0mm0.common.addon import Addon
from BeautifulSoup import BeautifulSoup

### TvRule.com  by Kasik. (2013) ###


addon_id = 'plugin.video.tvrule'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.tvrule', sys.argv)
art = main.art
    
base_url='http://www.tvrule.com/'


def Index(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
        match = re.findall('<a href="([^>]+)" rel="bookmark">([^>]+)</a></h2>.+?<a href="[^>]+">([^>]+)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Tv Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,name,date in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addInfo(name+'[COLOR green]  Date: '+date+'[/COLOR]',url,75,'','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Tv Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
       
        
        olderentries=re.compile('<a href="([^>]+)" >&laquo; Older Entries</a>').findall(link)
        for url in olderentries:
                main.addDir('[COLOR blue]Older Entries -> [/COLOR]',url,1,art+'/next2.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        

def Archive(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
        match = re.findall('<li><a href=\'([^>]+)\' title=\'[^>]+\'>([^>]+)</a></li>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Archives is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Archives loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addDir(name,url,1,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Archives loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait

def Shows(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
        match = re.findall('<option class="level-0" value=".+?">(.+?)</option>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Tv Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace("(US)","-").replace(' ','-').replace('-&amp;-','-').replace('&-','-')
                url = 'http://www.tvrule.com/category/' + name + '/'
                print url
                main.addInfo(name,url,1,'','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Tv Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait        
        
###############################  Search Section  ####################################

def Searchhistory():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTVR')
        if not os.path.exists(SeaFile):
            url='tvr'
            Search(url)
        else:
            main.addDir('Search','tvr',4,art+'/search.png')
            main.addDir('Clear History',SeaFile,20,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,4,thumb)

def Search(url):
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTVR')
        try:
            os.makedirs(seapath)
        except:
            pass
        if url == 'tvr':
                keyb = xbmc.Keyboard('', 'Search')
                keyb.doModal()
                if (keyb.isConfirmed()):
                    search = keyb.getText()
                    encode=urllib.quote(search)
                    surl='http://www.tvrule.com/?s='+encode
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
                        return
        else:
                encode = url
                surl='http://www.tvrule.com/?s='+encode
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<a href="([^>]+)" rel="bookmark">([^>]+)</a></h2>.+?<a href="[^>]+">([^>]+)</a>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,name,date in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','')
                main.addInfo(name+'[COLOR green]  Date: '+date+'[/COLOR]',url,75,'','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False 
        dialogWait.close()
        del dialogWait
        
        pagenext = re.findall('<a href="([^>]+)" >&laquo; Older Entries</a>',link)
        for url in pagenext:
                main.addDir('[COLOR blue]Older Entries -> [/COLOR]','http://www.tvrule.com/?s='+encode,9,art+'/next2.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

###############################################################################################################
        
       
###############################  Build Video Links  #############################################################################

def VIDEOLINKS(name,url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        putlocker=re.compile('http://www.putlocker.com/file/([^"]*)</a>').findall(link)                      
        for url in putlocker:
                url = 'http://www.putlocker.com/file/' + url
                main.addDownLink('[COLOR blue]Putlocker[/COLOR]',url,100,art+'/hosts/putlocker.png',art+'/hosts/putlocker.png')
        sockshare=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/hoster/113.png" alt="Sockshare [^"]*" title').findall(link)
        if len(sockshare) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Sockshare[/COLOR]",url,100,art+'/hosts/sockshare.png',art+'/hosts/sockshare.png')
        #movreel=re.compile('').findall(link)
        #if len(movreel) > 0:
         #       main.addDirb("[COLOR blue]Movreel[/COLOR]",url,100,art+'/hosts/movreel.png',art+'/hosts/movreel.png')
        #billionuploads=re.compile('').findall(link)
        #if len(billionuploads) > 0:
         #       main.addDirb("[COLOR blue]BillionUploads[/COLOR]",url,100,art+'/hosts/billionuploads.png',art+'/hosts/billionuploads.png')
        nowvideo=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/hoster/186.png" alt="Nowvideo [^"]*" title').findall(link)
        if len(nowvideo) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Nowvideo[/COLOR]",url,100,art+'/hosts/nowvideo.png',art+'/hosts/nowvideo.png')
        #oeupload=re.compile('').findall(link)
        #if len(oeupload) > 0:
         #       main.addDirb("[COLOR blue]180upload[/COLOR]",url,12,art+'/hosts/180upload.png',art+'/hosts/180upload.png')
        filenuke=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/flashPlayer2.gif" alt="Filenuke [^"]*" title').findall(link)
        if len(filenuke) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Filenuke[/COLOR]",url,100,art+'/hosts/filenuke.png',art+'/hosts/filenuke.png')
        flashx=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/hoster/150.png" alt="Flashx [^"]*" title').findall(link)
        if len(flashx) > 0:
                main.addDirb("[COLOR blue]Flashx[/COLOR]",url,100,art+'/hosts/flashx.png',art+'/hosts/flashx.png')
        novamov=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/flashPlayer2.gif" alt="Novamov [^"]*" title').findall(link)
        if len(novamov) > 0:
                url = base_url + url
                main.addDirb(name+" [COLOR red]"+quality+"[/COLOR]"+"[COLOR blue] : Novamov[/COLOR]",url,100,art+'/hosts/novamov.png',art+'/hosts/novamov.png')
        #gorillavid=re.compile('').findall(link)
        #if len(gorillavid) > 0:
         #       main.addDirb("[COLOR blue]Gorillavid[/COLOR]",url,148,art+'/hosts/gorillavid.png',art+'/hosts/gorillavid.png')
        divxstage=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/divx.gif" alt="Divxstage [^"]*" title').findall(link)
        if len(divxstage) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Divxstage[/COLOR]",url,100,art+'/hosts/divxstage.png',art+'/hosts/divxstage.png')
        movshare=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/flashPlayer2.gif" alt="Movshare [^"]*" title').findall(link)
        if len(movshare) > 0:
                url = base_url + url
                #main.addDirb(name'[COLOR blue]Movshare[/COLOR]',url,100,art+'/hosts/movshare.png',art+'/hosts/movshare.png')
        sharesix=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/flashPlayer2.gif" alt="Sharesix [^"]*" title').findall(link)
        if len(sharesix) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Sharesix[/COLOR]",url,100,art+'/hosts/sharesix.png',art+'/hosts/sharesix.png')
        #movpod=re.compile('').findall(link)
        #if len(movpod) > 0:
         #       url = base_url + url
          #      main.addDirb("[COLOR blue]Movpod[/COLOR]",url,150,art+'/hosts/movpod.png',art+'/hosts/movpod.png')
        #daclips=re.compile('').findall(link)
        #if len(daclips) > 0:
         #       url = base_url + url
          #      main.addDirb("[COLOR blue] : Daclips[/COLOR]",url,151,art+'/hosts/daclips.png',art+'/hosts/daclips.png')
        videoweed=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/flashPlayer2.gif" alt="Videoweed [^"]*" title').findall(link)
        if len(videoweed) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Videoweed[/COLOR]",url,100,art+'/hosts/videoweed.png',art+'/hosts/videoweed.png')
        played=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/flashPlayer2.gif" alt="played.to [^"]*" title').findall(link)
        if len(played) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Played[/COLOR]",url,100,art+'/hosts/played.png',art+'/hosts/played.png')
        movdivx=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/divx.gif" alt="Movdivx [^"]*" title').findall(link)
        if len(movdivx) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]MovDivx[/COLOR]",url,100,art+'/hosts/movdivx.png',art+'/hosts/movdivx.png')
        
        uploadc=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/flashPlayer2.gif" alt="UploadC [^"]*" title').findall(link)
        if len(uploadc) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Uploadc[/COLOR]",url,100,art+'/hosts/uploadc.png',art+'/hosts/uploadc.png')
        xvidstage=re.compile('"><a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/divx.gif" alt="Xvidstage [^"]*" title').findall(link)
        if len(xvidstage) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Xvidstage[/COLOR]",url,100,art+'/hosts/xvidstage.png',art+'/hosts/xvidstage.png')        
        #zooupload=re.compile('').findall(link)
        #if len(zooupload) > 0:
         #       url = base_url + url
          #      main.addDirb("[COLOR blue]Zooupload[/COLOR]",url,19,art+'/hosts/zooupload.png',art+'/hosts/zooupload.png')
        zalaa=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/flashPlayer2.gif" alt="Zalaa [^"]*" title').findall(link)
        if len(zalaa) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Zalaa[/COLOR]",url,100,art+'/hosts/zalaa.png',art+'/hosts/zalaa.png')
        vidxden=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/flashPlayer2.gif" alt="Vidxden [^"]*" title').findall(link)
        if len(vidxden) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Vidxden[/COLOR]",url,100,art+'/hosts/vidxden.png',art+'/hosts/vidxden.png')
        vidbux=re.compile('<a href="([^"]*)">[^"]*<img border=0 style="vertical-align:top;" src="http://img.movie4k.to/img/divx.gif" alt="Vidbux [^"]*" title').findall(link)
        if len(vidbux) > 0:
                url = base_url + url
                main.addDirb("[COLOR blue]Vidbux[/COLOR]",url,100,art+'/hosts/vidbux.png',art+'/hosts/vidbux.png')
        muchshare=re.compile('SRC="http://muchshare.net/embed-([^"]*).html" FRAMEBORDER').findall(link)
        for url in muchshare:
                url = 'http://muchshare.net/' + url
                main.addDownLink('[COLOR blue]MuchShare[/COLOR]',url,100,art+'/hosts/.png',art+'/hosts/.png')
        mooshare=re.compile('src="http://mooshare.biz/iframe/([^"]*)" frameborder').findall(link)
        for url in mooshare:
                url = 'http://mooshare.biz/iframe/' + url
                main.addDownLink('[COLOR blue]MooShare[/COLOR]',url,100,art+'/hosts/.png',art+'/hosts/.png') 
        





def Play(name,url):
        ok=True
        hname=name
        name  = name.split('[COLOR blue]')[0]
        name  = name.split('[COLOR red]')[0]
        infoLabels = main.GETMETAT(name,'','','')
        link=main.OPENURL(url)
        match=re.compile("Javascript:location.?href=.+?\\'(.+?)'").findall(link)
        for url in match:
            print url
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
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            #if selfAddon.getSetting("whistory") == "true":
                #wh.add_item(hname+' '+'[COLOR green]FreeOMovie[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
            #player.KeepAlive()
            return ok
        except Exception, e:
            if stream_url != False:
                    main.ErrorReport(e)
            return ok




def PlayB(name,url):
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
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                wh.add_item(hname+' '+'[COLOR green]Movie25[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
            player.KeepAlive()
            return ok
        except Exception, e:
            if stream_url != False:
                    main.ErrorReport(e)
            return ok
