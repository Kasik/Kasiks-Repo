import urllib,urllib2,re,cookielib, urlresolver,sys,os,string
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import base64
from t0mm0.common.addon import Addon
from BeautifulSoup import BeautifulSoup

### The DareTv by Kasik. (2014) ###

base_url='http://www.thedaretube.com/tv'
addon_id = 'plugin.video.daretv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.daretv', sys.argv)
art = main.art
AZ_DIRECTORIES = (ltr for ltr in string.ascii_uppercase)   


############################################################### TV SECTION  #############################################################################################################################################################
def TVIndex(url): #################  TV Index #################
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('src="http://www.thedaretube.com/tv/templates/svarog/timthumb.php[?]src=([^"]*)&amp;w=[^"]*&amp;h=[^"]*&amp;zc=1" alt=" " style="[^"]*"/>            </a>                        </div>                <h5>                                <a class="link" href="([^"]*)" title="([^"]*)">[^"]*</a>                </h5><p class="left">([^"]*)</p>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Latest Episodes Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for thumb,url,name,season in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addInfo(name+ ' ' + season,url,75,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Latest Episodes Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        nextpage=re.compile('><a href="([^"]*)">&raquo;</a></li> </ul></div><div class="clear">').findall(link)
        for url in nextpage:
                main.addDir('[COLOR blue]Next Page -> [/COLOR]',url,1,art+'/next.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Tv-Shows')  
        

def TVTags(url,name): ################# TV A-Z List #################
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('<li><a href="/tv/tvtag/([^"]*)">([^"]*)</a></li>',link)
        for url,name in match:
                url = 'http://www.thedaretube.com/tv/tvtag/' + url
                main.addDir(name,url,3,'')

def TVIndex2(url,name): ################# TV TAG Index #################
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('src="http://www.thedaretube.com/tv/templates/svarog/timthumb.php[?]src=([^"]*)&amp;w=[^"]*&amp;h=[^"]*&amp;zc=1" alt=" "/>            </a>                        </div>                <h5>                                <a class="link" href="([^"]*)" title="([^"]*)">[^"]*</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Tv Episodes Loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for thumb,url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addInfo(name,url,7,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Tv Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        nextpage=re.compile('<li><a href="([^"]*)">&raquo;</a></li> </ul></div><form method="post"').findall(link)
        for url in nextpage:
                main.addDir('[COLOR blue]Next Page -> [/COLOR]',url,3,art+'/next.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Tv-Shows')                 

def TVGenres(url,name): ################# TV Genre List #################
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('<a href="http://www.thedaretube.com/tv/tv-categories/([^"]*)">([^"]*)</a>',link)
        for url,name in match:
                url = 'http://www.thedaretube.com/tv/tv-categories/' + url + '/abc'
                main.addDir(name,url,5,'')

def TVIndex3(url,name): ################# TV Genre Index #################
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('src="http://www.thedaretube.com/tv/templates/svarog/timthumb.php[?]src=([^"]*)&amp;w=[^"]*&amp;h=[^"]*&amp;zc=1" alt=" "/>            </a>                        </div>                <h5>                                <a class="link" href="([^"]*)" title="([^"]*)">[^"]*</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Tv Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for thumb,url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addInfo(name,url,7,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Tv Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        nextpage=re.compile('<a href="([^"]*)">&raquo;</a></li> </ul></div></div><br style="clear:both;" />').findall(link)
        for url in nextpage:
                main.addDir('[COLOR blue]Next Page -> [/COLOR]',url,5,art+'/next.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Tv-Shows')                            

def TvSeasons(url,name): ################# TV Seasons #################
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('><a href=\'([^>]*)\'>Season ([0-9]*)</a>',link)
        for url,name in match:
                name = 'Season ' +name
                main.addDir(name,url,8,'')
                xbmcplugin.setContent(int(sys.argv[1]), 'Tv-Shows')

def Episodes(url,name): ################# TV Episodes #################
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('src="http://www.thedaretube.com/tv/templates/svarog/timthumb.php[?]src=([^"]*)&amp;w=[^"]*&amp;h=[^"]*&amp;zc=1" alt=" " style=.+?<h5 class="left">                <a class="link" href="([^>]*)" title="(.+?)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Tv Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for thumb,url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('">'," ")
                main.addInfo(name,url,75,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Tv Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        xbmcplugin.setContent(int(sys.argv[1]), 'Tv-Shows')

def Premiers(url,name): ################# Premiers #################
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('<a href="([^"]*)" style=".+?background-image: url([^"]*);".+?><h2>([^"]*)</h2>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Tv Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('">'," ")
                thumb = base_url + thumb
                url = 'http://www.thedaretube.com/' + url
                main.addInfo(name,url,7,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Tv Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        xbmcplugin.setContent(int(sys.argv[1]), 'Tv-Shows')        
           

def SearchResults(url):
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\xa6','...').replace('&#8211;','-').replace('#038;','').replace('&#039;',"'")
        match = re.findall('src="http://www.thedaretube.com/tv/templates/svarog/timthumb.php[?]src=([^"]*)&amp;w=[^"]*&amp;h=[^"]*&amp;zc=1" alt=" " />.+?<a class="link" href="([^"]*)" title="([^"]*)">[^"]*</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait while Search is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Search Results loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for thumb,url,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-').replace('&#039;',"'")
                main.addInfo(name,url,7,thumb,'','')
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
                main.addDir(name,url,220,'')

        
###############################  Search Section  ####################################
def SEARCHS(url):
        search_entered =search()
        name=str(search_entered).replace('+','')
        searchUrl = 'http://www.thedaretube.com/tv/index.php?menu=search&query=' + search_entered 
	# we need to set the title to our query
        title = urllib.quote_plus('')
        searchUrl += title 
        print "Searching URL: " + searchUrl 
        SearchResults(searchUrl)
        

def search():
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search')
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
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('IFRAME','iframe').replace('SRC','src').replace('<span>','')
        match=re.compile('"http://www.putlocker.com/file/([^"]*)"', re.DOTALL).findall(link)
        for url in match:
                url = 'http://www.putlocker.com/file/' + url + '#'
                main.addDownLink("[COLOR blue]Putlocker[/COLOR]",url,100,'','')
        matchb=re.compile('"http://www.putlocker.com/embed/([^"]*)"', re.DOTALL).findall(link)
        for url in matchb:
                url = 'http://www.putlocker.com/embed/' + url + '#'
                main.addDownLink("[COLOR blue]Putlocker[/COLOR]",url,100,'','')
        matchc=re.compile('"http://www.gorillavid.in/([^"]*)"', re.DOTALL).findall(link)
        for url in matchc:
                url = 'http://www.gorillavid.in/' + url
                main.addDownLink("[COLOR blue]Gorillavid[/COLOR]",url,100,'','')        
                
        
def Play(url,name):
        codelink = url
        url = url
        name = name
        hostUrl = url
        infoLabels = main.GETMETAT(name,'','','')
        videoLink = urlresolver.resolve(hostUrl)      
        player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo('video', infoLabels=infoLabels)
        listitem.setThumbnailImage(infoLabels['cover_url'])
        player.play(str(videoLink),listitem)
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
