import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,xbmcaddon,os
from metahandler import metahandlers
from BeautifulSoup import MinimalSoup as BeautifulSoup
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer
reload(sys)
sys.setdefaultencoding( "UTF-8" )     

addon_id = 'plugin.video.megabox'
addon = Addon(addon_id, sys.argv)     
settings = xbmcaddon.Addon(id=addon_id)
adult_content = settings.getSetting('adult_content')


cache = StorageServer.StorageServer("megabox", 0)

art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.megabox/art/', ''))

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

grab=metahandlers.MetaData()
net = Net()

def MAIN():
        addDir('Movies','none','movies',art + 'movies.png','dir',False)
        addDir('TV Shows','none','tv',art + 'tv.png','dir',False)
        if adult_content == 'true':
                addDir('Adult Movies',base_url + '?xxx','adultIndex',art + 'adult.png','dir',False)  
        
        addDir('Resolver Settings','none','resolverSettings',art + 'settings.png','dir',False)

def MOVIEGENRES():
        addDir('Action',base_url +'?genre=action','index',art + 'movieaction.png','dir',False)
        #addDir('Adult',base_url +'?genre=adult','index',art + 'movieadult.png','dir',False)
        addDir('Animation',base_url +'?genre=animation','index',art + 'movieanimation.png','dir',False)
        addDir('Comedy',base_url +'?genre=comedy','index',art + 'moviecomedy.png','dir',False)
        addDir('Crime',base_url +'?genre=crime','index',art + 'moviecrime.png','dir',False)
        addDir('Documentary',base_url +'?genre=documentary','index',art + 'moviedocu.png','dir',False)
        addDir('Drama',base_url +'?genre=drama','index',art + 'moviedrama.png','dir',False)
        addDir('Family',base_url +'?genre=family','index',art + 'moviefamily.png','dir',False)
        addDir('Horror',base_url +'?genre=horror','index',art + 'moviehorror.png','dir',False)
        addDir('Romance',base_url +'?genre=romance','index',art + 'movieromance.png','dir',False)
        addDir('Sci-Fi',base_url +'?genre=sci-fi','index',art + 'moviescifi.png','dir',False)
        addDir('Thriller',base_url +'?genre=thriller','index',art + 'moviethriller.png','dir',False)

def MOVIESECTION():
        addDir('Search Movies','none','searchmovies',art + 'searchmovies.png','dir',False)
        addDir('Featured',base_url + '?sort=featured','index',art + 'featmovies.png','dir',False)
        addDir('Ratings',base_url + '?sort=ratings','index',art + 'ratings.png','dir',False)
        addDir('Popular',base_url + '?sort=views','index',art + 'popular.png','dir',False)
        addDir('New Releases',base_url + '?sort=release','index',art + 'new.png','dir',False)
        addDir('Latest Added',base_url + '?sort=latest-added','index',art + 'latestmovies.png','dir',False)
        addDir('Coming Soon',base_url + '?sort=coming-soon','index',art + 'comingsoon.png','dir',False)
        addDir('Youtube Movies',base_url + '?sort=youtube-movies','index',art + 'youtube.png','dir',False)
        addDir('2013 Movies',base_url + '?year=2013','index',art + '2013.png','dir',False)
        addDir('2012 Movies',base_url + '?year=2012','index',art + '2012.png','dir',False)
        addDir('Movie Genres',base_url,'moviegenres',art + 'moviesgenres.png','dir',False)  

def INDEX(url):
        types = ''
        sending_url = url
        link = net.http_GET(url).content
        match=re.compile('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div>').findall(link)
        for url,thumb,name in match:
             show=''
             if 'XXX' in url:
                  continue
             else:
                  if re.search('[Ss]\d\d[Ee]\d\d',name) or  re.search('\d[Xx]\d',name):
                       if 'genre=15' in sending_url:
                              types = 'episodes'
                              addDir(name,base_url + url,'gatherlinks',thumb,'episodes',False)
                  else:
                     types = 'movies'
                     addDir(name,base_url + url,'gatherlinks',thumb,'movies',False)

        pages=re.compile('<a href="(.+?)" class="next">Next &#187;</a></div>').findall(link)
        for nexturl in pages:
          addDir('Next Page',base_url + nexturl,'index',art + 'Icon_Next.png','dir',False)
          
        AUTOVIEW(types)



def TVSECTION():
        addDir('Search Tv Shows','none','searchtv',art + 'searchtv.png','dir',False)
        addDir('Featured',base_url+'?sort=featured&tv','shows',art + 'feattv.png','dir',False)
        addDir('Rating',base_url+'?sort=ratings&tv','shows',art + 'tvrating.png','dir',False)
        addDir('Popular',base_url+'?sort=views&tv','shows',art + 'tvpp.png','dir',False)
        addDir('New Releases',base_url+'?sort=release&tv','shows',art + 'tvnew.png','dir',False)
        addDir('Latest Added',base_url+'?sort=latest-added&tv','shows',art + 'tvlatest.png','dir',False)
        addDir('2013 TV Shows',base_url+'?year=2013&tv','shows',art + 'tv2013.png','dir',False)
        addDir('2012 TV Shows',base_url+'?year=2012&tv','shows',art + 'tv2013.png','dir',False)
        addDir('Tv Genres','none','tvgenres',art + 'tvgenres.png','dir',False)

def TVGENRES():
        addDir('Action',base_url +'index.php?genre=action&tv','shows',art + 'tvaction.png','dir',False)
        addDir('Animation',base_url +'index.php?genre=animation&tv','shows',art + 'tvanimation.png','dir',False)
        addDir('Comedy',base_url +'index.php?genre=comedy&tv','shows',art + 'tvcomedy.png','dir',False)
        addDir('Crime',base_url +'index.php?genre=crime&tv','shows',art + 'tvcrime.png','dir',False)
        addDir('Documentary',base_url +'index.php?genre=documentary&tv','shows',art + 'tvdocu.png','dir',False)
        addDir('Drama',base_url +'index.php?genre=drama&tv','shows',art + 'tvdrama.png','dir',False)
        addDir('Family',base_url +'index.php?genre=family&tv','shows',art + 'tvfamily.png','dir',False)
        addDir('Horror',base_url +'index.php?genre=horror&tv','shows',art + 'tvhorror.png','dir',False)
        addDir('Romance',base_url +'index.php?genre=romance&tv','shows',art + 'tvromance.png','dir',False)
        addDir('Sci-Fi',base_url +'index.php?genre=sci-fi&tv','shows',art + 'tvscifi.png','dir',False)
        addDir('Thriller',base_url +'index.php?genre=thriller&tv','shows',art + 'tvthriller.png','dir',False)       

def TV(url):
        types = ''
        sending_url = url
        link = net.http_GET(url).content
        match=re.compile('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div>').findall(link)
        for url,thumb,name in match:
             show=''
             types = 'movies'
             addDir(name,base_url + url,'episodes',thumb,'shows',False)

                  
        pages=re.compile('<a href="(.+?)" class="next">Next &#187;</a></div>').findall(link)
        for nexturl in pages:
          addDir('Next Page',base_url + nexturl,'shows',art + 'Icon_Next.jpg','dir',False)
          
        AUTOVIEW(types)


def SEASONS(url):
        link = net.http_GET(url).content
        match=re.compile('<div class="tv_episode "><a href="[^"]*&season=([^"]*)&episode=[^"]*&tv">[^"]*<span class').findall(link)
        match.sort() # sort list so it shows season one first
        match = f7(match)
        for name in match:
             name = "Season " + name
             addDir(name,url,'episodes','','shows',False)
        

def EPISODES(url):
        link = net.http_GET(url).content  
        match=re.compile('<div class="tv_episode "><a href="([^"]*)&season=([^"]*)&episode=([^"]*)&tv">[^"]*<span class="ep_title">([^"]*)</span>').findall(link)
        for url,season,episode,name in match:
             name = '[COLOR blue]'+"Season" +season+'[/COLOR]'+ ' ' +'[COLOR red]'+ "Episode" +episode+'[/COLOR]'+ '[COLOR yellow]'+ ' '+name+'[/COLOR]'
             url = base_url + url + '&season='+season+'&episode='+episode+'&tv'
             addDir(name,url,'gatherlinks','','shows',False)
             



        

def ADULTINDEX(url):
        link = net.http_GET(url).content
        pages=re.compile('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div>').findall(link)
        if len(pages) > 0:
             if not 'search' in url:
                  if url == base_url + 'index.php?genre=14':
                          next_page = str(pages[10][0])
                          addDir('Next Page',base_url + '/' + next_page,6,art + 'Icon_Next.jpg','dir',False)
                  else:
                          next_page = str(pages[11][0])
                          addDir('Next Page',base_url + '/' + next_page,6,art + 'Icon_Next.jpg','dir',False)
        
        match=re.compile('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div>').findall(link)
        for url,thumb,name in match:
             url = base_url + '/' + url
             addADir(name,url,'videoLinks',base_url + '/' + thumbnail,plot,False)
        AUTOVIEW('movies')

def GATHERLINKS(url):
        link = net.http_GET(url).content
        link = link.replace('\t','').replace('\r','').replace('\n','')
        match=re.compile('href="([^"]*)">Version[^"]*</a>.+?<div class="col3">([^"]*)</div>').findall(link)
        for url,name in match:
             url = base_url + url
             name = '[COLOR orange]'+name+'[/COLOR]'
             addDownLink(name,url,'play','')
        
        
                  

def PLAY(name,host,url):
        if 'epornik' in url:
                link = net.http_GET(url).content
                elink=re.compile('s1.addVariable(.+?);').findall(link)
                dirty = re.sub("[',)(]", '', (elink[5]))
                clean =   dirty[7:-1]
                url = clean
        else:
                link = net.http_GET(url).content 
                match=re.compile('location.href=\'(.+?)\';"').findall(link)
                for url in match:  
                     url = urlresolver.resolve(url)
        meta = 0
        try:
             meta = getMeta(name,types)
        except:
             pass
        
        params = {'name':name, 'url':url, 'mode':mode, 'thumb':thumb, 'types':types, 'host':host}
        if meta == 0:
             addon.add_video_item(params, {'title':name}, img=thumb)
             liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.jpg", thumbnailImage=thumb)
        else:
             addon.add_video_item(params, meta, fanart=meta['backdrop_url'], img=meta['cover_url'])
             liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.jpg", thumbnailImage=meta['cover_url'])
             liz.setInfo('video',infoLabels=meta)
        
        xbmc.sleep(1000)
        
        xbmc.Player ().play(url, liz, False)                    
          

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search Movies')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = re.sub(' ','+', search)
                
                url = base_url + 'index.php?search=' + search + '&movie=&x=0&y=0'
                
                link = net.http_GET(url).content
                match=re.compile('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div>').findall(link)
                if len(match) > 0:
                        INDEX(url)
                else:
                        match=re.compile('<!--\nwindow.location = "(.+?)"\n//-->').findall(link)
                        if len(match) > 0:
                              if 'XXX' in str(match[0]):
                                   return
                                                
                              else:
                                   VIDEOLINKS(base_url + match[0],'')
                        else:
                                return


def SEARCHTV():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search Tv Shows')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = re.sub(' ','+', search)
                
                url = base_url + 'index.php?search=' + search + '&tv=&x=0&y=0'
                
                link = net.http_GET(url).content
                match=re.compile('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div>').findall(link)
                if len(match) > 0:
                        TV(url)
                else:
                        match=re.compile('<!--\nwindow.location = "(.+?)"\n//-->').findall(link)
                        if len(match) > 0:
                              if 'XXX' in str(match[0]):
                                   return
                                                
                              else:
                                   VIDEOLINKS(base_url + match[0],'')
                        else:
                                return

                              

base_url = 'http://megabox.li/'                              
                        
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
year = addon.queries.get('year', '')
season = addon.queries.get('season', '')
episodes = addon.queries.get('episodes', '')
types = addon.queries.get('types', '')
fanart = addon.queries.get('fanart', '')
imdb_id = addon.queries.get('imdb_id', '')
host = addon.queries.get('host', '')

print "Mode is: "+str(mode)
print "URL is: "+str(url)
print "Name is: "+str(name)
print "Name: "+str(name)
print "Thumb is: "+str(thumb)
print "Season is: "+str(season)
print "Season: "+str(season)
print "episodes is: "+str(episodes)
print "Type is: "+str(types)
print "IMDB ID is: "+str(imdb_id)
print "Host: "+str(host)


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def cleanUnicode(string):
    try:
        string = string.replace("'","").replace(unicode(u'\u201c'), '"').replace(unicode(u'\u201d'), '"').replace(unicode(u'\u2019'),'').replace(unicode(u'\u2026'),'...').replace(unicode(u'\u2018'),'').replace(unicode(u'\u2013'),'-')
        return string
    except:
        return string

def addDownLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        ok=True
        name=BeautifulSoup(name, convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok     

def addDir(name,url,mode,thumb,types,fav):
        fanart = ''
        scraped_thumb = thumb
        scraped_name = name
        addon_fanart = art + 'fanart.png'
        meta = None
        try:
             meta = getMeta(name,types)
        except:
             pass

        try:
                meta['title'] = scraped_name
                thumb = meta['cover_url']
                fanart = meta['backdrop_url']
        except:
                name = scraped_name
                
        if thumb == '':
                thumb = scraped_thumb
        if fanart == '':
             fanart = addon_fanart
                     
        params = {'name':name, 'url':url, 'mode':mode, 'thumb':thumb, 'types':types}
        if meta:
                addon.add_directory(params, meta, img=thumb, fanart=fanart)
        else:
                addon.add_directory(params, {'title':name}, img=thumb ,fanart=fanart)

def addADir(name,url,mode,thumb,plot,fav):
     fanart = art + 'fanart.jpg'
     params = {'name':name, 'url':url, 'mode':mode, 'thumb':thumb, 'types':'adult'}
     meta = {'title':name, 'cover_url':thumb, 'plot':plot}
     addon.add_directory(params, meta, img= thumb, fanart=fanart)

def addHost(host,name,url,mode,thumb):
     fanart = art + 'fanart.jpg'
     thumb = art + host +'.jpg'
     params = {'name':name, 'url':url, 'mode':mode, 'thumb':thumb, 'types':types, 'host':host}
     addon.add_directory(params, {'title':host}, img= thumb, fanart=fanart)

def getMeta(name,types):
        meta = 0
        imdb_id = None
        season = None
        episodes = None
        if types=='movies':
                head,sep,tail = name.partition('(')
                name = head
                year = tail.replace(')','')
                meta = grab.get_meta('movie',name,year)
        elif types=='episodes':
                show = None
                show_meta = None
                S00E00 = re.findall('[Ss]\d\d[Ee]\d\d',name)
                SXE = re.findall('\d[Xx]\d',name)
                SXEE = re.findall('\d[Xx]\d\d',name)
                if S00E00:
                        split = re.split('[Ss]\d\d[Ee]\d\d',name)
                        show = str(split[0])

                        S00E00 = str(S00E00)
                        S00E00.strip('[Ss][Ee]')
                        S00E00 = S00E00.replace("u","")

                        episodes = S00E00[-4:]
                        episodes = episodes[:-2]

                        season = S00E00[:5]
                        season = season[-2:]
                        
                if SXE:
                      split = re.split('\d[Xx]\d',name)
                      show = str(split[0])
                      SXE = str(SXE)
                      SXE = SXE.replace("u","")
                      season = SXE[2]
                      episodes = SXE[4]

                if SXEE:
                      split = re.split('\d[Xx]\d\d',name)
                      show = str(split[0])
                      SXEE = str(SXEE)
                      SXEE = SXEE.replace("u","")
                      sesaon = SXEE[2]
                      episodes = SXEE[4] + SXEE[5]
                      
                if 'Once Upon a Time' in show:
                         show = 'Once Upon a Time (2011)'
                if 'Dracula 2013' in show:
                         show = 'Dracula'
                if 'Castle' in show:
                         show = 'Castle (2009)'
                if 'Eastbound and Down' in show:
                         show = 'Eastbound & Down'
                if 'Marvels Agents of' in show:
                     show  = "Marvel's Agents of S.H.I.E.L.D."
                      
                show_meta = grab.get_meta('tvshow',show)
                imdb_id = show_meta['imdb_id']
                
                meta = grab.get_episode_meta(show,imdb_id,int(season),int(episodes))
     
        return(meta)

def resolvable(url):
     status = None
     hmf = urlresolver.HostedMediaFile(url)
     if hmf:
          status = True

     elif 'epornik' in url:
          status = True

     else:
          status = False
          
     return(status)

def AUTOVIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('movies-view'))
                        elif content == 'episodes':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('episodes-view'))      
                        else:
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view'))
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view'))
                        
                        
if mode==None or url==None or len(url)<1:
        print ""
        MAIN()
elif mode=='movies':
        print ""+url
        MOVIESECTION()
elif mode=='tv':
        print ""+url
        TVSECTION()
elif mode=='shows':
        print ""+url
        TV(url)
elif mode=='seasons':
        print ""+url
        SEASONS(url)
elif mode=='episodes':
        print ""+url
        EPISODES(url)
elif mode=='resolverSettings':
        print ""+url
        urlresolver.display_settings()
elif mode=='index':
        print ""+url
        INDEX(url)
elif mode=='index2':
        print ""+url
        Index2(url)        
elif mode=='gatherlinks':
        print ""+url
        GATHERLINKS(url)        
elif mode=='moviegenres':
        print ""+url
        MOVIEGENRES()
elif mode=='tvgenres':
        print ""+url
        TVGENRES()        
elif mode=='play':
        print ""+url
        PLAY(name,host,url)
elif mode=='searchmovies':
        print ""+url
        SEARCH()
elif mode=='searchtv':
        print ""+url
        SEARCHTV()        
elif mode=='adultIndex':
        print ""+url
        ADULTINDEX(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
