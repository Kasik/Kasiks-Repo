import urllib,urllib2,re,xbmcplugin,xbmcgui
from BeautifulSoup import MinimalSoup as BeautifulSoup


#Playvid.com - by Kasik 2013.
art = art = xbmc.translatePath('special://home/addons/plugin.video.playvid/art/')

def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

def MAIN():
        addDir('Search',search_url,4,art+'/search.png')
        addDir('Categories',base_url+'categories/',3,art+'/categories.png')
        addDir('HD Videos',base_url,6,art+'/hd.png')
        INDEX(base_url)

def CATEGORIES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        response.close()

        match=re.compile('<img src="([^"]*)" class="pic-shad"></a></div><p><b><a href="([^"]*)">([^"]*)</a>').findall(link)
        for thumb,url,name in match:
                addDir(name,url,7,thumb)

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        response.close()
		
        match=re.compile('class="thumb"><a href="([^"]*)"><img class="rotate-[^"]*" src="([^"]*)" alt="([^"]+)" width="192" height="109" /><span class="time">([^"]*)</span></a>').findall(link)
        for url,thumb,name,time in match:
                addDownLink(name,url,2,thumb)
                       

        matchpage=re.compile('<a href="([^"]*)">Next .+?</a></li>.+?</div>.+?</div>.+?<input type="hidden"').findall(link)
        for url in matchpage: 
                addDir('[COLOR green]Next Page >> [/COLOR]',url, 1,art+'/next.png')

def INDEX2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        response.close()
		
        match=re.compile('class="thumb"><a href="([^"]*)"><img class="rotate-[^"]*" src="([^"]*)" alt="([^"]+)" width="192" height="109" /><span class="time">([^"]*)</span></a>').findall(link)
        for url,thumb,name,time in match:
                addDownLink(name,url,2,thumb)
                       

        nextpage=re.compile('class="button gradient1 active"><a href="[^"]*">[^"]*</a></li><li class="button gradient1"><a href="([^"]*)">[^"]*</a>').findall(link)
        for nexturl in nextpage:  
                addDir('[COLOR green]Next Page >> [/COLOR]',nexturl, 7,art+'/next.png')                

def HD(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        response.close()
		
        match=re.compile('<div class="thumb"><a href="([^"]*)"><img class="rotate-[^"]*" src="([^"]*)" width="120" height="68" alt="" /><span class="hd"></span><span class="time">([^"]*)</span></a></div><div class="thumb-info"><h3 class="h3">([^"]*)</h3>').findall(link)
        for url,thumb,time,name in match:
                addDownLink(name,url,2,thumb)                

def SEARCHRESULTS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        response.close()
		
        match=re.compile('<div class="thumb"><a href="([^"]*)"><img class="rotate-[^"]*" src="([^"]*)" alt="([^"]*)" width="172" height="99" /><span class="time">([^"]*)</span>').findall(link)
        for url,thumb,name,time in match:
                addDownLink(name,url,2,thumb)
                       

        matchpage=re.compile('<a href="http://www.playvid.com/search" class="search btn-more">more<span></span></a>').findall(link)
        for nexturl in matchpage: 
                addDir('More',nexturl, 5, '')                

	
        
def VIDEOLINKS(url,name,thumb):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="([^"]*mp4)" title').findall(link)
        name=BeautifulSoup(urllib.unquote_plus(name), convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
        for url in match:
                listitem = xbmcgui.ListItem(name)
                listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
                listitem.setThumbnailImage(urllib.unquote_plus(thumb))
                print "Now Playing" 
                xbmc.Player().play(url, listitem)
                
               	
def SEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Search PlayVid" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title 
	print "Searching URL: " + searchUrl 
	SEARCHRESULTS(searchUrl)


                
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

base_url='http://www.playvid.com/'
search_url='http://www.playvid.com/search?q='



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
        print ""+url
        SEARCHRESULTS(url)

elif mode==6:
        print ""+url
        HD(url)

elif mode==7:
        print ""+url
        INDEX2(url)            


xbmcplugin.endOfDirectory(int(sys.argv[1]))
