import urllib,urllib2,re,xbmcplugin,xbmcgui
from BeautifulSoup import MinimalSoup as BeautifulSoup


#Hornbunny.com - by Kasik 2013.


def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

def MAIN():
        addDir('SEARCH',search_url,4,'')

        addDir('All','http://pollystreaming.com/videos/all/All/most_recent/all_time/',1,'')
        addDir('Uncategorized','http://pollystreaming.com/videos/1/Uncategorized/most_recent/all_time/',1,'')
        addDir('Anime','http://pollystreaming.com/videos/22/Anime/most_recent/all_time/',1,'')
        addDir('Action & Adventure','http://pollystreaming.com/videos/12/Action-Adventure/most_recent/all_time/',1,'')
        addDir('Biography','http://pollystreaming.com/videos/33/Biography/most_recent/all_time/',1,'')
        addDir('Cartoon','http://pollystreaming.com/videos/24/Cartoon/most_recent/all_time/',1,'')
        addDir('Comedy','http://pollystreaming.com/videos/31/Comedy/most_recent/all_time/',1,'')
        addDir('Crime','http://pollystreaming.com/videos/13/Crime/most_recent/all_time/',1,'')
        addDir('Drama','http://pollystreaming.com/videos/44/Drama/most_recent/all_time/',1,'')
        addDir('Detective','http://pollystreaming.com/videos/14/Detective/most_recent/all_time/',1,'')
        addDir('Documentary','http://pollystreaming.com/videos/46/Documentary/most_recent/all_time/',1,'')
        addDir('Family','http://pollystreaming.com/videos/32/Family/most_recent/all_time/',1,'')					
        addDir('Fantasy','http://pollystreaming.com/videos/34/Fantasy/most_recent/all_time/',1,'')
        addDir('Film noir','http://pollystreaming.com/videos/35/Film-noir/most_recent/all_time/',1,'')
        addDir('Inspirational','http://pollystreaming.com/videos/21/Inspirational/most_recent/all_time/',1,'')
        addDir('Game-Show','http://pollystreaming.com/videos/36/Game-Show/most_recent/all_time/',1,'')
        addDir('History','http://pollystreaming.com/videos/37/History/most_recent/all_time/',1,'')
        addDir('Horror','http://pollystreaming.com/videos/17/Horror/most_recent/all_time/',1,'')
        addDir('Movies','http://pollystreaming.com/videos/45/Movies/most_recent/all_time/',1,'')
        addDir('Musical','http://pollystreaming.com/videos/38/Musical/most_recent/all_time/',1,'')
        addDir('Mystery','http://pollystreaming.com/videos/18/Mystery/most_recent/all_time/',1,'')
        addDir('Reality-TV','http://pollystreaming.com/videos/39/Reality-TV/most_recent/all_time/',1,'')
        addDir('Romance','http://pollystreaming.com/videos/15/Romance/most_recent/all_time/',1,'')
        addDir('Sci-Fi','http://pollystreaming.com/videos/40/Sci-Fi/most_recent/all_time/',1,'')
        addDir('Sport','http://pollystreaming.com/videos/41/Sport/most_recent/all_time/',1,'')
        addDir('Talk-Show','http://pollystreaming.com/videos/42/Talk-Show/most_recent/all_time/',1,'')
        addDir('Thriller','http://pollystreaming.com/videos/23/Thriller/most_recent/all_time/',1,'')
        addDir('War','http://pollystreaming.com/videos/43/War/most_recent/all_time/',1,'')
        addDir('Western','http://pollystreaming.com/videos/20/Western/most_recent/all_time/',1,'')
        

def INDEX(url):
        link=OPEN_URL(url)
        link=link.replace('&#8217;',"'")
        match=re.compile('<a href="([^"]*)"><img src="([^"]*)" title="[^"]*" alt="([^"]*)"  /></a>        <span class="vid_time">([^"]*)</span>').findall(link)
        for url,thumb,name,time in match:
         addDownLink('[COLOR aqua]'+name+ '[/COLOR]' '[COLOR red]  Time: ' + time+'[/COLOR]',url,2,thumb)
                
        matchnext=re.compile('class="selected"><a href="([^"]*)">Recent</a>').findall(link)
        for url in matchnext:
         rematch=re.compile('<a href="./([^"]*)">&#8250;</a>').findall(link)
         print name
         for name in rematch:
                  url = url + name
                  print " FINAL " + url
                  addDir('[COLOR green]Next Page>>[/COLOR]',url,1,'')
             
        
       
def VIDEOLINKS(url,name,thumb):
        link=OPEN_URL(url)
        link=link
        match=re.compile('var normal_video_file = \'(.*?)\';var').findall(link)
        name=BeautifulSoup(urllib.unquote_plus(name), convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
        for url in match:
                listitem = xbmcgui.ListItem(name)
                listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
                listitem.setThumbnailImage(urllib.unquote_plus(thumb))
                print "Now Playing" 
                xbmc.Player().play(url, listitem)
               	
def SEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Enter Search Term" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title 
	print "Searching URL: " + searchUrl 
	INDEX(searchUrl)


                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', 'http://anyporn.com/player/kt_player_3.4.1.jsx')

    response = urllib2.urlopen(req)
    link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    response.close()
    return link


def addDownLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        ok=True
        name=BeautifulSoup(name, convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
thumb=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        thumb=urllib.unquote_plus(params["thumb"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

base_url='http://pollystreaming.com/videos/'

search_url='http://pollystreaming.com/search_result.php?query='



print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        print base_url 
        MAIN()
       
elif mode==1:
        print "" + url
        INDEX(url)
        
elif mode==2:
        print "NOW PLAYING"+url
        VIDEOLINKS(url,name,thumb)

elif mode==3:
        print ""+url 
        CATEGORIES(url)
        
elif mode==4:
        print mode
        SEARCH(url)

elif mode==5:
        print "" + url
        VIEWED()        


xbmcplugin.endOfDirectory(int(sys.argv[1]))
