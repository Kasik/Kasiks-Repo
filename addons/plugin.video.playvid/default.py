import urllib,urllib2,re,xbmcplugin,xbmcgui
from BeautifulSoup import MinimalSoup as BeautifulSoup


#Playvid.com - by Kasik 2014.
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
        addDir('Categories',base_url+'categories',3,art+'/categories.png')
        addDir('HD Videos',base_url+'hd',7,art+'/hd.png')
        #addDir('Channels',base_url+'channels',6,art+'/hd.png')
        INDEX('http://www.playvid.com/index')

def CATEGORIES():
        addDir('Amateur',base_url+'category/amateur',1,base_url+'images/categories/amateur.jpg')
        addDir('Anal',base_url+'category/anal',1,base_url+'images/categories/anal.jpg')
        addDir('Asian',base_url+'category/asian',1,base_url+'images/categories/asian.jpg')
        addDir('BBW',base_url+'category/bbw',1,base_url+'images/categories/bbw.jpg')
        addDir('BDSM',base_url+'category/bdsm',1,base_url+'images/categories/bdsm.jpg')
        addDir('Beach',base_url+'category/beach',1,base_url+'images/categories/beach.jpg')
        addDir('Bi-Sexual',base_url+'category/bi-sexual',1,base_url+'images/categories/bi-sexual.jpg')
        addDir('Big Asses',base_url+'category/bigasses',1,base_url+'images/categories/bigasses.jpg')
        addDir('Big Dick',base_url+'category/bigdick',1,base_url+'images/categories/bigdick.jpg')
        addDir('Big Tits',base_url+'category/bigtits',1,base_url+'images/categories/bigtits.jpg')
        addDir('Black and Ebony',base_url+'category/blackandebony',1,base_url+'images/categories/blackandebony.jpg')
        addDir('Blonde',base_url+'category/blonde',1,base_url+'images/categories/blonde.jpg')
        addDir('Blowjob',base_url+'category/blowjob',1,base_url+'images/categories/blowjob.jpg')
        addDir('Bukkake',base_url+'category/bukkake',1,base_url+'images/categories/bukkake.jpg')
        addDir('Cartoons',base_url+'category/cartoons',1,base_url+'images/categories/cartoons.jpg')
        addDir('Celebrity',base_url+'category/celebrity',1,base_url+'images/categories/celebrity.jpg')
        addDir('College',base_url+'category/college',1,base_url+'images/categories/college.jpg')
        addDir('Cream Pie',base_url+'category/creampie',1,base_url+'images/categories/creampie.jpg')
        addDir('Cum Shot',base_url+'category/cumshot',1,base_url+'images/categories/cumshot.jpg')
        addDir('Double Penetration',base_url+'category/doublepenetration',1,base_url+'images/categories/doublepenetration.jpg')
        addDir('Erotic',base_url+'category/erotic',1,base_url+'images/categories/erotic.jpg')
        addDir('Fetish',base_url+'category/fetish',1,base_url+'images/categories/fetish.jpg')
        addDir('Fisting',base_url+'category/fisting',1,base_url+'images/categories/fisting.jpg')
        addDir('Footjob',base_url+'category/footjob',1,base_url+'images/categories/footjob.jpg')
        addDir('Gangbang',base_url+'category/gangbang',1,base_url+'images/categories/gangbang.jpg')
        addDir('Gay',base_url+'category/gay',1,base_url+'images/categories/gay.jpg')
        addDir('German',base_url+'category/german',1,base_url+'images/categories/german.jpg')
        addDir('Grannies',base_url+'category/grannies',1,base_url+'images/categories/grannies.jpg')
        addDir('Group Sex',base_url+'category/groupsex',1,base_url+'images/categories/groupsex.jpg')
        addDir('Hairy',base_url+'category/hairy',1,base_url+'images/categories/hairy.jpg')
        addDir('Handjob',base_url+'category/handjob',1,base_url+'images/categories/handjob.jpg')
        addDir('Hardcore',base_url+'category/hardcore',1,base_url+'images/categories/hardcore.jpg')
        addDir('Hidden Cams',base_url+'category/hiddencams',1,base_url+'images/categories/hiddencams.jpg')
        addDir('Housewives',base_url+'category/housewives',1,base_url+'images/categories/housewives.jpg')
        addDir('Interracial',base_url+'category/interracial',1,base_url+'images/categories/interracial.jpg')
        addDir('Latina',base_url+'category/latina',1,base_url+'images/categories/latina.jpg')
        addDir('Lesbian',base_url+'category/lesbian',1,base_url+'images/categories/lesbian.jpg')
        addDir('Masturbation',base_url+'category/masturbation',1,base_url+'images/categories/masturbation.jpg')
        addDir('Mature',base_url+'category/mature',1,base_url+'images/categories/mature.jpg')
        addDir('Midget',base_url+'category/midget',1,base_url+'images/content/img02.jpg')
        addDir('Milf',base_url+'category/milf',1,base_url+'images/categories/milf.jpg')
        addDir('Old+Young',base_url+'category/old+young',1,base_url+'images/content/img02.jpg')
        addDir('Outdoor',base_url+'category/outdoor',1,base_url+'images/categories/outdoor.jpg')
        addDir('Point of View',base_url+'category/pointofview',1,base_url+'images/categories/pointofview.jpg')
        addDir('Pulic Nudity',base_url+'category/publicnudity',1,base_url+'images/categories/publicnudity.jpg')
        addDir('Sex Guides',base_url+'category/sexguides',1,base_url+'images/content/img02.jpg')
        addDir('Shemale',base_url+'category/shemale',1,base_url+'images/categories/shemale.jpg')
        addDir('Squirting',base_url+'category/squirting',1,base_url+'images/categories/squirting.jpg')
        addDir('Stockings',base_url+'category/stockings',1,base_url+'images/categories/stockings.jpg')
        addDir('Striptease',base_url+'category/striptease',1,base_url+'images/categories/striptease.jpg')
        addDir('Swingers',base_url+'category/swingers',1,base_url+'images/categories/swingers.jpg')
        addDir('Teen',base_url+'category/teen',1,base_url+'images/categories/teen.jpg')
        addDir('Threesome',base_url+'category/threesomes',1,base_url+'images/categories/threesomes.jpg')
        addDir('Toys',base_url+'category/toys',1,base_url+'images/categories/toys.jpg')
        addDir('Uniform',base_url+'category/uniform',1,base_url+'images/categories/uniform.jpg')
        addDir('Upskirts',base_url+'category/upskirts',1,base_url+'images/categories/upskirts.jpg')
        addDir('Vintage',base_url+'category/vintage',1,base_url+'images/categories/vintage.jpg')
        addDir('Voyeur',base_url+'category/voyeur',1,base_url+'images/categories/voyeur.jpg')
        addDir('Webcams',base_url+'category/webcams',1,base_url+'images/categories/webcams.jpg')
        
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        response.close()
		
        match=re.compile('<img src="([^"]*)" alt="">.+?<a href="([^"]*)" class="btn-play ajax">Play</a>.+?<strong class="title">([^"]*)</strong><div class="item-info"><span class="views">[^"]*</span><span class="duration">([^"]*)</span>').findall(link)
        for thumb,url,name,time in match:
                url = 'http://m.playvid.com' + url
                addDownLink(name+ '[COLOR red]  Duration: [/COLOR]' + time,url,2,thumb)
                       

        matchpage=re.compile('<a href="([^"]*)" class="show-more" data-callback="PvLoadMoreNotifications" style="display:none;">Show more</a>').findall(link)
        for url in matchpage: 
                addDir('[COLOR green]<< Show More >> [/COLOR]',base_url+'recently'+url, 1,art+'/next.png')

def INDEX2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        response.close()
		
        match=re.compile('href="([^"]*)"></a>.+?<img src="([^"]*)" alt="">.+?<strong class="title">([^"]*)</strong>').findall(link)
        for url,thumb,name in match:
                url = 'http://m.playvid.com' + url
                addDownLink(name,url,2,thumb)
                       

        nextpage=re.compile('</div><a href="([^"]*)" class="show-more" data-callback="["^]*" style="display:none;">Show more</a>').findall(link)
        for nexturl in nextpage:  
                addDir('[COLOR green]<< Show More >> [/COLOR]',nexturl, 7,art+'/next.png')                

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
		
        match=re.compile('<img src="([^"]*)" alt=""></div><div class="top-info"><span class="added">[^"]*</span></div><div class="info"><div class="buttons"><a href="([^"]*)" class="btn-play ajax">Play</a><a href="//accounts.playvid.com/playvid/login" class="btn-later">Watch Later</a></div><strong class="title">([^"]*)</strong><div class="item-info"><span class="views">[^"]*</span><span class="duration">([^"]*)</span>').findall(link)
        for thumb,url,name,time in match:
                url = 'http://m.playvid.com' + url
                addDownLink(name + ' Duration: ' + time,url,2,thumb)
                       

        matchpage=re.compile('</div><a href="([^"]*)" class="show-more" data-callback="[^"]*" style="display:none;">Show more</a>').findall(link)
        for nexturl in matchpage: 
                addDir('Show More',nexturl, 5, '')                

	
        
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
        CATEGORIES()
        
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
