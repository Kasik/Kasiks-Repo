
# 2Movies Chia Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers

try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.twomovies'


try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer




#addon = Addon(addon_id, sys.argv)
addon = main.addon
# Cache  
cache = StorageServer.StorageServer("Two Movies", 0)


mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')

print 'Mode is: ' + mode
print 'Url is: ' + url
print 'Name is: ' + name
print 'Thumb is: ' + thumb
print 'Extension is: ' + ext
print 'File Type is: ' + console
print 'DL Folder is: ' + dlfoldername
print 'Favtype is: ' + favtype
print 'Main Image is: ' + mainimg

# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://rowthreemedia.com/xbmchub/2movies/art/', ''))
grab=metahandlers.MetaData()
net = Net()
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def CHIACATS():

    
     main.addDir('Latest Anime Episodes','http://www.chia-anime.com/','chialatest',artwork+'anime/Anime_latestepisodes.png','','dir')
     main.addDir('Anime by Genres','none','chiagenres',artwork+'anime/Anime_Genre.png','','dir')
     main.addDir('A-Z','none','chiaalph',artwork+'anime/Anime_A-Z.png','','dir')
     main.addDir('Search Anime ','http://www.chia-anime.com/search/','searchanime',artwork +'Icon_Menu_Movies_SearchName.png','','dir')     
     main.AUTO_VIEW('')    


def CHIALATEST(url):
     link = net.http_GET(url).content
     match=re.compile('<h3><a href="(.+?)" rel="bookmark" title="(.+?)">.+?</a></h3></div></center><div><span class="video-episode">.+?</span></div><div class="thumb" style="background: #000 url(.+?) no-repeat').findall(link)
     for url,name,thumb in match:
          thumb = thumb.replace('(','')
          thumb = thumb.replace(')','')
          main.addDir(name,url,'chiavidpage',thumb,'','')
          main.AUTO_VIEW('movies')

def CHIAVIDPAGE(url,name):
     link = net.http_GET(url).content
     matchvid=re.compile('Watch via Mobile</font></a><a id="download" target="_blank" href="(.+?)">.+?MP4 Video format').findall(link)
     for url in matchvid:
          main.addCHIADLDir(name,url,'chialinkpage',thumb,'','','','')
          main.AUTO_VIEW('movies')


def CHIAALPH():
     main.addDir('#','http://www.chia-anime.com/alpha/#','chiaalphmain',artwork+'movieaz/hash.png','','dir')
     main.addDir('A','http://www.chia-anime.com/alpha/A','chiaalphmain',artwork+'movieaz/a.png','','dir')
     main.addDir('B','http://www.chia-anime.com/alpha/B','chiaalphmain',artwork+'movieaz/b.png','','dir')
     main.addDir('C','http://www.chia-anime.com/alpha/C','chiaalphmain',artwork+'movieaz/c.png','','dir')
     main.addDir('D','http://www.chia-anime.com/alpha/D','chiaalphmain',artwork+'movieaz/d.png','','dir')
     main.addDir('E','http://www.chia-anime.com/alpha/E','chiaalphmain',artwork+'movieaz/e.png','','dir')
     main.addDir('F','http://www.chia-anime.com/alpha/F','chiaalphmain',artwork+'movieaz/f.png','','dir')
     main.addDir('G','http://www.chia-anime.com/alpha/G','chiaalphmain',artwork+'movieaz/g.png','','dir')
     main.addDir('H','http://www.chia-anime.com/alpha/H','chiaalphmain',artwork+'movieaz/h.png','','dir')
     main.addDir('I','http://www.chia-anime.com/alpha/I','chiaalphmain',artwork+'movieaz/i.png','','dir')
     main.addDir('J','http://www.chia-anime.com/alpha/J','chiaalphmain',artwork+'movieaz/j.png','','dir')
     main.addDir('K','http://www.chia-anime.com/alpha/K','chiaalphmain',artwork+'movieaz/k.png','','dir')
     main.addDir('L','http://www.chia-anime.com/alpha/L','chiaalphmain',artwork+'movieaz/l.png','','dir')
     main.addDir('M','http://www.chia-anime.com/alpha/M','chiaalphmain',artwork+'movieaz/m.png','','dir')
     main.addDir('N','http://www.chia-anime.com/alpha/N','chiaalphmain',artwork+'movieaz/n.png','','dir')
     main.addDir('O','http://www.chia-anime.com/alpha/O','chiaalphmain',artwork+'movieaz/o.png','','dir')
     main.addDir('P','http://www.chia-anime.com/alpha/P','chiaalphmain',artwork+'movieaz/p.png','','dir')
     main.addDir('Q','http://www.chia-anime.com/alpha/Q','chiaalphmain',artwork+'movieaz/q.png','','dir')
     main.addDir('R','http://www.chia-anime.com/alpha/R','chiaalphmain',artwork+'movieaz/r.png','','dir')
     main.addDir('S','http://www.chia-anime.com/alpha/S','chiaalphmain',artwork+'movieaz/s.png','','dir')
     main.addDir('T','http://www.chia-anime.com/alpha/T','chiaalphmain',artwork+'movieaz/t.png','','dir')
     main.addDir('U','http://www.chia-anime.com/alpha/U','chiaalphmain',artwork+'movieaz/u.png','','dir')
     main.addDir('V','http://www.chia-anime.com/alpha/V','chiaalphmain',artwork+'movieaz/v.png','','dir')
     main.addDir('W','http://www.chia-anime.com/alpha/W','chiaalphmain',artwork+'movieaz/w.png','','dir')
     main.addDir('X','http://www.chia-anime.com/alpha/X','chiaalphmain',artwork+'movieaz/x.png','','dir')
     main.addDir('Y','http://www.chia-anime.com/alpha/Y','chiaalphmain',artwork+'movieaz/y.png','','dir')
     main.addDir('Z','http://www.chia-anime.com/alpha/Z','chiaalphmain',artwork+'movieaz/z.png','','dir')
          
        
     main.AUTO_VIEW('')

def CHIAGENRES(url):
     genreurl = 'http://www.chia-anime.com/?genre='
     main.addDir('Adventure',genreurl + 'adventure','chiagenremain',artwork+'/anime/Anime_Adventure.png','','dir')
     main.addDir('Comedy',genreurl + 'comedy','chiagenremain',artwork+'/anime/Anime_Comedy.png','','dir')
     main.addDir('Drama',genreurl + 'drama','chiagenremain',artwork+'/anime/Anime_Drama.png','','dir')
     main.addDir('Erotica',genreurl + 'erotica','chiagenremain',artwork+'/anime/Anime_Erotica.png','','dir')
     main.addDir('Fantasy',genreurl + 'fantasy','chiagenremain',artwork+'/anime/Anime_Fantasy.png','','dir')
     main.addDir('Horror',genreurl + 'horror','chiagenremain',artwork+'/anime/Anime_horror.png','','dir')
     main.addDir('Mystery',genreurl + 'mystery','chiagenremain',artwork+'/anime/Anime_Mystery.png','','dir')
     main.addDir('Romance',genreurl + 'romance','chiagenremain',artwork+'/anime/Anime_Romance.png','','dir')
     main.addDir('Thriller',genreurl + 'thriller','chiagenremain',artwork+'/anime/Anime_Thriller.png','','dir')
     main.addDir('Ninja',genreurl + 'ninga','chiagenremain',artwork+'/anime/Anime_Ninja.png','','dir')
     main.addDir('Military',genreurl + 'milatary','chiagenremain',artwork+'/anime/Anime_Military.png','','dir')
     main.addDir('Space',genreurl + 'space','chiagenremain',artwork+'/anime/Anime_Space.png','','dir')
     main.addDir('Aliens',genreurl + 'aliens','chiagenremain',artwork+'/anime/Anime_Aliens.png','','dir')
     main.addDir('Music',genreurl + 'music','chiagenremain',artwork+'/anime/Anime_Music.png','','dir')
     main.addDir('Sports',genreurl + 'sports','chiagenremain',artwork+'/anime/Anime_Sports.png','','dir')
     main.addDir('Demons',genreurl + 'demons','chiagenremain',artwork+'/anime/Anime_Demons.png','','dir')
     main.addDir('Girls with Guns',genreurl + 'girls+with+guns','chiagenremain',artwork+'/anime/Anime_Girlswithguns.png','','dir')
     main.addDir('Supernatural',genreurl + 'supernatural','chiagenremain',artwork+'/anime/Anime_Supernatural.png','','dir')
     main.addDir('Police',genreurl + 'police','chiagenremain',artwork+'/anime/Anime_Police.png','','dir')
     main.addDir('Vampires',genreurl + 'vampires','chiagenremain',artwork+'/anime/Anime_Vampires.png','','dir')
     main.addDir('Super Powers',genreurl + 'superpowers','chiagenremain',artwork+'/anime/Anime_Superpowers.png','','dir')
     main.addDir('Assassins',genreurl + 'assassins','chiagenremain',artwork+'/anime/Anime_Assassins.png','','dir')
     main.addDir('Historical',genreurl + 'historical','chiagenremain',artwork+'/anime/Anime_Historical.png','','dir')
     main.addDir('School',genreurl + 'school','chiagenremain',artwork+'/anime/Anime_School.png','','dir')
     main.addDir('Psychological',genreurl + 'psychological','chiagenremain',artwork+'/anime/Anime_Psychological.png','','dir')
     main.addDir('Martial Arts',genreurl + 'martial+arts','chiagenremain',artwork+'/anime/Anime_Martialarts.png','','dir')
         
     main.AUTO_VIEW('')
              
def CHIAGENREMAIN(url):
     link = net.http_GET(url).content
     match=re.compile('overflow:hidden;"> <a href="(.+?)" title="(.+?)"><img width=".+?" height=".+?" src="(.+?)"></a>').findall(link)
     for url,name,thumb in match:
          name = name.replace('View all episode in','')
          main.addDir(name,url,'chiaepisodes',thumb,'','')
          main.AUTO_VIEW('movies')

def CHIASEARCH(url):
     link = net.http_GET(url).content
     match=re.compile('<img style="padding-left:0px;" width="135" height="190" src="(.+?)"></a></div><div class="title"><a href="(.+?)">(.+?)</a></div>').findall(link)
     for thumb,url,name in match:
          #name = name.replace('View all episode in','')
          main.addDir(name,url,'chialinkpage',thumb,'','')
          main.AUTO_VIEW('movies')          

def CHIAALPHMAIN(url):
     link = net.http_GET(url).content
     match=re.compile('<img width=".+?" height=".+?" src="(.+?)"></a></p></div></td><div style="width:.+?; float:.+?;"><td class=".+?" style=".+?; overflow:.+?;"><div style="height:.+?; width:.+?;"><div style=".+?;"><a href="(.+?)" title="(.+?)">').findall(link)
     for thumb,url,name in match:
          name = name.replace('View all episode in','')
          main.addDir(name,url,'chiaepisodes',thumb,'','')
          main.AUTO_VIEW('movies')
               
def CHIAEPISODES(url,name,year,thumb):
     
    dlfoldername = name 
    link = net.http_GET(url).content
    match=re.compile('background: #000 url(.+?) no-repeat.+?;" alt="(.+?)"><a href="(.+?)"').findall(link)             
    for thumb,name,url in match:
         thumb = thumb.replace('(','')
         thumb = thumb.replace(')','')
         mainimg = thumb
         name = name.replace('&#8211','-')
         link = net.http_GET(url).content
         matchvid=re.compile('Watch via Mobile</font></a><a id="download" target="_blank" href="(.+?)">.+?MP4 Video format').findall(link)
         for url in matchvid:
              main.addCHIADLDir(name,url,'chialinkpage',thumb,'',dlfoldername,'',mainimg)
              main.AUTO_VIEW('movies')
          
                      

def CHIALINKPAGE(url,name,thumb):
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb}
     link = net.http_GET(url).content
     matchsource = re.compile('class="bttn green" href="(.+?)">Save mp4 as Link</a>').findall(link)
     for url in matchsource:
          CHIARESOLVE(name,url,thumb)
     
        

                     

#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHCIA(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for TV Shows" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	SEARCHSHOW(searchUrl)

	main.AUTO_VIEW('movies')


def CHIARESOLVE(name,url,iconimage):
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         main.AUTO_VIEW('')


def CHIADLVIDPAGE(url,name):
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,}
     link = net.http_GET(url).content
     matchsource = re.compile('class="bttn green" href="(.+?)">Save mp4 as Link</a>').findall(link)
     for url in matchsource:
                
                CHIARESOLVEDL(name,url,thumb)         

def CHIARESOLVEDL(name,url,thumb):
               if '.mp4' in url:
                    ext = '.mp4'
               elif '.flv' in url:
                    ext = '.flv'
               elif '.avi' in url:
                    ext = '.avi'
               if not ext == '':
          
          
                    console = 'Downloads/Anime/'+ dlfoldername
                    params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername}
               
               

                    xbmc.sleep(1000)
        
                    main.addToQueue(name,url,thumb,ext,console)#.play(url, liz, False)

#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCHANIME(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for Anime" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	CHIASEARCH(searchUrl)

	main.AUTO_VIEW('movies')                    

