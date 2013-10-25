import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net as net
from metahandler import metahandlers
import datetime,time,threading
from BeautifulSoup import BeautifulSoup

### TvRule.com by Kasik. (2013) ###

base_url ='http://www.tvrule.com/'
addon_id = 'plugin.video.tvrule'
selfAddon = xbmcaddon.Addon(id=addon_id)
tvrulepath = selfAddon.getAddonInfo('path')
addon = Addon(addon_id)
grab = metahandlers.MetaData(preparezip = False)
Dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.tvrule', ''))

datapath = addon.get_profile()


VERSION = "0.0.2"
PATH = "TvRule-"            


try:
    log_path = xbmc.translatePath('special://logpath')
    log = os.path.join(log_path, 'xbmc.log')
    logfile = open(log, 'r').read()
    match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
    if match:
        for build, PLATFORM in match:
            print 'XBMC '+build+' Platform '+PLATFORM
    else:
        PLATFORM=''
except:
    PLATFORM=''

sys.path.append( os.path.join( selfAddon.getAddonInfo('path'), 'resources', 'libs' ))
################################################################################ Common Calls ##########################################################################################################

art = xbmc.translatePath('special://home/addons/plugin.video.tvrule/src/art/')

elogo = xbmc.translatePath('special://home/addons/plugin.video.tvrule/src/art/bigx.png')
slogo = xbmc.translatePath('special://home/addons/plugin.video.tvrule/src/art/smallicon.png')

def OPENURL(url, mobile = False, q = False, verbose = True):
    UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    try:
        print "Openurl = " + url
        req = urllib2.Request(url)
        if mobile:
            req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #link = net(UserAgent).http_GET(url).content
        link=link.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','').replace('&#038;','&').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
        link=link.replace('%3A',':').replace('%2F','/')
        if q: q.put(link)
        return link
    except:
        if verbose:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Source Website is Down,3000,"+elogo+")")
        link ='website down'
        if q: q.put(link)
        return link
    
        
def REDIRECT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.geturl()
        return link

def Clearhistory(url):
        os.remove(url)

def unescapes(text):
        try:
            rep = {"%26":"&","&#38;":"&","&amp;":"&","&#044;": ",","&nbsp;": " ","\n": "","\t": "","\r": "","%5B": "[","%5D": "]","%3a": ":","%3A":":","%2f":"/","%2F":"/","%3f":"?","%3F":"?","%3d":"=","%3D":"=","%2C":",","%2c":",","%3C":"<","%20":" ","%22":'"',"%3D":"=","%3A":":","%2F":"/","%3E":">","%3B":",","%27":"'","%0D":"","%0A":"","%92":"'"}
            for s, r in rep.items():
                text = text.replace(s, r)

            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    

        except TypeError:
            pass

        return text

def removeColorTags(text):
        return re.sub('\[COLOR[^\]]{,15}\]','',text.replace("[/COLOR]", ""),re.I)
    
def removeColoredText(text):
        return re.sub('\[COLOR.*?\[/COLOR\]','',text,re.I)


def ErrorReport(e):
        elogo = xbmc.translatePath('special://home/addons/plugin.video.tvrule/resources/art/bigx.png')
        xbmc.executebuiltin("XBMC.Notification([COLOR=FF67cc33]Tv Rule Error[/COLOR],"+str(e)+",10000,"+elogo+")")
        xbmc.log('***********Tv Rule Error: '+str(e)+'**************')
        
def CloseAllDialogs():
        xbmc.executebuiltin("XBMC.Dialog.Close(all,true)")


def VIEWS():
        if selfAddon.getSetting("auto-view") == "true":
                if selfAddon.getSetting("choose-skin") == "true":
                        if selfAddon.getSetting("con-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("con-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(51)")
                        elif selfAddon.getSetting("con-view") == "2":
                                xbmc.executebuiltin("Container.SetViewMode(500)")
                        elif selfAddon.getSetting("con-view") == "3":
                                xbmc.executebuiltin("Container.SetViewMode(501)")
                        elif selfAddon.getSetting("con-view") == "4":
                                xbmc.executebuiltin("Container.SetViewMode(508)")
                        elif selfAddon.getSetting("con-view") == "5":
                                xbmc.executebuiltin("Container.SetViewMode(504)")
                        elif selfAddon.getSetting("con-view") == "6":
                                xbmc.executebuiltin("Container.SetViewMode(503)")
                        elif selfAddon.getSetting("con-view") == "7":
                                xbmc.executebuiltin("Container.SetViewMode(515)")
                        return
                elif selfAddon.getSetting("choose-skin") == "false":
                        if selfAddon.getSetting("xpr-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("xpr-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(52)")
                        elif selfAddon.getSetting("xpr-view") == "2":
                                xbmc.executebuiltin("Container.SetViewMode(501)")
                        elif selfAddon.getSetting("xpr-view") == "3":
                                xbmc.executebuiltin("Container.SetViewMode(55)")
                        elif selfAddon.getSetting("xpr-view") == "4":
                                xbmc.executebuiltin("Container.SetViewMode(54)")
                        elif selfAddon.getSetting("xpr-view") == "5":
                                xbmc.executebuiltin("Container.SetViewMode(60)")
                        elif selfAddon.getSetting("xpr-view") == "6":
                                xbmc.executebuiltin("Container.SetViewMode(53)")
                        return
        else:
                return
        

def VIEWSB():
        if selfAddon.getSetting("auto-view") == "true":
                        if selfAddon.getSetting("home-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("home-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(500)")

                        return

def VIEWSB2():
        if selfAddon.getSetting("auto-view") == "true":
                        if selfAddon.getSetting("sub-view") == "0":
                                xbmc.executebuiltin("Container.SetViewMode(50)")
                        elif selfAddon.getSetting("sub-view") == "1":
                                xbmc.executebuiltin("Container.SetViewMode(500)")

                        return
################################################################################ Movies Metahandler ##########################################################################################################

def formatCast(cast):
        roles = "\n\n"
        for role in cast:
            roles =  roles + "[COLOR blue]" + role[0] + "[/COLOR] as " + role[1] + " | "
        return roles

def GETMETAT(mname,genre,fan,thumb):
        originalName=mname
        if selfAddon.getSetting("meta-view") == "true":
                mname = re.sub(r'\[COLOR red\]\(?(\d{4})\)?\[/COLOR\]',r'\1',mname)
                mname = removeColoredText(mname)
                mname = mname.replace(' EXTENDED and UNRATED','').replace('Webrip','').replace('MaxPowers','').replace('720p','').replace('1080p','').replace('TS','').replace('HD','').replace('R6','').replace('H.M.','').replace('HackerMil','').replace('(','').replace(')','').replace('[','').replace(']','')
                mname = re.sub('Cam(?![A-Za-z])','',mname)
                mname = mname.strip()
                if re.findall('\s\d{4}',mname):
                    r = re.split('\s\d{4}',mname,re.DOTALL)
                    name = r[0]
                    year = re.findall('\s(\d{4})\s',mname + " ")
                    if year:
                        year = year[0]
                    else:
                        year=''
                else:
                    name=mname
                    year=''
                name = name.decode("ascii", "ignore")
                meta = grab.get_meta('movie',name,None,None,year=year)# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
                if not meta['year']:
                      name  = re.sub(':.*','',name)
                      meta = grab.get_meta('movie',name,None,None,year=year)
                print "Movie mode: %s"%name
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
                  'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'overlay':meta['overlay'],
                  'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year'], 'imdb_id' : meta['imdb_id']}
                if infoLabels['genre']=='':
                        infoLabels['genre']=genre
                if infoLabels['cover_url']=='':
                        infoLabels['cover_url']=thumb
                if infoLabels['backdrop_url']=='':
                        if fan=='':
                            fan=Dir+'fanart.jpg'
                        else:
                            fan=fan
                        infoLabels['backdrop_url']=fan
                if meta['overlay'] == 7:
                   infoLabels['playcount'] = 1
                else:
                   infoLabels['playcount'] = 0
                   
                if infoLabels['cover_url']=='':
                    thumb=art+'vidicon.png'
                    infoLabels['cover_url']=thumb
                #if int(year+'0'):
                #    infoLabels['year']=year 
                infoLabels['metaName']=infoLabels['title']
                infoLabels['title']=originalName

                infoLabels['plot'] = infoLabels['plot'] + formatCast(infoLabels['cast'])
        else:
                if thumb=='':
                    thumb=art+'vidicon.png'
                if fan=='':
                    fan=Dir+'fanart.jpg'
                else:
                    fan=fan
                infoLabels = {'title': mname,'metaName': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': '','plot': '','genre': genre,'imdb_id': '','tmdb_id':''}
        return infoLabels

################################################################################ TV Shows Metahandler ##########################################################################################################

def GETMETAEpiT(mname,thumb,desc):
        mname = removeColoredText(mname)
        originalName=mname
        if selfAddon.getSetting("meta-view-tv") == "true":
                mname = mname.replace('New Episode','').replace('Main Event','').replace('New Episodes','')
                mname = mname.strip()
                r = re.findall('(.+?)\ss(\d+)e(\d+)\s',mname + " ",re.I)
                if r:
                    for name,sea,epi in r:
                        year=''
                        name=name.replace(' US','').replace(' (US)','').replace(' UK',' (UK)').replace(' AU','').replace(' and',' &').replace(' 2013','').replace(' 2011','').replace(' 2012','').replace(' 2010','')
                        if re.findall('twisted',name,re.I):
                            year='2013'
                        if re.findall('the newsroom',name,re.I):
                            year='2012'
                        metaq = grab.get_meta('tvshow',name,None,None,year)
                        imdb=metaq['imdb_id']
                        tit=metaq['title']
                        year=metaq['year']
                        epiname=''

                f = re.findall('(.+?)\sseason\s(\d+)\sepisode\s(\d+)\s',mname + " ",re.I)
                if f:
                    for name,sea,epi in f:
                        year=''
                        name=name.replace(' US','').replace(' (US)','').replace(' (us)','').replace(' (uk Series)','').replace(' (UK)','').replace(' UK',' (UK)').replace(' AU','').replace(' AND',' &').replace(' And',' &').replace(' and',' &').replace(' 2013','').replace(' 2011','').replace(' 2012','').replace(' 2010','')
                        if re.findall('twisted',name,re.I):
                            year='2013'
                        if re.findall('the newsroom',name,re.I):
                            year='2012'
                        metaq = grab.get_meta('tvshow',name,None,None,year)
                        imdb=metaq['imdb_id']
                        tit=metaq['title']
                        year=metaq['year']
                        epiname=''
                        
                if len(r)==0 and len(f)==0:
                    metaq=''
                    name=mname
                    epiname=''
                    sea=0
                    epi=0
                    imdb=''
                    tit=''
                    year=''
                meta = grab.get_episode_meta(str(name),imdb, int(sea), int(epi))
                print "Episode Mode: Name %s Season %s - Episode %s"%(str(name),str(sea),str(epi))
                infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'premiered':meta['premiered'],
                      'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'overlay':meta['overlay'],'episode': meta['episode'],
                              'season': meta['season'],'backdrop_url': meta['backdrop_url']}

                if infoLabels['cover_url']=='':
                        if metaq!='':
                            thumb=metaq['cover_url']
                            infoLabels['cover_url']=thumb
                           
                if infoLabels['backdrop_url']=='':
                        fan=Dir+'fanart.jpg'
                        infoLabels['backdrop_url']=fan
                if infoLabels['cover_url']=='':
                    if thumb=='':
                        thumb=art+'/vidicon.png'
                        infoLabels['cover_url']=thumb
                    else:
                        infoLabels['cover_url']=thumb
                infoLabels['imdb_id']=imdb
                if meta['overlay'] == 7:
                   infoLabels['playcount'] = 1
                else:
                   infoLabels['playcount'] = 0
                
                infoLabels['showtitle']=tit
                infoLabels['year']=year
                infoLabels['metaName']=infoLabels['title']
                infoLabels['title']=originalName
                   
        else:
                fan=Dir+'fanart.jpg'
                infoLabels = {'title': mname,'metaName': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': '','plot': desc,'genre': '','imdb_id': ''}       
        
        return infoLabels
############################################################################### Playback resume/ mark as watched #################################################################################

def WatchedCallback():
        addon.log('Video completely watched.')
        videotype='movies'
        grab.change_watched(videotype, name, iconimage, season='', episode='', year='', watched=7)
        xbmc.executebuiltin("XBMC.Container.Refresh")

def WatchedCallbackwithParams(video_type, title, imdb_id, season, episode, year):
    print "worked"
    grab.change_watched(video_type, title, imdb_id, season=season, episode=episode, year=year, watched=7)
    xbmc.executebuiltin("XBMC.Container.Refresh")

def ChangeWatched(imdb_id, videoType, name, season, episode, year='', watched='', refresh=False):
        grab.change_watched(videoType, name, imdb_id, season=season, episode=episode, year=year, watched=watched)
        xbmc.executebuiltin("XBMC.Container.Refresh")

def refresh_movie(vidtitle,imdb, year=''):

    #global metaget
    #if not metaget:
    #    metaget=metahandlers.MetaData()
    vidtitle = vidtitle.decode("ascii", "ignore")
    if re.search("^\d+", vidtitle):
        m = re.search('^(\d+)(.*)', vidtitle)
        vidtitle = m.group(1) + m.group(2) 
    else: vidtitle = re.sub("\d+", "", vidtitle)
    vidtitle=vidtitle.replace('  ','')
    search_meta = grab.search_movies(vidtitle)
    
    if search_meta:
        movie_list = []
        for movie in search_meta:
            movie_list.append(movie['title'] + ' (' + str(movie['year']) + ')')
        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose', movie_list)
        
        if index > -1:
            new_imdb_id = search_meta[index]['imdb_id']
            new_tmdb_id = search_meta[index]['tmdb_id']
            year=search_meta[index]['year']

            meta=grab.update_meta('movie', vidtitle, imdb, '',new_imdb_id,new_tmdb_id,year)
            


            xbmc.executebuiltin("Container.Refresh")
    else:
        msg = ['No matches found']
        addon.show_ok_dialog(msg, 'Refresh Results')

def episode_refresh(vidname, imdb, season_num, episode_num):
    grab.update_episode_meta(vidname, imdb, season_num, episode_num)
    xbmc.executebuiltin("XBMC.Container.Refresh")
################################################################################Trailers#######################################################################
def trailer(tmdbid):
    if tmdbid == '':
        xbmc.executebuiltin("XBMC.Notification(Sorry!,No Trailer Available For This Movie,3000)")
    else:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading Trailer,1500)")
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1'
        request= 'http://api.themoviedb.org/3/movie/' + tmdbid + '/trailers?api_key=d5da2b7895972fffa2774ff23f40a92f'
        txheaders= {'Accept': 'application/json','User-Agent':user_agent}
        req = urllib2.Request(request,None,txheaders)
        response=urllib2.urlopen(req).read()
        if re.search('"size":"HD"',response):
            quality=re.compile('"size":"HD","source":"(.+?)"').findall(response)[0]
            youtube='http://www.youtube.com/watch?v=' + quality
            stream_url= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+quality+"&hd=1"
            xbmc.Player().play(stream_url)
        elif re.search('"size":"HQ"',response):
            quality=re.compile('"size":"HQ","source":"(.+?)"').findall(response)[0]
            youtube='http://www.youtube.com/watch?v=' + quality
            stream_url= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+quality+"&hd=1"
            xbmc.Player().play(stream_url)
        elif re.search('"size":"Standard"',response):
            quality=re.compile('"size":"Standard","source":"(.+?)"').findall(response)[0]
            youtube='http://www.youtube.com/watch?v=' + quality
            stream_url= "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+quality+"&hd=1"
            xbmc.Player().play(stream_url)
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,No Trailer Available For This Movie,3000)")

def TRAILERSEARCH(url, name, imdb):
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Getting Trailers Result,2000)")
    name = re.split(':\s\[',name)
    search      = name[0]
    infoLabels = grab._cache_lookup_by_name('movie', search.strip(), year='')
    print infoLabels
    res_name    = []
    res_url     = []
    res_name.append('[COLOR red][B]Cancel[/B][/COLOR]')
    
    site = ' site:http://www.youtube.com '
    results = SearchGoogle(search+' official trailer', site)
    for res in results:
        if res.url.encode('utf8').startswith('http://www.youtube.com/watch'):
            res_name.append(res.title.encode('utf8'))
            res_url.append(res.url.encode('utf8'))
    results = SearchGoogle(search[:(len(search)-7)]+' official trailer', site)
    
    for res in results:
        if res.url.encode('utf8').startswith('http://www.youtube.com/watch') and res.url.encode('utf8') not in res_url:
            res_name.append(res.title.encode('utf8'))
            res_url.append(res.url.encode('utf8'))
            
    dialog = xbmcgui.Dialog()
    ret = dialog.select(search + ' trailer search',res_name)

    if ret == 0:
        return
    elif ret >= 1:
        trailer_url = res_url[ret - 0]
        try:
            xbmc.executebuiltin(
                "PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid=%s)" 
                % str(trailer_url)[str(trailer_url).rfind("v=")+2:] )
            if re.findall('Darwin iOS',PLATFORM):
                grab.update_trailer('movie', imdb, trailer_url)
                xbmc.executebuiltin("XBMC.Container.Refresh")

        except:
            return    


############################################################################### Resolvers ############################################################################################
def resolve_url(url):
    return resolvers.resolve_url(url)
############################################################################### Download Code ###########################################################################################
downloadPath = selfAddon.getSetting('download-folder')
DownloadLog=os.path.join(datapath,'Downloads')
try:
    os.makedirs(DownloadLog)
except:
    pass
DownloadFile=os.path.join(DownloadLog,'DownloadLog') 

class StopDownloading(Exception): 
        def __init__(self, value): 
            self.value = value 
        def __str__(self): 
            return repr(self.value)
def GetUrliW(url):
        link=OPENURL(url)
        link=unescapes(link)
        match=re.compile('<(?:iframe|pagespeed_iframe).+?src=\"(.+?)\"').findall(link)
        link=match[0]
        return link

def geturl(url):
        link=OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('<a class="myButton" href="(.+?)">Click Here to Play</a>').findall(link)
        if len(match)==0:
                match=re.compile('<a class="myButton" href="(.+?)">Click Here to Play Part1</a><a class="myButton" href="(.+?)">Click Here to Play Part2</a>').findall(link)
                return match[0]
        else:
                return match[0]

def Download_Source(name,url):
    originalName=name
    match=re.compile('watchseries.lt').findall(url)
    if match:
        name=name.replace('/','').replace('.','').replace(':','')
        name=name.replace('[DVD]','').replace('[TS]','').replace('[TC]','').replace('[CAM]','').replace('[SCREENER]','').replace('[COLOR blue]','').replace('[COLOR red]','').replace('[/COLOR]','').replace('[COLOR]','')
        name=name.replace(' : Gorillavid','').replace(' : Divxstage','').replace(' : Movshare','').replace(' : Sharesix','').replace(' : Movpod','').replace(' : Daclips','').replace(' : Videoweed','')
        name=name.replace(' : Played','').replace(' : MovDivx','').replace(' : Movreel','').replace(' : BillionUploads','').replace(' : Putlocker','').replace(' : Sockshare','').replace(' : Nowvideo','').replace(' : 180upload','').replace(' : Filenuke','').replace(' : Flashx','').replace(' : Novamov','').replace(' : Uploadc','').replace(' : Xvidstage','').replace(' : Zooupload','').replace(' : Zalaa','').replace(' : Vidxden','').replace(' : Vidbux','')
        name=name.replace(' 720p BRRip','').replace(' 720p HDRip','').replace(' 720p WEBRip','').replace(' 720p BluRay','')
        name=name.replace('  Part:1','').replace('  Part:2','').replace('  Part:3','').replace('  Part:4','')
        match=re.compile('(.+?)xocx(.+?)xocx').findall(url)
        for hurl, durl in match:
            url=geturl('http://watchseries.lt'+hurl)
    match2=re.compile('iwatchonline').findall(url)
    if match2:
        name=name.split('[COLOR red]')[0]
        name=name.replace('/','').replace('.','')
        url=GetUrliW(url)
    
    
    name=name.split(' [')[0]
    name=name.split('[')[0]
    name=name.split(' /')[0]
    name=name.split('/')[0]

    stream_url = resolve_url(url)
        
    if stream_url:
            print stream_url
            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,2000)")
            if os.path.exists(downloadPath):
                match1=re.compile("flv").findall(stream_url)
                if len(match1)>0:
                    name=name+'.flv'
                match2=re.compile("mkv").findall(stream_url)
                if len(match2)>0:
                    name=name+'.mkv'
                match3=re.compile("mp4").findall(stream_url)
                if len(match3)>0:
                    name=name+'.mp4'
                match4=re.compile("avi").findall(stream_url)
                if len(match4)>0:
                    name=name+'.avi'
                mypath=os.path.join(downloadPath,name)
                if os.path.isfile(mypath) is True:
                    xbmc.executebuiltin("XBMC.Notification(Download Alert!,The video you are trying to download already exists!,8000)")
                else:
                    DownloadInBack=selfAddon.getSetting('download-in-background')
                    if DownloadInBack == 'true':
                        QuietDownload(stream_url,mypath,originalName,name)
                    else:
                        Download(stream_url,mypath,originalName,name)
            
            else:
                xbmc.executebuiltin("XBMC.Notification(Download Alert!,You have not set the download folder,8000)")
                return False
                
    else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Not Found,6000)")
            stream_url = False


def GetNoobroom():
        link=OPENURL('http://www.noobroom.com')
        match=re.compile('value="(.+?)">').findall(link)
        return match[0]            
def Noobroom(page_url):
    user = selfAddon.getSetting('username')
    passw = selfAddon.getSetting('password')
    import re
    import urllib2
    
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'}
   

    url=GetNoobroom()+'/login2.php'
    net1 = net()
    log_in = net1.http_POST(url,{'email':user,'password':passw}).content
    #print net1.get_cookies()
    html = net1.http_GET(page_url).content
    media_id = re.compile('"file": "(.+?)"').findall(html)[0]
    fork_url = re.compile('"streamer": "(.+?)"').findall(html)[0] + '&start=0&file=' + media_id

    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):    
        def http_error_302(self, req, fp, code, msg, headers):
            #print headers
            self.video_url = headers['Location']
            #print self.video_url
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302

    myhr = MyHTTPRedirectHandler()

    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(net1._cj),
        urllib2.HTTPBasicAuthHandler(),
        myhr)
    urllib2.install_opener(opener)

    req = urllib2.Request(fork_url)
    for k, v in headers.items():
                req.add_header(k, v)
    try:            
        response = urllib2.urlopen(req)
    except:
        pass

    #print myhr.video_url
    return myhr.video_url   

def Download_SourceB(name,url):#starplay/noobroom
    originalName=name
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,5000)")

    stream_url= Noobroom(url)
    name=name.split(' [')[0]
    name=name.replace('/','').replace('.','').replace(':','')

    if stream_url:
            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,2000)")
            if os.path.exists(downloadPath):
                match1=re.compile("flv").findall(stream_url)
                if len(match1)>0:
                    name=name+'.flv'
                match2=re.compile("mkv").findall(stream_url)
                if len(match2)>0:
                    name=name+'.mkv'
                match3=re.compile("mp4").findall(stream_url)
                if len(match3)>0:
                    name=name+'.mp4'
                match4=re.compile("avi").findall(stream_url)
                if len(match4)>0:
                    name=name+'.avi'
                mypath=os.path.join(downloadPath,name)
                if os.path.isfile(mypath) is True:
                    xbmc.executebuiltin("XBMC.Notification(Download Alert!,The video you are trying to download already exists!,8000)")
                else:
                    DownloadInBack=selfAddon.getSetting('download-in-background')
                    if DownloadInBack == 'true':
                        QuietDownload(stream_url,mypath,originalName,name)
                    else:
                        Download(stream_url,mypath,originalName,name)
            
            else:
                xbmc.executebuiltin("XBMC.Notification(Download Alert!,You have not set the download folder,8000)")
                return False
                
    else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Not Found,6000)")
            stream_url = False

def Download(url, dest,originalName, displayname=False):
         
        if displayname == False:
            displayname=url
        delete_incomplete = selfAddon.getSetting('delete-incomplete-downloads')
        dp = xbmcgui.DialogProgress()
        dp.create('Downloading:    '+displayname)
        start_time = time.time() 
        try: 
            urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))
            open(DownloadFile,'a').write('{name="%s",destination="%s"}'%(originalName,dest))
            
        except:
            if delete_incomplete == 'true':
                #delete partially downloaded file if setting says to.
                while os.path.exists(dest): 
                    try: 
                        os.remove(dest) 
                        break 
                    except: 
                        pass 
            #only handle StopDownloading (from cancel), ContentTooShort (from urlretrieve), and OS (from the race condition); let other exceptions bubble 
            if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): 
                return False 
            else: 
                raise 
            return False
        return True

def QuietDownload(url, dest,originalName, videoname):
    #quote parameters passed to download script     
    q_url = urllib.quote_plus(url)
    q_dest = urllib.quote_plus(dest)
    q_vidname = urllib.quote_plus(videoname)
    q_vidOname = urllib.quote_plus(originalName)
    
    #Create possible values for notification
    notifyValues = [2, 5, 10, 20, 25, 50, 100]

    # get notify value from settings
    NotifyPercent=int(selfAddon.getSetting('notify-percent'))
    
    script = os.path.join( tvrulepath, 'resources', 'libs', "DownloadInBackground.py" )
    xbmc.executebuiltin( "RunScript(%s, %s, %s, %s, %s, %s)" % ( script, q_url, q_dest, q_vidname,q_vidOname, str(notifyValues[NotifyPercent]) ) )
    return True

 
def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            # print ( 
                # percent, 
                # numblocks, 
                # blocksize, 
                # filesize, 
                # currently_downloaded, 
                # kbps_speed, 
                # eta, 
                # ) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Kb/s ' % kbps_speed 
            e += 'ETA: %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs, e)
            #print percent, mbs, e 
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close() 
            raise StopDownloading('Stopped Downloading')


def jDownloader(url):
    match2=re.compile('iwatchonline').findall(url)
    if match2:
        url=GetUrliW(url)
    match=re.compile('watchseries.lt').findall(url)
    if match:
        match=re.compile('(.+?)xocx(.+?)xocx').findall(url)
        for hurl, durl in match:
            url=geturl('http://watchseries.lt'+hurl)
    match3=re.findall('xoxv(.+?)xoxe(.+?)xoxc',url)
    if match3:
        for hoster, hurl in match3:
            media= urlresolver.HostedMediaFile(host=hoster, media_id=hurl)
            r=re.findall("'url': '(.+?)',",str(media))[0]
            url=r
    print "Downloading "+url+" via jDownlaoder"
    cmd = 'plugin://plugin.program.jdownloader/?action=addlink&url='+url
    xbmc.executebuiltin('XBMC.RunPlugin(%s)' % cmd)

################################################################################ Message ##########################################################################################################

def Message():
    help = SHOWMessage()
    help.doModal()
    del help


class SHOWMessage(xbmcgui.Window):
    def __init__(self):
        self.addControl(xbmcgui.ControlImage(0,0,1280,720,art+'/infoposter.png'))
    def onAction(self, action):
        if action == 92 or action == 10:
            xbmc.Player().stop()
            self.close()

def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()
    

################################################################################ Types of Directories ##########################################################################################################

def addDirT(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='DIR'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_directory(name, u, section_title='TV', section_addon_title="TV Show Fav's", sub_section_title='Shows', img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='TV', section_addon_title="TV Show Fav's", sub_section_title='Shows'))]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands, replaceItems=True )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 

def addPlayT(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='PLAY'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_video_item(name, u, section_title='TV', section_addon_title="TV Show Fav's", sub_section_title='Shows', img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='TV', section_addon_title="TV Show Fav's", sub_section_title='Shows'))]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands, replaceItems=True )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok 

def addDirTE(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        infoLabels =GETMETAEpiT(name,iconimage,'')
        if selfAddon.getSetting("meta-view-tv") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        else:
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        type='DIR'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_directory(name, u, section_title='TV', section_addon_title="TV Episode Fav's", sub_section_title='Episodes', img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='TV', section_addon_title="TV Episode Fav's", sub_section_title='Episodes'))]
        if selfAddon.getSetting("meta-view-tv") == "true":
                video_type='episode'
                cname=infoLabels['title']
                cname=cname.decode('ascii', 'ignore')
                cname=urllib.quote_plus(cname)
                sea=infoLabels['season']
                epi=infoLabels['episode']
                imdb_id=infoLabels['imdb_id']
                if imdb_id != '':
                    Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=779&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type, imdb_id,sea,epi)))
               # Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=780&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type,imdb_id,sea,epi)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands, replaceItems=True )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 


def addPlayTE(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        mname=name
        if re.findall('sceper',url):
            mname=name.split('&')[0]
        infoLabels =GETMETAEpiT(mname,iconimage,plot)
        if selfAddon.getSetting("meta-view-tv") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        else:
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        type='PLAY'
        plot=plot.encode('ascii', 'ignore')
        
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_video_item(name, u, section_title='TV', section_addon_title="TV Episode Fav's", sub_section_title='Episodes', img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='TV', section_addon_title="TV Episode Fav's", sub_section_title='Episodes'))]
        if selfAddon.getSetting("meta-view-tv") == "true":
                video_type='episode'
                cname=infoLabels['title']
                cname=cname.decode('ascii', 'ignore')
                cname=urllib.quote_plus(cname)
                sea=infoLabels['season']
                epi=infoLabels['episode']
                imdb_id=infoLabels['imdb_id']
                if imdb_id != '':
                    Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=779&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type, imdb_id,sea,epi)))
                #Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=780&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type,imdb_id,sea,epi)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands, replaceItems=True )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDirM(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        infoLabels =GETMETAT(name,genre,fanart,iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                tmdbid=infoLabels['tmdb_id']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
        else:
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        type='DIR'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_directory(name, u, section_title='Movies', section_addon_title="Movie Fav's", img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Movies', section_addon_title="Movie Fav's"))]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=urllib.quote_plus(infoLabels['metaName'])
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                #Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands, replaceItems=True )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 


def addPlayM(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        infoLabels =GETMETAT(name,genre,fanart,iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                tmdbid=infoLabels['tmdb_id']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
        else:
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        type='PLAY'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_video_item(name, u, section_title='Movies', section_addon_title="Movie Fav's", img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Movies', section_addon_title="Movie Fav's"))]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=urllib.quote_plus(infoLabels['metaName'])
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
               # Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands, replaceItems=True )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
    
def addDirMs(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='DIR'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_directory(name, u, section_title='Misc.', section_addon_title="Misc. Fav's", img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Misc.', section_addon_title="Misc. Fav's"))]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands, replaceItems=True )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 

def addPlayMs(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='PLAY'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_video_item(name, u, section_title='Misc.', section_addon_title="Misc. Fav's", img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Misc.', section_addon_title="Misc. Fav's"))]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands, replaceItems=True )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDirL(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='DIR'
        
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_directory(name, u, section_title='Live', section_addon_title="Live Fav's", img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Live', section_addon_title="Live Fav's"))]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands, replaceItems=True )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 

def addPlayL(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if iconimage=='':
            iconimage=art+'vidicon.png'
        if plot=='':
            plot='Sorry description not available'
        type='PLAY'
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_video_item(name, u, section_title='Live', section_addon_title="Live Fav's", img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Live', section_addon_title="Live Fav's"))]
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( Commands, replaceItems=True )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addPlayc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        contextMenuItems=[]
        if iconimage==None:
            iconimage=''
        if plot==None:
            plot=''
        if fanart==None:
            fanart=''
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems( contextMenuItems, replaceItems=True )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
    
def addDirb(name,url,mode,iconimage,fanart):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="%s/art/vidicon.png"%selfAddon.getAddonInfo("path"), thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirXml(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/xmlplaylist.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if selfAddon.getSetting("addmethod") == "true":
            contextMenuItems.append(('[B][COLOR blue]Add[/COLOR][/B] Playlist','XBMC.RunPlugin(%s?name=None&mode=250&url=%s&iconimage=None)'% (sys.argv[0],urllib.quote_plus(plot))))
        contextMenuItems.append(("[B][COLOR red]Remove[/COLOR][/B] Playlist",'XBMC.RunPlugin(%s?name=%s&mode=251&url=%s&iconimage=%s)'% (sys.argv[0],name,urllib.quote_plus(url),plot)))
        contextMenuItems.append(("[B][COLOR aqua]Edit[/COLOR][/B] Playlist",'XBMC.RunPlugin(%s?name=%s&mode=255&url=%s&iconimage=%s)'% (sys.argv[0],name,urllib.quote_plus(url),plot)))
        if selfAddon.getSetting("addmethod") == "true":
            contextMenuItems.append(('[B][COLOR blue]Add[/COLOR][/B] Folder','XBMC.RunPlugin(%s?name=%s&mode=252&url=%s&iconimage=None)'% (sys.argv[0],name,plot)))
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if dur=='Livestreams':
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addXmlFolder(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/folder.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=Dir+'fanart.jpg'
        liz.setProperty('fanart_image', fanart)
        if selfAddon.getSetting("addmethod") == "true":
            contextMenuItems.append(('[B][COLOR blue]Add[/COLOR][/B] Playlist','XBMC.RunPlugin(%s?name=None&mode=250&url=%s&iconimage=None)'% (sys.argv[0],urllib.quote_plus(plot))))
            if plot=='home':
                contextMenuItems.append(('[B][COLOR blue]Add[/COLOR][/B] Folder','XBMC.RunPlugin(%s?name=%s&mode=252&url=%s&iconimage=None)'% (sys.argv[0],name,urllib.quote_plus(plot))))
        contextMenuItems.append(("[B][COLOR red]Remove[/COLOR][/B] Folder",'XBMC.RunPlugin(%s?name=%s&mode=254&url=%s&iconimage=None)'% (sys.argv[0],name,url)))
        contextMenuItems.append(("[B][COLOR aqua]Edit[/COLOR][/B] Folder",'XBMC.RunPlugin(%s?name=%s&mode=256&url=%s&iconimage=None)'% (sys.argv[0],name,url)))
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/link.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirHome(name,url,mode,iconimage):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(name,url,mode,iconimage,plot):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&plot="+str(plot)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirFIX(name,url,mode,iconimage,location,path):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&location="+urllib.quote_plus(location)+"&path="+urllib.quote_plus(path)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', Dir+'fanart.jpg')
        contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDown(name,url,mode,iconimage,fan):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        link=OPENURL(url)
        match=re.compile("Javascript:location.?href=.+?'(.+?)\'").findall(link)
        if len(match)>0:
            for url in match:
                sysurl = urllib.quote_plus(url)
        else:
            sysurl = urllib.quote_plus(url)
        sysname= urllib.quote_plus(name)
        contextMenuItems.append(('Direct Download', 'XBMC.RunPlugin(%s?mode=190&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
        contextMenuItems.append(('Download with jDownloader', 'XBMC.RunPlugin(%s?mode=776&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fan)
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDown2(name,url,mode,iconimage,fan):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        sysurl = urllib.quote_plus(url)
        sysname= urllib.quote_plus(name)
        contextMenuItems.append(('Direct Download', 'XBMC.RunPlugin(%s?mode=190&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
        contextMenuItems.append(('Download with jDownloader', 'XBMC.RunPlugin(%s?mode=776&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fan)
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDown3(name,url,mode,iconimage,fanart,id=False):#Noobroom only
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        infoLabels =GETMETAT(name,'','',iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                tmdbid=infoLabels['tmdb_id']
                plot=infoLabels['plot']
                name=infoLabels['metaName']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PLAYLIST_ORDER )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_TITLE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
        else:
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )

            plot='Sorry description not available'
            plot=plot.replace(",",'.')
        name=name.replace(",",'')
        sysurl = urllib.quote_plus(url)
        sysname= urllib.quote_plus(name)
        
        type='PLAY'
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_video_item(name, u, section_title='Movies', section_addon_title="Movie Fav's", img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Movies', section_addon_title="Movie Fav's")),
            ('Direct Download', 'XBMC.RunPlugin(%s?mode=212&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl))]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=urllib.quote_plus(infoLabels['metaName'])
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                #Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands, replaceItems=True )
        if(id != False):
            infoLabels["count"] = id
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDown4(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        Commands=[]
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        st=""
        sst=""
        sat=""
        if re.findall('(.+?)\ss(\d+)e(\d+)\s',name,re.I) or re.findall('Season(.+?)Episode([^<]+)',name,re.I):
            infoLabels =GETMETAEpiT(name,iconimage,plot)
            video_type='episode'
            sea=infoLabels['season']
            epi=infoLabels['episode']
            cname=urllib.quote_plus(infoLabels['title'].decode("ascii", "ignore"))
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            st="TV"
            sst="Episodes"
            sat="TV Episode Fav's"
        else:
            infoLabels =GETMETAT(name,genre,fanart,iconimage)
            video_type='movie'
            tmdbid=infoLabels['tmdb_id']
            cname=urllib.quote_plus(infoLabels['metaName'])
            xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
            st="Movies"
            sst=""
            sat="Movie Fav's"
        if ((selfAddon.getSetting("meta-view") == "true" and video_type == 'movie') or 
            (selfAddon.getSetting("meta-view-tv") == "true" and video_type == 'episode')):
                imdb_id=infoLabels['imdb_id']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
        else:
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        if(selfAddon.getSetting("meta-view-tv") != "true"):
            xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        sysurl = urllib.quote_plus(url)
        sysname= urllib.quote_plus(name)
        type='PLAY'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",'.')
        name=name.replace(",",'')
        args=[(url,name,mode,iconimage,str(plot),type)]
        if '</sublink>' not in url:
            Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_video_item(name, u, section_title=st, section_addon_title=sat, sub_section_title=sst, img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
                ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title=st, section_addon_title=sat, sub_section_title=sst)),
                  ('Direct Download', 'XBMC.RunPlugin(%s?mode=190&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)),
                  ('Download with jDownloader', 'XBMC.RunPlugin(%s?mode=776&name=%s&url=%s)' % (sys.argv[0], sysname, url))]
        if (selfAddon.getSetting("meta-view") == "true" and video_type == 'movie'):
            Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb_id)))
            #Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb_id)))
        elif (selfAddon.getSetting("meta-view-tv") == "true" and video_type == 'episode'):
            if imdb_id != '':
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=779&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type,imdb_id,sea,epi)))
            #Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=780&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type,imdb_id,sea,epi)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands, replaceItems=True )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        if '</sublink>' in url:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDownLink(name,url,mode,iconimage,fan):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        ok=True
        name=BeautifulSoup(name, convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fan)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok    

def addInfo(name,url,mode,iconimage,gen,year):
        ok=True
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        name=name.replace('()','')
        infoLabels = GETMETAT(name,gen,year,iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                tmdbid=infoLabels['tmdb_id']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
        else:
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=urllib.quote_plus(infoLabels['metaName'])
                #Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                #Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addDirIWO(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        infoLabels =GETMETAT(name,genre,fanart,iconimage)
        if selfAddon.getSetting("meta-view") == "true":
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                tmdbid=infoLabels['tmdb_id']
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
        else:
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        type='DIR'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        plot=plot.encode('ascii', 'ignore')
        plot=plot.replace(",",".").replace('"','')
        name=name.replace(",",'')
        iconimage=iconimage.replace(",",".")
        Commands=[("[B][COLOR blue]Add[/COLOR][/B] to My Fav's",fav.add_directory(name, u, section_title='Movies', section_addon_title="iWatchOnline Fav's", img=iconimage, fanart=fanart, infolabels={'item_mode':mode, 'item_url':url, 'plot':plot,'duration':dur,'genre':genre,'year':year})),
            ("[B][COLOR red]Remove[/COLOR][/B] from My Fav's",fav.delete_item(name, section_title='Movies', section_addon_title="iWatchOnline Fav's"))]
        if selfAddon.getSetting("meta-view") == "true":
                video_type='movie'
                imdb=infoLabels['imdb_id']
                cname=urllib.quote_plus(infoLabels['metaName'])
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
                #Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands, replaceItems=True )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok 
    
def addDLog(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
        ok=True
        if re.findall('(.+?)\ss(\d+)e(\d+)\s',name,re.I) or re.findall('Season(.+?)Episode([^<]+)',name,re.I):
            infoLabels =GETMETAEpiT(name,iconimage,plot)
            video_type='episode'
            sea=infoLabels['season']
            epi=infoLabels['episode']
            cname=urllib.quote_plus(infoLabels['title'].decode("ascii", "ignore"))
        else:
            infoLabels =GETMETAT(name,genre,fanart,iconimage)
            video_type='movie'
            tmdbid=infoLabels['tmdb_id']
            cname=urllib.quote_plus(infoLabels['metaName'])
        if ((selfAddon.getSetting("meta-view") == "true" and video_type == 'movie') or 
            (selfAddon.getSetting("meta-view-tv") == "true" and video_type == 'episode')):
                imdb_id=infoLabels['imdb_id']
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                if infoLabels['overlay'] == 6:
                    watched_mark = 'Mark as Watched'
                else:
                    watched_mark = 'Mark as Unwatched'
        else:
            if fanart == '':
                fanart=Dir+'fanart.jpg'
            if iconimage=='':
                iconimage=art+'vidicon.png'
            if plot=='':
                plot='Sorry description not available'
        type='PLAY'
        plot=infoLabels['plot']
        img=infoLabels['cover_url']
        Commands=[("[B][COLOR red]Remove[/COLOR][/B]",'XBMC.RunPlugin(%s?mode=243&name=%s&url=%s)'% (sys.argv[0],name,url))]
        if (selfAddon.getSetting("meta-view") == "true" and video_type == 'movie'):
            Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb_id)))
            #Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, video_type,imdb_id)))
        elif (selfAddon.getSetting("meta-view-tv") == "true" and video_type == 'episode'):
            if imdb_id != '':
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=779&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type,imdb_id,sea,epi)))
            #Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=780&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, video_type,imdb_id,sea,epi)))
        Commands.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
        Commands.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
        liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=infoLabels['cover_url'])
        liz.addContextMenuItems( Commands, replaceItems=True )
        liz.setInfo( type="Video", infoLabels = infoLabels)
        liz.setProperty('fanart_image', infoLabels['backdrop_url'])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok    

def addSpecial(name,url,mode,iconimage):
    liz=xbmcgui.ListItem(name,iconImage="",thumbnailImage = iconimage)
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)

def addSearchDir(name,url, mode,iconimage):
    #thumbnail = 'DefaultPlaylist.png'
    u         = sys.argv[0]+"?url="+urllib.quote_plus(url) + "?mode=" + str(mode)        
    liz       = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty('fanart_image', Dir+'fanart.jpg')
    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)
