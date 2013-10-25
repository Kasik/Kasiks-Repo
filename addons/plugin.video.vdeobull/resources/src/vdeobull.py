import urllib,urllib2,re,cookielib, urlresolver,sys,os,string
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import base64
from t0mm0.common.addon import Addon
from BeautifulSoup import BeautifulSoup

### VideoBull.com  by Kasik. (2013) ###


addon_id = 'plugin.video.vdeobull'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.vdeobull', sys.argv)
art = main.art
AZ_DIRECTORIES = (ltr for ltr in string.ascii_uppercase)   
base_url='http://videobull.com/'

def AtoZ(url,name):
        main.addDir('1',base_url +'tv-shows/#mctm-1',6,art+'/01.png')
        main.addDir('2',base_url +'tv-shows/#mctm-2',6,art+'/02.png')
        main.addDir('3',base_url +'tv-shows/#mctm-3',6,art+'/03.png')
        main.addDir('4',base_url +'tv-shows/#mctm-4',6,art+'/04.png')
        #main.addDir('5',base_url +'tv-shows/#mctm-5',6,art+'/05.png')
        main.addDir('6',base_url +'tv-shows/#mctm-6',6,art+'/06.png')
        main.addDir('7',base_url +'tv-shows/#mctm-7',6,art+'/07.png')
        main.addDir('8',base_url +'tv-shows/#mctm-8',6,art+'/08.png')
        main.addDir('9',base_url +'tv-shows/#mctm-9',6,art+'/09.png')
        for i in string.ascii_uppercase:
                main.addDir(i,base_url +'tv-shows/#mctm-'+i.lower()+'/',6,art+'/'+i.lower()+'.png')



def Index(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
        match = re.findall('<a href="([^"]*)" rel="bookmark" title="[^"]*"><img src="([^"]*)" width="120px" height="178px" alt="([^"]*)" /></a></div>.+?<p class="postmetadata">Updated: ([^"]*)</p>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Tv Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,date in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addInfo(name+'[COLOR green]  Updated: '+date+'[/COLOR]',url,75,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Tv Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
       
        
        pagenext=re.compile('<a href=\'([^>]+)\' class=\'nextpostslink\'>></a>').findall(link)
        for url in pagenext:
                main.addDir('[COLOR blue]Next Page -> [/COLOR]',url,1,art+'/next2.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Tv-Shows')
        

def Popular(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\xa6','...')
        match = re.findall('<option value="([^>]+)">([^"]*)</option>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Popular List is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Popular List loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addDir(name,url,7,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Popular List loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait

def Popular2(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\xa6','...').replace('&#8211;','-').replace('#038;','')
        match = re.findall('<div id="contentarchivetime">([^"]*)>></div><div id="contentarchivetitle"><a href="([^"]*)" title="[^"]*">([^"]*)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Episode List is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for date,url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addDir(name,url,75,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait

           
def ALPHA(url,name):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
        match=re.compile('<li><a title="[%s]([^"]*)" href="([^"]*)">[^"]*</a> <span class="mctagmap_count">[^"]*</span></li>' % name).findall(link)
        for title,url in match:
            title=name+title
            main.addDir(title,url,7,'')  
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def SearchResults(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\xa6','...').replace('&#8211;','-').replace('#038;','').replace('&#039;',"'")
        match = re.findall('<div id="contentarchivetime">([^"]*)>></div><div id="contentarchivetitle"><a href="([^"]*)" title="[^"]*">([^"]*)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait while Search is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Search Results loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for date,url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-').replace('&#039;',"'")
                main.addDir(name,url,75,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Search Results loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait    

        nextpage=re.compile("<a href='([^>]+)' class='nextpostslink'>></a>").findall(link)
        for url in nextpage:
                name = '[COLOR green] Next Page -> [/COLOR]'
                main.addDir(name,url,11,'')

        
###############################  Search Section  ####################################
def SEARCHS(url):
        search_entered =search()
        name=str(search_entered).replace('+','')
        searchUrl = 'http://videobull.com/?s=' + search_entered + '&x=0&y=0' 
	# we need to set the title to our query
        title = urllib.quote_plus('')
        searchUrl += title 
        print "Searching URL: " + searchUrl 
        SearchResults(searchUrl)
        



def search():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search Tv Shows')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20
            if search_entered == None:
                return False          
        return search_entered	
###############################################################################################################
        
       
###############################  Build Video Links  #############################################################################

def VIDEOLINKS(name,url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match=re.compile('''<a id='.+?' href='.*?title=(.+?)' target='_blank' rel='nofollow'>(.+?)</a>''', re.DOTALL).findall(link)
        for url,host in match:    
                main.addDownLink('[COLOR green][B]'+host+'[/B][/COLOR]',url,100,'','')  
                #addDownLink(name,url,mode,iconimage,fan):



def Play(url,name):
        codelink = url
        url = base64.b64decode(codelink)
        hostUrl = url
        infoLabels = main.GETMETAT(name,'','','')
        videoLink = urlresolver.resolve(hostUrl)      
        player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo('video', infoLabels=infoLabels)
        listitem.setThumbnailImage(infoLabels['cover_url'])
        player.play(videoLink,listitem)
        main.addLink('Restart Video '+ name,str(videoLink),'')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))



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
