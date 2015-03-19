import urllib,urllib2,re,cookielib, urlresolver,sys,os,string
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import base64
from t0mm0.common.addon import Addon
from BeautifulSoup import BeautifulSoup

### The DareTv by Kasik. (2014) ###

base_url='http://www.thedarehub.com/tv/movies'
addon_id = 'plugin.video.daretv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.daretv', sys.argv)
art = main.art
AZ_DIRECTORIES = (ltr for ltr in string.ascii_uppercase)   


############################################################### MOVIE SECTION  #############################################################################################################################################################
def MoviesIndex(url,name): #################  Movie Index #################
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('<div class="view_img">.+?<a href="([^"]*?)" class="spec-border-ie" title.+?<img class="img-preview spec-border"  src="([^"]*?)" alt="([^"]*?)" style',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addInfo(name,url,80,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        nextpage=re.compile('<a href="([^"]*?)">&raquo;</a></li>             </ul>        </div><div class="clear">').findall(link)
        for url in nextpage:
                main.addDir('[COLOR blue]Next Page -> [/COLOR]',url,1,art+'/next.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')  
        

def MoviesTags(url,name): ################# Movie Genre List #################
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('<li><a href="(http://www.thedarehub.com/tv/movie-tags/.+?)">([^"]*?)</a></li>',link)
        for url,name in match:
                main.addDir(name,url,13,'')

              

def MovieIndex2(url,name): ################# Movie Genre Index #################
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        match = re.findall('<div class="view_img">.+?<a href="([^"]*?)" class="spec-border-ie" title.+?<img class="img-preview spec-border"  src="([^"]*?)" alt="([^"]*?)" style',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-')
                main.addInfo(name,url,80,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        nextpage=re.compile('<a href="([^"]*?)">&raquo;</a></li>             </ul>        </div>        <form method="post"').findall(link)
        for url in nextpage:
                main.addDir('[COLOR blue]Next Page -> [/COLOR]',url,13,art+'/next.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')                 

               
           

def SearchResults(url):
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\xa6','...').replace('&#8211;','-').replace('#038;','').replace('&#039;',"'")
        movies=re.compile('class="page_title">Movie results(.+?)>Close</a>').findall(link)
        match=re.compile('<div class="view_img">.+?<a href="([^"]*?)" class="spec-border-ie" title=.+?<img class="img-preview spec-border show-thumbnail"  src="http://www.thedarehub.com/tv/templates/svarog/timthumb.php[?]src=([^"]*?)&amp;w=130&amp;h=190&amp;zc=1" alt.+?<a class="link" href=".+?" title="([^"]*?)">').findall(movies[0])
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait while Search is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Search Results loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name in match:
                name=name.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-').replace('\xe2\x80\x94','').replace('&-','-').replace('&#039;',"'")
                main.addInfo(name,url,80,thumb,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Search Results loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait    

        nextpage=re.compile("DELETE").findall(link)
        for url in nextpage:
                name = '[COLOR green] Next Page -> [/COLOR]'
                main.addDir(name,url,15,'')

        
###############################  Search Section  ####################################
def SEARCHS(url):
        search_entered =search()
        name=str(search_entered).replace('+','')
        searchUrl = 'http://www.thedarehub.com/tv/index.php?menu=search&query=' + search_entered 
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
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('IFRAME','iframe').replace('SRC','src')
        putlockera=re.compile('<iframe src="http://www.putlocker.com/([^"]*)"', re.DOTALL).findall(link)
        for url in putlockera:
                url = 'http://www.putlocker.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Putlocker[/B][/COLOR]',url,100,'','')
        putlockerb=re.compile('<a href="http://www.putlocker.com/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in putlockerb:
                url = 'http://www.putlocker.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Putlocker[/B][/COLOR]',url,100,'','')

        socksharea=re.compile('<a href="http://www.sockshare.com/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in socksharea:
                url = 'http://www.sockshare.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Sockshare[/B][/COLOR]',url,100,'','')
        sockshareb=re.compile('<iframe src="http://www.sockshare.com/([^"]*)"', re.DOTALL).findall(link)
        for url in sockshareb:
                url = 'http://www.sockshare.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Sockshare[/B][/COLOR]',url,100,'','')

        vidtoa=re.compile('<a href="http://vidto.me/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in vidtoa:
                url = 'http://vidto.me/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vidto[/B][/COLOR]',url,100,'','')
        vidtob=re.compile('<iframe src="http://vidto.me/([^"]*)" ', re.DOTALL).findall(link)
        for url in vidtob:
                url = 'http://vidto.me/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vidto[/B][/COLOR]',url,100,'','')        
                
        allmyvideosa=re.compile('<a href="http://allmyvideos.net/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in allmyvideosa:
                url = 'http://allmyvideos.net/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - All My Videos[/B][/COLOR]',url,100,'','')
        allmyvideosb=re.compile('<iframe src="http://allmyvideos.net/([^"]*)" ', re.DOTALL).findall(link)
        for url in allmyvideosb:
                url = 'http://allmyvideos.net/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - AllMyVideos[/B][/COLOR]',url,100,'','')        
                
        vsharea=re.compile('<a href="http://vshare.eu/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in vsharea:
                url = 'http://vshare.eu/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vshare[/B][/COLOR]',url,100,'','')
        vshareb=re.compile('<a href="http://vshare.eu/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in vshareb:
                url = 'http://vshare.eu/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vshare[/B][/COLOR]',url,100,'','')
                
        vidspota=re.compile('<a href="http://vidspot.net/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in vidspota:
                url = 'http://vidspot.net/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vidspot[/B][/COLOR]',url,100,'','')
        vidspotb=re.compile('<iframe src="http://vidspot.net/([^"]*)" ', re.DOTALL).findall(link)
        for url in vidspotb:
                url = 'http://vidspot.net/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vidspot[/B][/COLOR]',url,100,'','')        
                
        gorillaa=re.compile('<a href="http://gorillavid.in/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in gorillaa:
                url = 'http://gorillavid.in/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Gorillavid[/B][/COLOR]',url,100,'','')
        gorillab=re.compile('<iframe src="http://gorillavid.in/([^"]*)"', re.DOTALL).findall(link)
        for url in gorillab:
                url = 'http://gorillavid.in/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Gorillavid[/B][/COLOR]',url,100,'','')
                
        filenukea=re.compile('<a href="http://filenuke.com/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in filenukea:
                url = 'http://filenuke.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Filenuke[/B][/COLOR]',url,100,'','')
        filenukeb=re.compile('<iframe src="http://filenuke.com/([^"]*)"', re.DOTALL).findall(link)
        for url in filenukeb:
                url = 'http://filenuke.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Filenuke[/B][/COLOR]',url,100,'','')        
                
        ishareda=re.compile('href="http://ishared.eu/video/([^"]*)" target="_blank">Open video</a></li>', re.DOTALL).findall(link)
        for url in ishareda:
                url = 'http://ishared.eu/video/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Ishared[/B][/COLOR]',url,100,'','')
        isharedb=re.compile('<iframe src="http://ishared.eu/embed/([^"]*)" ', re.DOTALL).findall(link)
        for url in isharedb:
                url = 'http://ishared.eu/embed/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Ishared[/B][/COLOR]',url,100,'','')
        isharedc=re.compile('<iframe id="iframe1"  name="iframe1"  src="http://ishared.eu/([^"]*)"', re.DOTALL).findall(link)
        for url in isharedc:
                url = 'http://ishared.eu/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Ishared[/B][/COLOR]',url,100,'','')        
        youwatcha=re.compile('<a href="http://youwatch.org/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in youwatcha:
                url = 'http://youwatch.org/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Youwatch[/B][/COLOR]',url,100,'','')
        youwatchb=re.compile('<a href="http://youwatch.org/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in youwatchb:
                url = 'http://youwatch.org/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Youwatch[/B][/COLOR]',url,100,'','')        
        arkvida=re.compile('<a href="http://arkvid.tv/player/[?]v=([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in arkvida:
                url = 'http://arkvid.tv/player/?v=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Arkvid[/B][/COLOR]',url,100,'','')
        arkvidb=re.compile('<iframe src="http://arkvid.tv/player/[?]v=([^"]*)" ', re.DOTALL).findall(link)
        for url in arkvidb:
                url = 'http://arkvid.tv/player/?v=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Arkvid[/B][/COLOR]',url,100,'','')
        video44a=re.compile('<a href="http://www.video44.net/gogo/[?]file=([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in video44a:
                url = 'http://www.video44.net/gogo/?file=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Video44[/B][/COLOR]',url,100,'','')
        video44b=re.compile('<iframe src="http://www.video44.net/gogo/[?]file=([^"]*)"', re.DOTALL).findall(link)
        for url in video44b:
                url = 'http://www.video44.net/gogo/?file=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Video44[/B][/COLOR]',url,100,'','')        
        mp4uploada=re.compile('<a href="http://www.mp4upload.com/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in mp4uploada:
                url = 'http://www.mp4upload.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Mp4upload[/B][/COLOR]',url,100,'','')
        mp4uploadb=re.compile('<iframe src="http://www.mp4upload.com/([^"]*)" ', re.DOTALL).findall(link)
        for url in mp4uploadb:
                url = 'http://www.mp4upload.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Mp4upload[/B][/COLOR]',url,100,'','')
        auenginea=re.compile('<a href="http://auengine.com/embed.php[?]file=([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in auenginea:
                url = 'http://auengine.com/embed.php?file=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Auengine[/B][/COLOR]',url,100,'','')
        auengineb=re.compile('<iframe src="http://auengine.com/embed.php[?]file=([^"]*)" ', re.DOTALL).findall(link)
        for url in auengineb:
                url = 'http://auengine.com/embed.php?file=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Auengine[/B][/COLOR]',url,100,'','')
        vodlockera=re.compile('<a href="http://vodlocker.com/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in vodlockera:
                url = 'http://vodlocker.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vodlocker[/B][/COLOR]',url,100,'','')
        vodlockerb=re.compile('http://vodlocker.com/embed-([^"]*?)-.+?.html"', re.DOTALL).findall(link)
        for url in vodlockerb:
                url = 'http://vodlocker.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vodlocker[/B][/COLOR]',url,100,'','')         
        vidbulla=re.compile('<a href="http://vidbull.com/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in vidbulla:
                url = 'http://vidbull.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vidbull[/B][/COLOR]',url,100,'','')
        vidbullb=re.compile('<iframe src="http://vidbull.com/([^"]*)" ', re.DOTALL).findall(link)
        for url in vidbullb:
                url = 'http://vidbull.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vidbull[/B][/COLOR]',url,100,'','')
        sharesixa=re.compile('<a href="http://sharesix.com/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in sharesixa:
                url = 'http://sharesix.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Sharesix[/B][/COLOR]',url,100,'','')
        sharesixb=re.compile('<iframe src="http://www.thedarewall.com/thedarewall/embed.php[?]url=http://sharesix.com/([^"]*)"', re.DOTALL).findall(link)
        for url in sharesixb:
                url = 'http://sharesix.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Sharesix[/B][/COLOR]',url,100,'','')
        vka=re.compile('<a href="http://vk.com/video_ext.php[?]oid=([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in vka:
                url = 'http://vk.com/video_ext.php?oid=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - VK[/B][/COLOR]',url,100,'','')
        vkb=re.compile('iframe src="http://vk.com/video_ext.php[?]oid=([^"]*)"', re.DOTALL).findall(link)
        for url in vkb:
                url = 'http://vk.com/video_ext.php?oid=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - VK[/B][/COLOR]',url,100,'','')
        vkc=re.compile('<iframe id="iframe1"  name="iframe1"  src="http://vk.com/video_ext.php[?]oid=([^"]*)"', re.DOTALL).findall(link)
        for url in vkc:
                url = 'http://vk.com/video_ext.php?oid=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - VK[/B][/COLOR]',url,100,'','')        

        nosvideoa=re.compile('<a href="http://nosvideo.com/[?]v=([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in nosvideoa:
                url = 'http://nosvideo.com/?v=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Nosvideo[/B][/COLOR]',url,100,'','')
        nosvideob=re.compile('<iframe src="http://nosvideo.com/embed/([^"]*)"', re.DOTALL).findall(link)
        for url in nosvideob:
                url = 'http://nosvideo.com/embed/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Nosvideo[/B][/COLOR]',url,100,'','')

        novamova=re.compile('<a href="http://novamov.com/video/([^"]*)" target="_blank">Open video</a>', re.DOTALL).findall(link)
        for url in novamova:
                url = 'http://novamov.com/video/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Novamov[/B][/COLOR]',url,100,'','')
        novamovb=re.compile('src="http://embed.novamov.com/embed.php[?]width=620&height=360&v=([^"]*)" scrolling="no">', re.DOTALL).findall(link)
        for url in novamovb:
                url = 'http://embed.novamov.com/embed.php?width=620&height=360&v=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Novamov[/B][/COLOR]',url,100,'','')
        youtube=re.compile('href="https://www.youtube.com/watch[?]v=([^"]*)"', re.DOTALL).findall(link)
        for url in youtube:
                url = 'https://www.youtube.com/watch?v=' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Youtube[/B][/COLOR]',url,100,'','')
        youtubepart2=re.compile('src="//www.youtube.com/embed/([^"]*)" frameborder="0" allowfullscreen></iframe> Part 2 <', re.DOTALL).findall(link)
        for url in youtubepart2:
                url = 'https://www.youtube.com/embed/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Youtube Part 2[/B][/COLOR]',url,100,'','')
        youtubeb=re.compile('src="//www.youtube.com/embed/([^"]*?)"').findall(link)
        for url in youtubeb:
                url = 'https://www.youtube.com/embed/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Youtube[/B][/COLOR]',url,100,'','')
        vshare=re.compile('http://vshare.eu/embed-([^"]*?)-.+?.html', re.DOTALL).findall(link)
        for url in vshare:
                url = 'http://vshare.eu/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vshare[/B][/COLOR]',url,100,'','')
        streamin=re.compile('http://streamin.to/embed-([^"]*?)-.+?.html', re.DOTALL).findall(link)
        for url in streamin:
                url = 'http://streamin.to/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Streamin.to[/B][/COLOR]',url,100,'','')
        thefile=re.compile('http://thefile.me/embed-([^"]*?)-.+?.html', re.DOTALL).findall(link)
        for url in thefile:
                url = 'http://thefile.me/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Thefile[/B][/COLOR]',url,100,'','')
        exashare=re.compile('http://www.exashare.com/embed-([^"]*?)-.+?.html', re.DOTALL).findall(link)
        for url in exashare:
                url = 'http://www.exashare.com/' + url
                main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Exashare[/B][/COLOR]',url,100,'','')
        vidzi=re.compile('http://vidzi.tv/embed-([^"]*?)-.+?.html').findall(link)
        for url in vidzi:
               url='http://vidzi.tv/'+url
               main.addDown2("[COLOR yellow]"+name+"[/COLOR]"+'[COLOR blue][B] - Vidzi[/B][/COLOR]',url,100,'','')
               


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
