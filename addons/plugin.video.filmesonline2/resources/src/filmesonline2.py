import urllib,urllib2,re,cookielib, urlresolver,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
from t0mm0.common.addon import Addon
from BeautifulSoup import BeautifulSoup
from universal import playbackengine


### FilmesOnline2.com  by Kasik. (2013) ###


addon_id = 'plugin.video.filmesonline2'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.filmesonline2', sys.argv)
art = main.art
    
base_url='http://www.filmesonline2.com/'


def Index(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\xc3\x9a','U').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('\xc3\xb3','o').replace('&#8211;','-').replace('\xc3\xa7\xc3\xa3','c').replace('\xc3\xad','i').replace('\xc2\xaa','').replace('&#8217;',"'")
        match = re.findall('class="capa">        <a href="([^"]*)" class="absolute-capa no-text">[^"]*</a>        <img src="([^"]*)" alt="([^"]*)" />',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait, while Movie list is cached..')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on.[/B]',remaining_display)
        for url,thumb,name in match:
                name=name.replace('\r','').replace('\n','').replace('\xc3\x9a','U').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('\xc3\xb3','o').replace('&#8211;','-').replace('\xc3\xa7\xc3\xa3','c').replace('\xc3\xad','i').replace('\xc2\xaa','').replace('&#8217;',"'")
                main.addInfo(name,url,100,thumb,'','')
                #main.addDownLink(name,url,100,thumb,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on.[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
       
        
        olderentries=re.compile('class="next page-numbers" href="([^"]*)">&raquo;</a>').findall(link)
        for url in olderentries:
                main.addDir('[COLOR blue]Next Page -> [/COLOR]',url,1,art+'/next.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        

def Categories(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('&#8211;','-').replace('\xc3\xa7\xc3\xa3','c').replace('\xc3\xad','i')
        match = re.findall('id="menu-item-[^"]*" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-[^"]*"><a href="([^"]*)">([^>]+)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait, while Category list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Categories Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on.[/B]',remaining_display)
        for url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('&#8211;','-').replace('\xc3\xa7\xc3\xa3','c').replace('\xc3\xad','i')
                main.addDir(name,url,7,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Categorias carregado :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on.[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait

def Series(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('\xc3\xb3','o').replace('&#8211;','-').replace('\xc3\xa7\xc3\xa3','c').replace('\xc3\xad','i').replace('\xc2\xaa','').replace('&#8217;',"'")
        match = re.findall('title="<img class=\'capa-search\' src=\'([^"]*)\'>" alt="([^"]*)\'">.+?<a href="([^"]*)" title="[^"]*">[^"]*</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait, while Series list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Series loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on.[/B]',remaining_display)
        for thumb,name,url in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace("(US)","-").replace(' ','-').replace('-&amp;-','-').replace('&-','-')
                print url
                main.addInfo(name,url,6,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Series Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on.[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait

        olderentries=re.compile('href="([^"]*)">&raquo;</a>').findall(link)
        for url in olderentries:
                main.addDir('[COLOR blue]Next Page -> [/COLOR]',url,3,art+'/next.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'TV')

def Index2(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('&#8211;','-').replace('\xc3\xa7\xc3\xa3','c').replace('\xc3\xad','i')
        match = re.findall('<li><a class="lbp_secondary" title="([^>]+)" href="([^>]+)" target="_blank">([^"]*)</a></li>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Episodes loaded.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on.[/B]',remaining_display)
        for title,url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('&#8211;','-')
                main.addDownLink(title + '   ' + name,url,150,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on.[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('&#8211;','-').replace('\xc3\xa7\xc3\xa3','c').replace('\xc3\xad','i')
        match = re.findall('href="https://docs.google.com/file/([^"]*)" target="_blank">([^"]*)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Episodes loaded.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on.[/B]',remaining_display)
        for url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('&#8211;','-')
                url = 'https://docs.google.com/file/' + url
                main.addDownLink(name,url,150,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on.[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait

def CatDex(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('\xc3\xb3','o').replace('&#8211;','-').replace('\xc3\xa7\xc3\xa3','c').replace('\xc3\xad','i').replace('\xc2\xaa','').replace('&#8217;',"'")
        match = re.findall('title="<img class=\'capa-search\' src=\'([^"]*)\'>" alt="([^"]*)\'">.+?<a href="([^"]*)" title="[^"]*">[^"]*</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait, while Series list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Series loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on.[/B]',remaining_display)
        for thumb,name,url in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace("(US)","-").replace(' ','-').replace('-&amp;-','-').replace('&-','-')
                print url
                main.addDownLink(name,url,100,thumb,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Series Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on.[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        olderentries=re.compile('class="next page-numbers" href="([^"]*)">&raquo;</a>').findall(link)
        for url in olderentries:
                main.addDir('[COLOR blue]Next Page -> [/COLOR]',url,7,art+'/next.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        

def Index3(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('&#8211;','-').replace('\xc3\xa7\xc3\xa3','c').replace('\xc3\xad','i')
        match = re.findall('<li><a class="lbp_secondary" title="([^>]+)" href="([^>]+)" target="_blank">([^"]*)</a></li>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Episodes loaded.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on.[/B]',remaining_display)
        for title,url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xc3\xa9','e').replace('&#8211;','-')
                main.addDownLink(title + '   ' + name,url,100,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on.[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait        
        
      
        
###############################  Search Section  ####################################

def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def Search(url):
        searchUrl = 'http://www.filmesonline2.com/?s=' 
        vq = _get_keyboard( heading="Pesquisa" )
        # if blank or the user cancelled the keyboard, return
        if ( not vq ): return False, 0
        # we need to set the title to our query
        title = urllib.quote_plus(vq)
        searchUrl += title 
        print "Searching URL: " + searchUrl 
        Series(searchUrl)
        
        
        



###############################################################################################################
def unescape(text):
        try:            
            rep = {"&nbsp;": " ",
                   "\n": "",
                   "\t": "",   
                   "%3a": ":",
                   "%3A":":",
                   "%2f":"/",
                   "%2F":"/",
                   "%3f":"?",
                   "%3F":"?",
                   "%26":"&",
                   "%3d":"=",
                   "%3D":"=",
                   "%2C":",",
                   "%2c":","
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
                                
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
                                
        except TypeError:
            pass


        return text


def Play(name,url):
        ok=True
        namelist=[]
        urllist=[]
        infoLabels =main.GETMETAT('','','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        docUrl= re.compile('<iframe src="([^"]*)" width="690" height="450"></iframe></div>').findall(link)
        if docUrl:
            link2=main.OPENURL(docUrl[0])
            match= re.compile('url_encoded_fmt_stream_map\":\"(.+?),\"').findall(link2)
            if match:
                streams_map = str(match)
                stream= re.compile('url=(.+?)&type=.+?&quality=(.+?)[,\"]{1}').findall(streams_map)
                for group1,group2 in stream:#Thanks to the-one for google-doc resolver
                    stream_url = str(group1)
                    stream_url = unescape(stream_url)
                    urllist.append(stream_url)
                    stream_qlty = str(group2.upper())
                    if (stream_qlty == 'HD720'):
                        stream_qlty = 'HD-720p'
                    elif (stream_qlty == 'LARGE'):
                        stream_qlty = 'SD-480p'
                    elif (stream_qlty == 'MEDIUM'):
                        stream_qlty = 'SD-360p'
                    namelist.append(stream_qlty)
                dialog = xbmcgui.Dialog()
                answer =dialog.select("Quality Select", namelist)
                if answer != -1:
                        try:
                                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                                stream_url2 = urllist[int(answer)]
                                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                                # play with bookmark
                                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url2, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                                player.KeepAlive()
                                return ok
                        except Exception, e:
                                if stream_url != False:
                                        main.ErrorReport(e)
                return ok
        xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Not Available,3000)")
        return ok       




def PlayB(name,url):
        ok=True
        namelist=[]
        urllist=[]
        infoLabels =main.GETMETAT('','','','')
        video_type='show'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match= re.compile('url_encoded_fmt_stream_map\":\"(.+?),\"').findall(link)
        if match:
                streams_map = str(match)
                stream= re.compile('url=(.+?)&type=.+?&quality=(.+?)[,\"]{1}').findall(streams_map)
                for group1,group2 in stream:#Thanks to the-one for google-doc resolver
                    stream_url = str(group1)
                    stream_url = unescape(stream_url)
                    urllist.append(stream_url)
                    stream_qlty = str(group2.upper())
                    if (stream_qlty == 'HD720'):
                        stream_qlty = 'HD-720p'
                    elif (stream_qlty == 'LARGE'):
                        stream_qlty = 'SD-480p'
                    elif (stream_qlty == 'MEDIUM'):
                        stream_qlty = 'SD-360p'
                    namelist.append(stream_qlty)
                dialog = xbmcgui.Dialog()
                answer =dialog.select("Quality Select", namelist)
                if answer != -1:
                        try:
                                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                                stream_url2 = urllist[int(answer)]
                                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                                # play with bookmark
                                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url2, addon_id=addon_id, video_type=video_type, title=str(infoLabels
['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, 
watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                                player.KeepAlive()
                                return ok
                        except Exception, e:
                                if stream_url != False:
                                        main.ErrorReport(e)
                return ok
        xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Not Available,3000)")
        return ok       
