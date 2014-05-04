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
        addDir('Categories',m_url+'categories',3,art+'/categories.png')
        #addDir('HD Videos',m_url+'hd',7,art+'/hd.png')
        #addDir('Channels',m_url+'channels',6,art+'/hd.png')
        INDEX(m_url)

def CATEGORIES():
        addDir('Amateur',m_url+'category/amateur',7,m_url+'images/categories/amateur.jpg')
        addDir('Anal',m_url+'category/anal',7,m_url+'images/categories/anal.jpg')
        addDir('Asian',m_url+'category/asian',7,m_url+'images/categories/asian.jpg')
        addDir('BBW',m_url+'category/bbw',7,m_url+'images/categories/bbw.jpg')
        addDir('BDSM',m_url+'category/bdsm',7,m_url+'images/categories/bdsm.jpg')
        addDir('Beach',m_url+'category/beach',7,m_url+'images/categories/beach.jpg')
        addDir('Bi-Sexual',m_url+'category/bi-sexual',7,m_url+'images/categories/bi-sexual.jpg')
        addDir('Big Asses',m_url+'category/bigasses',7,m_url+'images/categories/bigasses.jpg')
        addDir('Big Dick',m_url+'category/bigdick',7,m_url+'images/categories/bigdick.jpg')
        addDir('Big Tits',m_url+'category/bigtits',7,m_url+'images/categories/bigtits.jpg')
        addDir('Black and Ebony',m_url+'category/blackandebony',7,m_url+'images/categories/blackandebony.jpg')
        addDir('Blonde',m_url+'category/blonde',7,m_url+'images/categories/blonde.jpg')
        addDir('Blowjob',m_url+'category/blowjob',7,m_url+'images/categories/blowjob.jpg')
        addDir('Bukkake',m_url+'category/bukkake',7,m_url+'images/categories/bukkake.jpg')
        addDir('Cartoons',m_url+'category/cartoons',7,m_url+'images/categories/cartoons.jpg')
        addDir('Celebrity',m_url+'category/celebrity',7,m_url+'images/categories/celebrity.jpg')
        addDir('College',m_url+'category/college',7,m_url+'images/categories/college.jpg')
        addDir('Cream Pie',m_url+'category/creampie',7,m_url+'images/categories/creampie.jpg')
        addDir('Cum Shot',m_url+'category/cumshot',7,m_url+'images/categories/cumshot.jpg')
        addDir('Double Penetration',m_url+'category/doublepenetration',7,m_url+'images/categories/doublepenetration.jpg')
        addDir('Erotic',m_url+'category/erotic',7,m_url+'images/categories/erotic.jpg')
        addDir('Fetish',m_url+'category/fetish',7,m_url+'images/categories/fetish.jpg')
        addDir('Fisting',m_url+'category/fisting',7,m_url+'images/categories/fisting.jpg')
        addDir('Footjob',m_url+'category/footjob',7,m_url+'images/categories/footjob.jpg')
        addDir('Gangbang',m_url+'category/gangbang',7,m_url+'images/categories/gangbang.jpg')
        addDir('Gay',m_url+'category/gay',7,m_url+'images/categories/gay.jpg')
        addDir('German',m_url+'category/german',7,m_url+'images/categories/german.jpg')
        addDir('Grannies',m_url+'category/grannies',7,m_url+'images/categories/grannies.jpg')
        addDir('Group Sex',m_url+'category/groupsex',7,m_url+'images/categories/groupsex.jpg')
        addDir('Hairy',m_url+'category/hairy',7,m_url+'images/categories/hairy.jpg')
        addDir('Handjob',m_url+'category/handjob',7,m_url+'images/categories/handjob.jpg')
        addDir('Hardcore',m_url+'category/hardcore',7,m_url+'images/categories/hardcore.jpg')
        addDir('Hidden Cams',m_url+'category/hiddencams',7,m_url+'images/categories/hiddencams.jpg')
        addDir('Housewives',m_url+'category/housewives',7,m_url+'images/categories/housewives.jpg')
        addDir('Interracial',m_url+'category/interracial',7,m_url+'images/categories/interracial.jpg')
        addDir('Latina',m_url+'category/latina',7,m_url+'images/categories/latina.jpg')
        addDir('Lesbian',m_url+'category/lesbian',7,m_url+'images/categories/lesbian.jpg')
        addDir('Masturbation',m_url+'category/masturbation',7,m_url+'images/categories/masturbation.jpg')
        addDir('Mature',m_url+'category/mature',7,m_url+'images/categories/mature.jpg')
        addDir('Midget',m_url+'category/midget',7,m_url+'images/content/img02.jpg')
        addDir('Milf',m_url+'category/milf',7,m_url+'images/categories/milf.jpg')
        addDir('Old+Young',m_url+'category/old+young',7,m_url+'images/content/img02.jpg')
        addDir('Outdoor',m_url+'category/outdoor',7,m_url+'images/categories/outdoor.jpg')
        addDir('Point of View',m_url+'category/pointofview',7,m_url+'images/categories/pointofview.jpg')
        addDir('Pulic Nudity',m_url+'category/publicnudity',7,m_url+'images/categories/publicnudity.jpg')
        addDir('Sex Guides',m_url+'category/sexguides',7,m_url+'images/content/img02.jpg')
        addDir('Shemale',m_url+'category/shemale',7,m_url+'images/categories/shemale.jpg')
        addDir('Squirting',m_url+'category/squirting',7,m_url+'images/categories/squirting.jpg')
        addDir('Stockings',m_url+'category/stockings',7,m_url+'images/categories/stockings.jpg')
        addDir('Striptease',m_url+'category/striptease',7,m_url+'images/categories/striptease.jpg')
        addDir('Swingers',m_url+'category/swingers',7,m_url+'images/categories/swingers.jpg')
        addDir('Teen',m_url+'category/teen',7,m_url+'images/categories/teen.jpg')
        addDir('Threesome',m_url+'category/threesomes',7,m_url+'images/categories/threesomes.jpg')
        addDir('Toys',m_url+'category/toys',7,m_url+'images/categories/toys.jpg')
        addDir('Uniform',m_url+'category/uniform',7,m_url+'images/categories/uniform.jpg')
        addDir('Upskirts',m_url+'category/upskirts',7,m_url+'images/categories/upskirts.jpg')
        addDir('Vintage',m_url+'category/vintage',7,m_url+'images/categories/vintage.jpg')
        addDir('Voyeur',m_url+'category/voyeur',7,m_url+'images/categories/voyeur.jpg')
        addDir('Webcams',m_url+'category/webcams',7,m_url+'images/categories/webcams.jpg')
        
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        response.close()
		
        match=re.compile('<a href="([^"]*)"  target="_blank" onclick="[^"]*"><img src="([^"]*)" alt="[^"]*" width="300" height="169"/></a><span class="time">([^"]*)</span></div><div class="bottom"><h2>([^"]*)</h2>').findall(link)
        for url,thumb,time,name in match:
                url = 'http://m.playvid.com' + url
                addDownLink(name+ '[COLOR red]  Duration: [/COLOR]' + time,url,2,thumb)
                       

        matchpage=re.compile('href="([^"]*)"  target="_blank" onclick="[^"]*" >Next</a>').findall(link)
        for url in matchpage: 
                addDir('[COLOR green]Next Page >> [/COLOR]','http://m.playvid.com'+url, 1,art+'/next.png')

def INDEX2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        response.close()
		
        match=re.compile('<a  target="_blank" onclick="[^"]*"  href="([^"]*)"><img src="([^"]*)" width="135" height="76" /><span class="time">([^"]*)</span></a></div><div class="about-movie"><h3 class="video-title">([^"]*)</h3>').findall(link)
        for url,thumb,time,name in match:
                url = 'http://m.playvid.com' + url
                addDownLink(name+ '[COLOR red]  Duration: [/COLOR]' + time,url,2,thumb)
                       

        nextpage=re.compile('<a  target="_blank" onclick=".+?"  href="/category/([^"]*)">.+?href="([^"]*)">Next</a>').findall(link)
        for url,nexturl in nextpage:  
                addDir('[COLOR green]Next Page >> [/COLOR]','http://m.playvid.com' + '/category/' + url +nexturl, 7,art+'/next.png')                



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
		
        match=re.compile('href="([^"]*)"><img src="([^"]*)" width="135" height="76" /><span class="time">([^"]*)</span></a></div><div class="about-movie"><h3 class="video-title">([^"]*)</h3>').findall(link)
        for url,thumb,time,name in match:
                url = 'http://m.playvid.com' + url
                addDownLink(name+ '[COLOR red]  Duration: [/COLOR]' + time,url,2,thumb)
                       

        matchpage=re.compile('href="([^"]*)">Next</a>').findall(link)
        for nexturl in matchpage: 
                addDir('[COLOR green]Next Page >> [/COLOR]','http://m.playvid.com'+nexturl,5,art+'/next.png')              

	
        
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

m_url='http://www.playvid.com/'
search_url='http://m.playvid.com/search?q='
m_url='http://m.playvid.com/'


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        print m_url 
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
