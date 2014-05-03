import urllib,urllib2,re,string,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import time,threading

#Filmesonline2 - by Kasik 2013.

addon_id = 'plugin.video.filmesonline2'
selfAddon = xbmcaddon.Addon(id=addon_id)
filmesonline2path = selfAddon.getAddonInfo('path')
grab = None
fav = False
hostlist = None
Dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.filmesonline2', ''))
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
hosts = 'putlocker,firedrive,sockshare,billionuploads,hugefiles,mightyupload,movreel,lemuploads,180upload,megarelease,filenuke,flashx,gorillavid,bayfiles,veehd,vidto,mailru,videomega,epicshare,bayfiles,2gbhosting,alldebrid,allmyvideos,vidspot,castamp,cheesestream,clicktoview,crunchyroll,cyberlocker,daclips,dailymotion,divxstage,donevideo,ecostream,entroupload,facebook,filebox,hostingbulk,hostingcup,jumbofiles,limevideo,movdivx,movpod,movshare,movzap,muchshare,nolimitvideo,nosvideo,novamov,nowvideo,ovfile,play44_net,played,playwire,premiumize_me,primeshare,promptfile,purevid,rapidvideo,realdebrid,rpnet,seeon,sharefiles,sharerepo,sharesix,skyload,stagevu,stream2k,streamcloud,thefile,tubeplus,tunepk,ufliq,upbulk,uploadc,uploadcrazynet,veoh,vidbull,vidcrazynet,video44,videobb,videofun,videotanker,videoweed,videozed,videozer,vidhog,vidpe,vidplay,vidstream,vidup,vidx,vidxden,vidzur,vimeo,vureel,watchfreeinhd,xvidstage,yourupload,youtube,youwatch,zalaa,zooupload,zshare'

VERSION = "0.1.1"
PATH = "Filmesonline2-"  


try:
    log_path = xbmc.translatePath('special://logpath')
    log = os.path.join(log_path, 'xbmc.log')
    logfile = open(log, 'r').read()
    match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built').search(logfile)
    if match:
        PLATFORM = match.group(1)
        build = match.group(2)
        print 'XBMC '+build+' Platform '+PLATFORM
    else:
        PLATFORM=''
except:
    PLATFORM=''

sys.path.append( os.path.join( selfAddon.getAddonInfo('path'), 'resources', 'libs' ))
################################################################################ Common Calls ##########################################################################################################
art = xbmc.translatePath('special://home/addons/plugin.video.filmesonline2/resources/art/')
fanartimage=Dir+'fanart2.jpg'
elogo = xbmc.translatePath('special://home/addons/plugin.video.filmesonline2/resources/art/bigx.jpg')
slogo = xbmc.translatePath('special://home/addons/plugin.video.filmesonline2/resources/art/smallicon.png')

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    #req.add_header('Referer', '')

    response = urllib2.urlopen(req)
    link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&player=2','').replace("",'').replace('\xe2\x80\x99',"'").replace('\xe2\x80\x93','-')
    response.close()
    return link


def OPENURL(url, mobile = False, q = False, verbose = True, timeout = 10, cookie = None, data = None, cookiejar = False, log = True, headers = [], type = ''):
    import urllib2 
    UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    try:
        if log:
            print "Openurl = " + url
        if cookie and not cookiejar:
            import cookielib
            cookie_file = os.path.join(os.path.join(datapath,'Cookies'), cookie+'.cookies')
            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try: cj.load(cookie_file,True)
                except: cj.save(cookie_file,True)
            else: cj.save(cookie_file,True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        elif cookiejar:
            import cookielib
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        else:
            opener = urllib2.build_opener()
        if mobile:
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')]
        else:
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
        for header in headers:
            opener.addheaders.append(header)
        if data:
            if type == 'json': 
                import json
                data = json.dumps(data)
                opener.addheaders.append(('Content-Type', 'application/json'))
            else: data = urllib.urlencode(data)
            response = opener.open(url, data, timeout)
        else:
            response = opener.open(url, timeout=timeout)
        if cookie and not cookiejar:
            cj.save(cookie_file,True)
        link=response.read()
        response.close()
        opener.close()
        #link = net(UserAgent).http_GET(url).content
        link=link.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','x').replace('&#038;','&').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
        link=link.replace('%3A',':').replace('%2F','/')
        if q: q.put(link)
        return link
    except Exception as e:
        if verbose:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Source Website is Down,3000,"+elogo+")")
        xbmc.log('***********Website Error: '+str(e)+'**************', xbmc.LOGERROR)
        import traceback
        traceback.print_exc()
        link ='website down'
        if q: q.put(link)
        return link
    
def batchOPENURL(urls, mobile = False, merge = True):
    try:
        import Queue as queue
    except ImportError:
        import queue
    max = len(urls)
    results = []
    for url in urls: 
        q = queue.Queue()
        threading.Thread(target=OPENURL, args=(url,mobile,q)).start()
        results.append(q)
    if merge: content = ''
    else: content = []
    for n in range(max):
        if merge: content += results[n].get()
        else: content.append(results[n].get())
    return content

def OPENURL2(url):
    from t0mm0.common.net import Net as net
    UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    try:
        print "Openurl = " + url
        link = net(UserAgent).http_GET(url).content
        return link.encode('utf-8', 'ignore')
    except:
        xbmc.executebuiltin("XBMC.Notification(Sorry!,Source Website is Down,3000,"+elogo+")")
        link ='website down'
        return link
        
def REDIRECT(url):
        import urllib2
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.geturl()
        return link

def Clearhistory(path):
    if os.path.exists(path):
        os.remove(path)
    
def setGrab():
    global grab
    if grab is None:
        from metahandler import metahandlers
        grab = metahandlers.MetaData()
        
def getFav():
    global fav
    if not fav:
        from resources.universal import favorites
        fav = favorites.Favorites(addon_id, sys.argv)
    return fav

def getRDHosts():
    CachePath = os.path.join(datapath,'Cache')
    CachedRDHosts = xbmc.translatePath(os.path.join(CachePath, 'rdhosts'))
    rdhosts =  getFile(CachedRDHosts)
    if not rdhosts or os.stat(CachedRDHosts).st_mtime + 86400 < time.time():
        rdhosts = OPENURL('http://real-debrid.com/api/hosters.php').replace('"', '')
        setFile(CachedRDHosts,rdhosts,True)
    return rdhosts

def getHostList():
    global hostlist
    if not hostlist:
        hostlist = hosts
        try: 
            if xbmcaddon.Addon(id='script.module.urlresolver').getSetting("RealDebridResolver_enabled") == 'true': hostlist += getRDHosts()
        except: pass
    return hostlist

def unescapes(text):
    try:
        rep = {"%26":"&","&#38;":"&","&amp;":"&","&#044;": ",","&nbsp;": " ","\n": "","\t": "","\r": "","%5B": "[","%5D": "]",
               "%3a": ":","%3A":":","%2f":"/","%2F":"/","%3f":"?","%3F":"?","%3d":"=","%3D":"=","%2C":",","%2c":",","%3C":"<",
               "%20":" ","%22":'"',"%3D":"=","%3A":":","%2F":"/","%3E":">","%3B":",","%27":"'","%0D":"","%0A":"","%92":"'",
               "&lt;": "<","&gt;": ">","&quot": '"',"&rsquo;": "'","&acute;": "'"}
        for s, r in rep.items():
            text = text.replace(s, r)
        text = re.sub(r"<!--.+?-->", "", text)    
    except TypeError: pass
    return text

def removeColorTags(text):
    return re.sub('\[COLOR[^\]]{,15}\]','',text.replace("[/COLOR]", ""),re.I|re.DOTALL).strip()
    
def removeColoredText(text):
    return re.sub('\[COLOR.*?\[/COLOR\]','',text,re.I|re.DOTALL).strip()

def SwitchUp():
    if selfAddon.getSetting("switchup") == "false":
        selfAddon.setSetting(id="switchup", value="true")
    else:
        selfAddon.setSetting(id="switchup", value="false")
    xbmc.executebuiltin("XBMC.Container.Refresh")

def ErrorReport(e):
    elogo = xbmc.translatePath('special://home/addons/plugin.video.filmesonline2/resources/art/bigx.jpg')
    xbmc.executebuiltin("XBMC.Notification([COLOR=FF67cc33]Filmesonline2 Error[/COLOR],"+str(e)+",10000,"+elogo+")")
    xbmc.log('***********Filmesonline2 Error: '+str(e)+'**************', xbmc.LOGERROR)
        
def CloseAllDialogs():
    xbmc.executebuiltin("XBMC.Dialog.Close(all,true)")
        
def ClearDir(dir, clearNested = False):
    for the_file in os.listdir(dir):
        file_path = os.path.join(dir, the_file)
        if clearNested and os.path.isdir(file_path):
            ClearDir(file_path, clearNested)
            try: os.rmdir(file_path)
            except Exception, e: print str(e)
        else:
            try:os.unlink(file_path)
            except Exception, e: print str(e)

def removeFile(file):
    try: 
        if os.path.exists(file): os.remove(file)
        return True
    except: return False
        
def getFileName(file):
    return re.sub('.*?([\w-]+)\.[^\.]+$','\\1',file)   
     
def getFile(path):
    content = None
    if os.path.exists(path):
        try: content = open(path).read()
        except: pass
    return content
   
def setFile(path,content,force=False):
    if os.path.exists(path) and not force:
        return False
    else:
        try:
            open(path,'w+').write(content)
            return True
        except: pass
    return False 

def downloadFile(url,dest,silent = False,cookie = None):
    try:
        import urllib2
        file_name = url.split('/')[-1]
        print "Downloading: %s" % (file_name)
        if cookie:
            import cookielib
            cookie_file = os.path.join(os.path.join(datapath,'Cookies'), cookie+'.cookies')
            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try: cj.load(cookie_file,True)
                except: cj.save(cookie_file,True)
            else: cj.save(cookie_file,True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        else:
            opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
        u = opener.open(url)
        f = open(dest, 'wb')
        meta = u.info()
        if meta.getheaders("Content-Length"):
            file_size = int(meta.getheaders("Content-Length")[0])
        else: file_size = 'Unknown'
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer: break
            file_size_dl += len(buffer)
            f.write(buffer)
#             status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
#             status = status + chr(8)*(len(status)+1)
#             print status,
        print "Downloaded: %s %s Bytes" % (file_name, file_size)
        f.close()
        return True
    except Exception, e:
        print 'Error downloading file ' + url.split('/')[-1]
        main.ErrorReport(e)
        if not silent:
            dialog = xbmcgui.Dialog()
            dialog.ok("Filmesonline2", "Report the error below at " + supportsite, str(e), "We will try our best to help you")
        return False
            
def updateSearchFile(searchQuery,searchType,defaultValue = '###',searchMsg = ''):
    addToSearchHistory = True
    searchpath=os.path.join(datapath,'Search')
    if searchType == "TV":
        searchHistoryFile = "SearchHistoryTv"
        if not searchMsg: searchMsg = 'Search For TV Shows' 
    else:
        searchHistoryFile = "SearchHistoryMV"
        if not searchMsg: searchMsg = 'Search For Movies' 
    SearchFile=os.path.join(searchpath,searchHistoryFile)
    searchQuery=urllib.unquote(searchQuery)
    if not searchQuery or searchQuery == defaultValue:
        searchQuery = ''
        try: os.makedirs(searchpath)
        except: pass
        keyb = xbmc.Keyboard('', searchMsg )
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchQuery = keyb.getText()
        else:
            xbmcplugin.endOfDirectory(int(sys.argv[1]),False,False)
            return False
    else:
        addToSearchHistory = False
    searchQuery=urllib.quote(searchQuery)
    if os.path.exists(SearchFile):
        searchitems=re.compile('search="([^"]+?)",').findall(open(SearchFile,'r').read())
        if searchitems.count(searchQuery) > 0: addToSearchHistory = True
    if addToSearchHistory:
        if not os.path.exists(SearchFile) and searchQuery != '':
            open(SearchFile,'w').write('search="%s",'%searchQuery)
        elif searchQuery != '':
            open(SearchFile,'a').write('search="%s",'%searchQuery)
        else: return False
        searchitems=re.compile('search="([^"]+?)",').findall(open(SearchFile,'r').read())
        rewriteSearchFile = False
        if searchitems.count(searchQuery) > 1:
            searchitems.remove(searchQuery)
            rewriteSearchFile = True
        if len(searchitems)>=10:
            searchitems.remove(searchitems[0])
            rewriteSearchFile = True
        if rewriteSearchFile:   
            os.remove(SearchFile)
            for searchitem in searchitems:
                try: open(SearchFile,'a').write('search="%s",'%searchitem)
                except: pass
    return searchQuery

def supportedHost(host):
    if 'ul' == host: host = 'uploaded'
    return host.lower() in getHostList()
######################################################################## Live Stream do Regex ############################################################
def doRegex(murl):
    #rname=rname.replace('><','').replace('>','').replace('<','')
    import urllib2
    url=re.compile('([^<]+)<regex>',re.DOTALL).findall(murl)[0]
    doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
    for k in doRegexs:
        if k in murl:
            regex=re.compile('<name>'+k+'</name><expres>(.+?)</expres><page>(.+?)</page><referer>(.+?)</referer></regex>',re.DOTALL).search(murl)
            referer=regex.group(3)
            if referer=='':
                referer=regex.group(2)
            req = urllib2.Request(regex.group(2))
            req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
            req.add_header('Referer',referer)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\/','/')
            r=re.compile(regex.group(1),re.DOTALL).findall(link)[0]
            url = url.replace("$doregex[" + k + "]", r)
   
    return url
    
################################################################################ AutoView ##########################################################################################################

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

def GETMETAT(mname,genre,fan,thumb,plot='',imdb='',tmdb=''):
    originalName=mname
    if selfAddon.getSetting("meta-view") == "true":
        setGrab()
        mname = re.sub(r'\[COLOR red\]\(?(\d{4})\)?\[/COLOR\]',r'\1',mname)
        mname = removeColoredText(mname)
        mname = mname.replace(' EXTENDED and UNRATED','').replace('Webrip','').replace('MaxPowers','').replace('720p','').replace('1080p','').replace('TS','').replace('HD','').replace('R6','').replace('H.M.','').replace('HackerMil','').replace('(','').replace(')','').replace('[','').replace(']','')
        mname = mname.replace(' Extended Cut','').replace('Awards Screener','')
        mname = re.sub('Cam(?![A-Za-z])','',mname)
        mname = re.sub('(?i)3-?d h-?sbs','',mname)
        mname = mname.strip()
        if re.findall('\s\d{4}',mname):
            r = re.split('\s\d{4}',mname,re.DOTALL)
            name = r[0]
            year = re.findall('\s(\d{4})\s',mname + " ")
            if year: year = year[0]
            else: year=''
        else:
            name=mname
            year=''
        name = name.decode("ascii", "ignore")
        meta = grab.get_meta('movie',name,imdb,tmdb,year)# first is Type/movie or tvshow, name of show,tvdb id,imdb id,string of year,unwatched = 6/watched  = 7
        if not meta['year']:
            name  = re.sub(':.*','',name)
            meta = grab.get_meta('movie',name,imdb,tmdb,year)
        print "Movie mode: %s"%name
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
          'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'overlay':meta['overlay'],
          'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year'],
          'imdb_id' : meta['imdb_id']}
        if infoLabels['genre']=='':
            infoLabels['genre']=genre
        if infoLabels['cover_url']=='':
            infoLabels['cover_url']=thumb
        if infoLabels['backdrop_url']=='':
            if fan=='': fan=fanartimage
            else: fan=fan
            infoLabels['backdrop_url']=fan
        if meta['overlay'] == 7: infoLabels['playcount'] = 1
        else: infoLabels['playcount'] = 0
        if infoLabels['cover_url']=='':
            thumb=art+'/vidicon.png'
            infoLabels['cover_url']=thumb
        #if int(year+'0'):
        #    infoLabels['year']=year 
        infoLabels['metaName']=infoLabels['title']
        infoLabels['title']=originalName
        if infoLabels['plot']=='': infoLabels['plot']=plot
        else: infoLabels['plot'] = infoLabels['plot'] + formatCast(infoLabels['cast'])
    else:
        if thumb=='': thumb=art+'/vidicon.png'
        if fan=='': fan=fanartimage
        else: fan=fan
        infoLabels = {'title': mname,'metaName': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': '','plot': '','genre': genre,'imdb_id': '','tmdb_id':''}
    return infoLabels

################################################################################ TV Shows Metahandler ##########################################################################################################

def GETMETAEpiT(mname,thumb,desc):
        originalName=mname
        mname = removeColoredText(mname)
        if selfAddon.getSetting("meta-view-tv") == "true":
                setGrab()
                mname = mname.replace('New Episode','').replace('Main Event','').replace('New Episodes','')
                mname = mname.strip()
                r = re.findall('(.+?)\ss(\d+)e(\d+)\s',mname + " ",re.I)
                if not r: r = re.findall('(.+?)\sseason\s(\d+)\sepisode\s(\d+)\s',mname + " ",re.I)
                if not r: r = re.findall('(.+?)\s(\d+)x(\d+)\s',mname + " ",re.I)
                if r:
                    for name,sea,epi in r:
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
                else:       
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
                        fan=fanartimage
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
                fan=fanartimage
                infoLabels = {'title': originalName,'metaName': mname,'cover_url': thumb,'backdrop_url': fan,'season': '','episode': '','year': '','plot': desc,'genre': '','imdb_id': ''}       
        
        return infoLabels
############################################################################### Playback resume/ mark as watched #################################################################################

def WatchedCallback():
        xbmc.log('%s: %s' % (selfAddon.addon.getAddonInfo('name'), 'Video completely watched.'), xbmc.LOGNOTICE)
        videotype='movies'
        setGrab()
        grab.change_watched(videotype, name, iconimage, season='', episode='', year='', watched=7)
        xbmc.executebuiltin("XBMC.Container.Refresh")

def WatchedCallbackwithParams(video_type, title, imdb_id, season, episode, year):
    print "worked"
    setGrab()
    grab.change_watched(video_type, title, imdb_id, season=season, episode=episode, year=year, watched=7)
    xbmc.executebuiltin("XBMC.Container.Refresh")

def ChangeWatched(imdb_id, videoType, name, season, episode, year='', watched='', refresh=False):
        setGrab()
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
    setGrab()
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
        xbmcgui.Dialog().ok('Refresh Results','No matches found')

def episode_refresh(vidname, imdb, season_num, episode_num):
    setGrab()
    grab.update_episode_meta(vidname, imdb, season_num, episode_num)
    xbmc.executebuiltin("XBMC.Container.Refresh")
################################################################################Trailers#######################################################################
def trailer(tmdbid):
    if tmdbid == '':
        xbmc.executebuiltin("XBMC.Notification(Sorry!,No Trailer Available For This Movie,3000)")
    else:
        import urllib2
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
    setGrab()
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

def SearchGoogle(search, site):
    from xgoogle.search import GoogleSearch
    gs = GoogleSearch(''+search+' '+site)
    gs.results_per_page = 25
    gs.page = 0
    try:
        results = gs.get_results()
    except Exception, e:
        print '***** Error: %s' % e
        return None
    return results
############################################################################### Resolvers ############################################################################################
def resolve_url(url,filename = False):
    import resolvers
    return resolvers.resolve_url(url,filename)
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

def geturl(murl):
        link=OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('<a class="myButton" href="(.+?)">Click Here to Play</a>').findall(link)
        if len(match)==0:
                match=re.compile('<a class="myButton" href="(.+?)">Click Here to Play Part1</a><a class="myButton" href="(.+?)">Click Here to Play Part2</a>').findall(link)
                return match[0]
        else:
                return match[0]

def resolveDownloadLinks(url):
    if re.search('watchseries.lt',url):
        match=re.compile('(.+?)xocx(.+?)xocx').findall(url)
        for hurl, durl in match:
            url=geturl('http://watchseries.lt'+hurl)
    elif re.search('iwatchonline',url):
        name=name.split('[COLOR red]')[0]
        name=name.replace('/','').replace('.','')
        url=GetUrliW(url)
    elif re.search('Filmesonline2',url):
        from resources.libs import Filmesonline2
        url = Filmesonline2.resolveM25URL(url)
    elif url.startswith('ice'):
        from resources.libs.movies_tv import icefilms
        url = url.lstrip('ice')
        url = eval(urllib.unquote(url))
        url = icefilms.resolveIceLink(url)
    elif 'mobapps.cc' in url or 'vk.com' in url:
        from resources.libs.plugins import mbox
        url = mbox.resolveMBLink(url)
    elif 'noobroom' in url:
        from resources.libs.movies_tv import starplay
        url = starplay.find_noobroom_video_url(url)
    return url

def Download_Source(name,url):
    originalName=name
    url = resolveDownloadLinks(url)
    name=removeColoredText(name)
    name=name.replace('/','').replace('\\','').replace(':','').replace('|','')      
    name=re.sub(r'[^\w]', ' ', name)
    name=name.split(' [')[0]
    name=name.split('[')[0]
    name=name.split(' /')[0]
    name=name.split('/')[0]

    stream_url = resolve_url(url)    
    if stream_url:
        print stream_url
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,2000)")
        if os.path.exists(downloadPath):
            if re.search("flv",stream_url):name += '.flv'
            elif re.search("mkv",stream_url): name += '.mkv'
            elif re.search("mp4",stream_url): name += '.mp4'
            elif re.search("avi",stream_url): name += '.avi'
            elif re.search("divx",stream_url): name += '.divx'
            else: name += '.mp4'
            mypath=os.path.join(downloadPath,name)
            if os.path.isfile(mypath):
                xbmc.executebuiltin("XBMC.Notification(Download Alert!,The video you are trying to download already exists!,8000)")
            else:
                name=name.replace(' ','')
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
                except:  pass 
        #only handle StopDownloading (from cancel), ContentTooShort (from urlretrieve), and OS (from the race condition); let other exceptions bubble 
        if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): 
            return False 
        else: raise 
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
    
    script = os.path.join( filmesonline2path, 'resources', 'libs', "DownloadInBackground.py" )
    xbmc.executebuiltin( "RunScript(%s, %s, %s, %s, %s, %s)" % ( script, q_url, q_dest, q_vidname,q_vidOname, str(notifyValues[NotifyPercent]) ) )
    return True
 
def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Kb/s ' % kbps_speed 
            e += 'ETA: %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close() 
            raise StopDownloading('Stopped Downloading')

def jDownloader(murl):
    url = resolveDownloadLinks(murl)
    print "Downloading "+murl+" via jDownlaoder"
    cmd = 'plugin://plugin.program.jdownloader/?action=addlink&url='+murl
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

def addDirX(name,url,mode,iconimage,plot='',fanart='',dur=0,genre='',year='',imdb='',tmdb='',isFolder=True,searchMeta=False,addToFavs=True,
            id=None,fav_t='',fav_addon_t='',fav_sub_t='',metaType='Movies',menuItemPos=None,menuItems=None,down=False,replaceItems=True):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
    if 'http://api.video.mail.ru/videos/embed/' in url or mode==364:
        name=name.decode('windows-1251')
        plot=plot.decode('windows-1251')
    if searchMeta:
        if metaType == 'TV':
            infoLabels = GETMETAEpiT(name,iconimage,plot)
        else:
            infoLabels = GETMETAT(name,genre,fanart,iconimage,plot,imdb,tmdb)
        iconimage = infoLabels['cover_url']
        fanart = infoLabels['backdrop_url']
        plot = infoLabels['plot']
    if not fanart: fanart=fanartimage
    if not iconimage: iconimage=art+'/vidicon.png'
    if not plot: plot='Sorry description not available'
    plot=plot.replace(",",'.')
    Commands = []
    if down:
        sysurl = urllib.quote_plus(url)
        sysname= urllib.quote_plus(name)
        Commands.append(('Direct Download', 'XBMC.RunPlugin(%s?mode=190&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
        Commands.append(('Download with jDownloader', 'XBMC.RunPlugin(%s?mode=776&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
  
    if searchMeta:
        if metaType == 'TV' and selfAddon.getSetting("meta-view-tv") == "true":
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            cname = infoLabels['title']
            cname = cname.decode('ascii', 'ignore')
            cname = urllib.quote_plus(cname)
            sea = infoLabels['season']
            epi = infoLabels['episode']
            imdb_id = infoLabels['imdb_id']
            if imdb_id != '':
                if infoLabels['overlay'] == 6: watched_mark = 'Mark as Watched'
                else: watched_mark = 'Mark as Unwatched'
                Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=779&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, 'episode', imdb_id,sea,epi)))
            Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=780&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], cname, 'episode',imdb_id,sea,epi)))
        elif metaType == 'Movies' and selfAddon.getSetting("meta-view") == "true":
            xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
            if id != None: xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PLAYLIST_ORDER )
            else: xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_TITLE )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )
            cname=urllib.quote_plus(infoLabels['metaName'])
            imdb_id = infoLabels['imdb_id']
            if infoLabels['overlay'] == 6: watched_mark = 'Mark as Watched'
            else: watched_mark = 'Mark as Unwatched'
            Commands.append((watched_mark, 'XBMC.RunPlugin(%s?mode=777&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, 'movie',imdb_id)))
            Commands.append(('Play Trailer','XBMC.RunPlugin(%s?mode=782&name=%s&url=%s&iconimage=%s)'% (sys.argv[0],cname,'_',imdb_id)))
            Commands.append(('Refresh Metadata', 'XBMC.RunPlugin(%s?mode=778&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], cname, 'movie',imdb_id)))
    else:
        infoLabels={ "Title": name, "Plot": plot, "Duration": dur, "Year": year ,"Genre": genre,"OriginalTitle" : removeColoredText(name) }
    if id != None: infoLabels["count"] = id
    Commands.append(('[B][COLOR=FF67cc33]Filmesonline2[/COLOR] Settings[/B]','XBMC.RunScript('+xbmc.translatePath(filmesonline2path + '/resources/libs/settings.py')+')'))
    if menuItemPos != None:
        for mi in reversed(menuItems):
            Commands.insert(menuItemPos,mi)
    
    liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
    liz.addContextMenuItems( Commands, replaceItems=False)
    liz.setInfo( type="Video", infoLabels=infoLabels )
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)

def addDirT(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,fav_t='TV',fav_addon_t='TV Show',fav_sub_t='Shows')

def addPlayT(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=False,fav_t='TV',fav_addon_t='TV Show',fav_sub_t='Shows')

def addDirTE(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,searchMeta=1,metaType='TV',fav_t='TV',fav_addon_t='TV Episode',fav_sub_t='Episodes')
    
def addPlayTE(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,searchMeta=1,metaType='TV',fav_t='TV',fav_addon_t='TV Episode',fav_sub_t='Episodes')

def addDirM(name,url,mode,iconimage,plot,fanart,dur,genre,year,imdb=''):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,imdb,searchMeta=1,fav_t='Movies',fav_addon_t='Movie')

def addPlayM(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,searchMeta=1,fav_t='Movies',fav_addon_t='Movie')
    
def addDirMs(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,fav_t='Misc.',fav_addon_t='Misc.')

def addPlayMs(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,fav_t='Misc.',fav_addon_t='Misc.')

def addDirL(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,fav_t='Live',fav_addon_t='Live')

def addPlayL(name,url,mode,iconimage,plot,fanart,dur,genre,year,secName='',secIcon=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
    surl=urllib.quote_plus(u)
    dname=removeColorTags(name)
    mi=[('Add to [COLOR=FFb151ef]Dixie[/COLOR]', 'XBMC.RunPlugin(%s?mode=1501&plot=%s&name=%s&url=%s&iconimage=%s)' % (sys.argv[0] ,secName,dname,surl, secIcon))]
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,fav_t='Live',fav_addon_t='Live',menuItemPos=2,menuItems=mi)

def addPlayc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,addToFavs=0)
    
def addDirb(name,url,mode,iconimage,fanart):
    return addDirX(name,url,mode,iconimage,'',fanart,addToFavs=0)

def addDirc(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,addToFavs=0)

def addDirXml(name,url,mode,iconimage,plot,fanart,dur,genre,year):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)
        liz=xbmcgui.ListItem(name, iconImage=art+'/xmlplaylist.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=fanartimage
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
        liz=xbmcgui.ListItem(name, iconImage=art+'/folder.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        if fanart == '':
            fanart=fanartimage
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
    liz=xbmcgui.ListItem(name, iconImage=art+'/link.png', thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', fanartimage)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,plot='',fanart=''):
    return addDirX(name,url,mode,iconimage,plot,fanart,addToFavs=0,replaceItems=False)

def addDirHome(name,url,mode,iconimage):
    return addDirX(name,url,mode,iconimage,addToFavs=0)

def addDirFIX(name,url,mode,iconimage,location,path):
    contextMenuItems = []
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&location="+urllib.quote_plus(location)+"&path="+urllib.quote_plus(path)
    liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', fanartimage)
    contextMenuItems.append(('Watch History','XBMC.Container.Update(%s?name=None&mode=222&url=None&iconimage=None)'% (sys.argv[0])))
    contextMenuItems.append(("My Fav's",'XBMC.Container.Update(%s?name=None&mode=639&url=None&iconimage=None)'% (sys.argv[0])))
    liz.addContextMenuItems(contextMenuItems, replaceItems=False)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def addDown2(name,url,mode,iconimage,fanart,id=None):
    return addDirX(name,url,mode,iconimage,'',fanart,isFolder=0,addToFavs=0,id=id,down=1)

def addDown3(name,url,mode,iconimage,fanart,id=None):
    return addDirX(name,url,mode,iconimage,'',fanart,isFolder=0,searchMeta=1,fav_t='Movies',fav_addon_t='Movie',id=id,down=1)

def addDown4(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    f = '</sublink>' in url
    if re.search('(?i)\ss(\d+)e(\d+)',name) or re.search('(?i)Season(.+?)Episode',name):
        return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=f,searchMeta=1,metaType='TV',
                       fav_t='TV',fav_addon_t='TV Episode',fav_sub_t='Episodes',down=not f)
    else:
        return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=f,searchMeta=1,
                       fav_t='Movies',fav_addon_t='Movie',down=not f)

def addInfo(name,url,mode,iconimage,genre,year):
#     mi = [('Search Filmesonline2','XBMC.Container.Update(%s?mode=4&url=%s)'% (sys.argv[0],'###'))]
#     return addDirX(name,url,mode,iconimage,'','','',genre,year,searchMeta=1,fav_t='Movies',fav_addon_t='Filmesonline2',menuItemPos=0,menuItems=mi)
    return addDirX(name,url,mode,iconimage,'','','',genre,year,searchMeta=1,fav_t='Movies',fav_addon_t='Filmesonline2')

def addDirIWO(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,searchMeta=1,fav_t='Movies',fav_addon_t='iWatchOnline')
    
def addDLog(name,url,mode,iconimage,plot,fanart,dur,genre,year):
    mi=[("[B][COLOR red]Remove[/COLOR][/B]",'XBMC.RunPlugin(%s?mode=243&name=%s&url=%s)'% (sys.argv[0],name,url))]
    if re.search('(?i)\ss(\d+)e(\d+)',name) or re.search('(?i)Season(.+?)Episode',name):
        return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,searchMeta=1,metaType='TV',addToFavs=0,menuItemPos=0,menuItems=mi)
    else: return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0,searchMeta=1,addToFavs=0,menuItemPos=0,menuItems=mi)

def addSpecial(name,url,mode,iconimage):
    liz=xbmcgui.ListItem(name,iconImage="",thumbnailImage = iconimage)
    liz.setProperty('fanart_image', fanartimage)
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)

def addSearchDir(name,url, mode,iconimage):
    #thumbnail = 'DefaultPlaylist.png'
    u         = sys.argv[0]+"?url="+urllib.quote_plus(url) + "?mode=" + str(mode)        
    liz       = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fanartimage)
    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)
