
# 2Movies TV SHOW Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers


try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.twomovies'
#addon = Addon(addon_id, sys.argv)
addon = main.addon

try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer






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
cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://rowthreemedia.com/xbmchub/2movies/art/', ''))
grab=metahandlers.MetaData()
net = Net()
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def TVCATS():

    
          main.addDir('TV Shows by Year','none','tvbyyear',artwork +'Icon_Menu_TVShows_ByYear.png','','dir')
          main.addDir('TV Shows by Genre','none','tvgenres',artwork + '/tvshows/tvshowsgenre.png','','dir')
          main.addDir('TV Shows by Rating','http://twomovies.name/browse_tv_shows/all/byRating/all/','tvplayyear',artwork + '/tvshows/tvshowsrating.png','','dir')
          main.addDir('TV Shows by Popularity','http://twomovies.name/browse_tv_shows/all/byViews/all/','tvplayyear',artwork + '/tvshows/tvshowspopularity.png','','dir')
          main.addDir('[COLOR gold]Search TV Shows[/COLOR]','http://twomovies.name/search/?search_query=','searchtv',artwork + 'Icon_Menu_TVShows_Search.png','','dir')
          
          main.AUTO_VIEW('')    


def TVBYYEAR():
        yearurl = 'http://twomovies.name/browse_tv_shows/all/byViews/'
        main.addDir('2013 ',yearurl+'2013','tvplayyear',artwork +'Icon_Menu_TVShows_2013.png','','dir')
        main.addDir('2012 ',yearurl+'2012','tvplayyear',artwork +'Icon_Menu_TVShows_2012.png','','dir')
        main.addDir('2011 ',yearurl+'2011','tvplayyear',artwork +'Icon_Menu_TVShows_2011.png','','dir')
        main.addDir('2010 ',yearurl+'2010','tvplayyear',artwork +'Icon_Menu_TVShows_2010.png','','dir')
        main.addDir('2009 ',yearurl+'2009','tvplayyear',artwork +'Icon_Menu_TVShows_2009.png','','dir')
        main.addDir('2008 ',yearurl+'2008','tvplayyear',artwork +'Icon_Menu_TVShows_2008.png','','dir')
        main.addDir('2007 ',yearurl+'2007','tvplayyear',artwork +'Icon_Menu_TVShows_2007.png','','dir')
        main.addDir('2006 ',yearurl+'2006','tvplayyear',artwork +'Icon_Menu_TVShows_2006.png','','dir')
        main.addDir('2005 ',yearurl+'2005','tvplayyear',artwork +'Icon_Menu_TVShows_2005.png','','dir')
        main.addDir('2004 ',yearurl+'2004','tvplayyear',artwork +'Icon_Menu_TVShows_2004.png','','dir')
        main.addDir('2003 ',yearurl+'2003','tvplayyear',artwork +'Icon_Menu_TVShows_2003.png','','dir')
        main.addDir('2002 ',yearurl+'2002','tvplayyear',artwork +'Icon_Menu_TVShows_2002.png','','dir')
        main.addDir('2001 ',yearurl+'2001','tvplayyear',artwork +'Icon_Menu_TVShows_2001.png','','dir')
        main.addDir('2000 ',yearurl+'2000','tvplayyear',artwork +'Icon_Menu_TVShows_2000.png','','dir')
        
        main.AUTO_VIEW('')


def TVGENRES():
        
        main.addDir('Action','http://twomovies.name/browse_tv_shows/Action/byViews/all/','tvplaygenre',artwork +'/tvshows/action.png','','dir')
        main.addDir('Adventure','http://twomovies.name/browse_tv_shows/Adventure/byViews/all/','tvplaygenre',artwork +'/tvshows/adventure.png','','dir')
        main.addDir('Animation','http://twomovies.name/browse_tv_shows/Animation/byViews/all/','tvplaygenre',artwork +'/tvshows/animation.png','','dir')
        main.addDir('Biography','http://twomovies.name/browse_tv_shows/Biography/byViews/all/','tvplaygenre',artwork +'/tvshows/biography.png','','dir')
        main.addDir('Comedy','http://twomovies.name/browse_tv_shows/Comedy/byViews/all/','tvplaygenre',artwork +'/tvshows/comedy.png','','dir')
        main.addDir('Crime','http://twomovies.name/browse_tv_shows/Crime/byViews/all/','tvplaygenre',artwork +'/tvshows/crime.png','','dir')
        main.addDir('Documentary','http://twomovies.name/browse_tv_shows/Documentary/byViews/all/','tvplaygenre',artwork +'/tvshows/documentary.png','','dir')
        main.addDir('Drama','http://twomovies.name/browse_tv_shows/Drama/byViews/all/','tvplaygenre',artwork +'/tvshows/drama.png','','dir')
        main.addDir('Family','http://twomovies.name/browse_tv_shows/Family/byViews/all/','tvplaygenre',artwork +'/tvshows/family.png','','dir')
        main.addDir('Fantastic','http://twomovies.name/browse_tv_shows/Fantastic/byViews/all/','tvplaygenre',artwork +'/tvshows/fantastic.png','','dir')
        main.addDir('Fantasy','http://twomovies.name/browse_tv_shows/Fantasy/byViews/all/','tvplaygenre',artwork +'/tvshows/fantasy.png','','dir')
        main.addDir('Film-Noir','http://twomovies.name/browse_tv_shows/Film-Noir/byViews/all/','tvplaygenre',artwork +'/tvshows/film-noir.png','','dir')
        main.addDir('History','http://twomovies.name/browse_tv_shows/History/byViews/all/','tvplaygenre',artwork +'/tvshows/history.png','','dir')
        main.addDir('Horror','http://twomovies.name/browse_tv_shows/Horror/byViews/all/','tvplaygenre',artwork +'/tvshows/horror.png','','dir')
        main.addDir('Music','http://twomovies.name/browse_tv_shows/Music/byViews/all/','tvplaygenre',artwork +'/tvshows/music.png','','dir')
        main.addDir('Mystery','http://twomovies.name/browse_tv_shows/Mystery/byViews/all/','tvplaygenre',artwork +'/tvshows/mystery.png','','dir')
        main.addDir('Reality-TV','http://twomovies.name/browse_tv_shows/Reality-TV/byViews/all/','tvplaygenre',artwork +'/tvshows/reality-tv.png','','dir')
        main.addDir('Romance','http://twomovies.name/browse_tv_shows/Romance/byViews/all/','tvplaygenre',artwork +'/tvshows/romance.png','','dir')
        main.addDir('Sci-Fi','http://twomovies.name/browse_tv_shows/Sci-Fi/byViews/all/','tvplaygenre',artwork +'/tvshows/sci-fi.png','','dir')
        main.addDir('Thriller','http://twomovies.name/browse_tv_shows/Thriller/byViews/all/','tvplaygenre',artwork +'/tvshows/thriller.png','','dir')
        main.addDir('Western','http://twomovies.name/browse_tv_shows/Western/byViews/all/','tvplaygenre',artwork +'/tvshows/western.png','','dir')
        
        main.AUTO_VIEW('')

               

        

        
def TVPLAYYEAR (url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://twomovies.name/browse_tv_shows/all/byViews/(.+?)/">\r\n').findall(link)
          if len(matchyear) > 0:
           for year in matchyear:        
                 data = main.GRABTVMETA(name,year)
                 thumb = data['cover_url']
                   
           types = 'tvshow'
           main.addSDir(name+'('+year+')',url,'episodes',thumb,'',types,data)
           nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>').findall(link)
        if len(nmatch) > 0:
        
                    main.addDir('Next Page',(nmatch[0]),'tvplayyear',artwork + '/tvshows/nextpage.png','','dir')
             
                    main.AUTO_VIEW('tvshow')        
def TVPLAYGENRE (url):
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://twomovies.name/browse_tv_shows/all/byViews/(.+?)/">\r\n').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABTVMETA(name,year)
                 thumb = data['cover_url']
                
                   
             types = 'tvshow'
             main.addSDir(name+'('+year+')',url,'episodes',thumb,'',types,data)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>').findall(link)
        if len(nmatch) > 0:
        
                    main.addDir('Next Page',(nmatch[0]),'tvplaygenre',artwork + '/tvshows/nextpage.png','','dir')
             
                    main.AUTO_VIEW('tvshow')



def SEARCHSHOW(url):
             if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
             link = net.http_GET(url).content
             match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
             if len(match) > 0:
              for url,sitethumb,name in match:
               matchyear=re.compile('<div class="filmyar"><a class="filmyar" href="http://twomovies.name/browse_tv_shows/all/byViews/.+?/">(.+?)</a>').findall(link)
               if len(match) > 0:
                    for year in matchyear:        
                         data = main.GRABTVMETA(name,year)
                         thumb = data['cover_url']
                    types = 'tvshow'
                    if 'watch_tv_show' in url:
                              main.addTVDir(name+'('+year+')',url,'episodes',thumb,data,types,'')
                              main.AUTO_VIEW('tvshows')


                                
def EPISODES(url,name,thumb):
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,} 
    dlfoldername = name
    mainimg = thumb
    show = name
    if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)
    link = net.http_GET(url).content
    matchurl=re.compile('<a class="linkname" href="(.+?)">.+? - (.+?)</a>').findall(link)             
    for url,epname in matchurl:
         matchse=re.compile('http://twomovies.name/watch_episode/(.+?)/(.+?)/(.+?)/').findall(url)
         for showname,season, episode in matchse:
              s = 'S' + season
              e = 'E' + episode
              se = s+e
              name = se + ' ' + epname
              favtype = 'episodes'
              main.addEPDir(name,url,thumb,'tvlinkpage',show,dlfoldername,mainimg,season,episode)
             
              main.AUTO_VIEW('tvshow')


def TVLINKPAGE(url,name,thumb,mainimg):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,'mainimg':mainimg}
        inc = 0
        mainimg = mainimg
        showname = name
        if settings.getSetting('tmovies_account') == 'true':  
              net.set_cookies(cookiejar)    
        link = net.http_GET(url).content
        link=link.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        match=re.compile('href="http://twomovies.name/full_movie(.+?)"target="_blank"').findall(link)
        #match=re.compile('href="(.+?)" target=".+?" rel=".+?" onclick=".+?">Full Movie</a>').findall(link)
        for url in match:
          url = 'http://twomovies.name/full_movie'+url         
          '''if inc < 50:
                        link = net.http_GET(url).content
                        urls=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)

                        hmf = urlresolver.HostedMediaFile(urls[0])'''
          if inc < 50:
                  #This gets around the Continue Button
                link = net.http_GET(url).content 
                conmatch=re.compile('/>Please click (.+?):</p>').findall(link)
                #formmatch=re.compile('input class="(.+?)" type="(.+?)" value="(.+?)" name="(.+?)" /').findall(link)
                for button in conmatch:
                        if 'continue button' in conmatch:
                                        conmatch =str(conmatch)
                                        print 'Button SAYS ' +conmatch
                                        url = url
                                        header_dict = {}
                                        header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                                        header_dict['Connection'] = 'keep-alive'
                                        header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
                                        header_dict['Host'] = 'twomovies.name'
                                        header_dict['Referer'] = url
                                        header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
                                        
                                        form_data = {'confirm':'Continue'}
                                        net.set_cookies(cookiejar)
                                        conbutton = net.http_POST(url, form_data=form_data,headers=header_dict)
                                
                  #This gets around the Continue Button
                #link = net.http_GET(url).content  
                matchurl=re.compile('go=(.+?)"').findall(link)
                #print 'MY LINK URL IS '+ urls
                for urls in matchurl:
  ################srting conversion########################
                   urls = str(urls)
                   print 'LINK URL AFTER STRING is' +urls
##################Try to replace urlparts##################
                 
                   urls = urls.replace('&rel=nofollow','')
                  
                  ##########################################      
                  #returns true or false media file resolve  
                   hmf = urlresolver.HostedMediaFile(urls)
                  ##########################################
                   if hmf:
                                host = hmf.get_host()
                                hthumb = main.GETHOSTTHUMB(host)
                                #dlurl = urlresolver.resolve(url)
                                data = main.GRABTVMETA(showname,'')
                                thumb = data['cover_url']
                                favtype = 'tvshows'
                                try:    
                                        main.addTVDLDir(showname,urls,'vidpage',hthumb,data,dlfoldername,favtype,mainimg)
                                        inc +=1
                                except:
                                        continue
                                   
def DLTVVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
        #link = net.http_GET(url).content
        #match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        #for url in match:
         
                
        main.RESOLVETVDL(name,url,thumb)

def TVVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,} 
        #link = net.http_GET(url).content
        #match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        #for url in match:
        url = url
        name =name
                
        main.RESOLVE2(name,url,thumb)

#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHTV(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for TV Shows" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	SEARCHSHOW(searchUrl)

	main.AUTO_VIEW('tvshow')




#NAME METHOD*****************************

