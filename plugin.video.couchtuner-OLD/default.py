#-*- coding: utf-8 -*-
import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,urllib2,re,string,os,time,threading

try:
    from resources.libs import main,settings    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.couchtuner/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]CouchTuner Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]Twitter @ Kasik04a[/COLOR] to Fix')
    xbmc.log('CouchTuner ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)
    
#CouchTuner by Kasik04a


addon_id = 'plugin.video.couchtuner'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
base_url = 'http://www.couchtuner.eu'

################################################################################ Directories ##########################################################################################################
UpdatePath=os.path.join(main.datapath,'Update')
try: os.makedirs(UpdatePath)
except: pass
CachePath=os.path.join(main.datapath,'Cache')
try: os.makedirs(CachePath)
except: pass
CookiesPath=os.path.join(main.datapath,'Cookies')
try: os.makedirs(CookiesPath)
except: pass
TempPath=os.path.join(main.datapath,'Temp')
try: os.makedirs(TempPath)
except: pass

def MAIN():
    
    main.addDir('New Release','http://www.couchtuner.eu/',1,art+'/New.png')
    main.addDir('TV A-Z Index ','http://www.couchtuner.eu/tv-lists/',7,art+'/showlist.png')
    main.addDir('Search','http://www.couchtuner.eu/?s=',110,art+'/search.png')

########################################################################################################################################################################
def AtoZ():
    main.addDir('0-9','http://www.couchtuner.eu/tv-list/#',8,art+'/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,'http://www.couchtuner.eu/tv-list/#'+i.upper()+'/',8,art+'/'+i.lower()+'.png')


def AZLIST(url):
    link=main.OPEN_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;',' - ')
    #match=re.compile('<li><a href="([^"]*)" title="[^"]*">[%s]([^"]*)</a>'% name).findall(link)
    match=re.compile('<li><strong><a href="([^<]+)">[%s]([^<]+)</a></strong></li>'% name).findall(link)
    for url,title in match:
        title=name+title
        #url = url.replace('watch-','watch/')+'/'
        main.addInfo(title,url,9,'','','')




def Episodes(url):
    link=main.OPEN_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;',' - ')
    match=re.compile('<li><strong><a href="([^<]+)">([^<]+)</a>([^<]+)</strong>').findall(link)
    for url,title,title1 in match:
        title=title+' ' + title1
        #url = url.replace('watch-','watch/')+'/'
        main.addInfo(title,url,10,'','','')
        

def FirstLinks(name,url):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('Watch it here :</span>.+?<a href="([^"]*?)">').findall(link)
    if match:
     for url in match:
       Linkz(name,url)
    else:
      match2=re.compile('Watch it here :.+?</span><a href="([^"]*?)">').findall(link)
      for url in match2:
       Linkz(name,url)   
        

def Linkz(name,url):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    vodlocker=re.compile('"http://vodlocker.com/embed-([^"]*?)-.+?.html"').findall(link)
    for url in vodlocker:
        url='http://vodlocker.com/'+url    
        host='vodlocker'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')    
    played=re.compile('http://played.to/embed-([^"]*?)-.+?.html').findall(link)
    for url in played:
        url='http://played.to/'+url    
        host='played'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    thevideo=re.compile('"http://www.thevideo.me/embed-([^"]*?)-.+?.html').findall(link)
    for url in thevideo:
        url='http://www.thevideo.me/'+url    
        host='thevideo'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    vidbull=re.compile('http://vidbull.com/embed-zvfcf9rs2kid-540x318.html').findall(link)
    for url in vidbull:
        url='http://vidbull.com/'+url    
        host='vidbull'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    youwatch=re.compile('http://youwatch.org/embed-([^"]*?)-.+?.html').findall(link)
    for url in youwatch:
        url='http://youwatch.org/'+url    
        host='youwatch'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    vidto=re.compile('"http://vidto.me/embed-([^"]*?)-.+?.html"').findall(link)
    for url in vidto:
        url='http://vidto.me/'+url    
        host='vidto'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')     
    vshare=re.compile('http://vshare.eu/embed-([^"]*?)-.+?.html').findall(link)
    for url in vshare:
        url='http://vshare.eu/'+url    
        host='vshare'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')     
    vidspot=re.compile('"http://vidspot.net/embed-([^"]*?).html').findall(link)
    for url in vidspot:
        url='http://vidspot.net/'+url    
        host='vidspot'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    allmyvideos=re.compile('"http://allmyvideos.net/embed-([^"]*?)-.+?.html"').findall(link)
    for url in allmyvideos:
        url='http://allmyvideos.net/'+url    
        host='allmyvideos'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    vkmobile=re.compile('http://videoapi.my.mail.ru/videos/embed/mail/geek.tv/_myvideo/([^"]*?).html').findall(link)
    for url in vkmobile:
        url='http://videoapi.my.mail.ru/videos/embed/mail/geek.tv/_myvideo/'+url    
        host='VK-Mobile'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
    fhoot=re.compile('http://filehoot.com/embed-([^"]*?)-.+?.html').findall(link)
    for url in fhoot:
        url='http://filehoot.com/'+url    
        host='filehoot'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')     
    exashare=re.compile('"http://www.exashare.com/embed-([^"]*?)-.+?.html"').findall(link)
    for url in exashare:
        url='http://www.exashare.com/'+url    
        host='exashare'    
        main.addDown2(name.strip()+" [COLOR red]"+host.upper()+"[/COLOR]",str(url),2,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')     

    






def Episodes2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;','-').replace('&#8217;',"'").replace('season-','s').replace('episode-','e').replace('#038;','')
        response.close()
		
        match=re.compile('<a href="http://www.couchtuner.ch/([^"]*)/">([^"]*)</a>([^"]*)</strong>').findall(link)
        for url,episode,title in match:
                title='[COLOR blue]'+episode+'[/COLOR]'+ ' - ' +'[COLOR red]'+title+'[/COLOR]'
                url = 'http://www.zzstream.li/'+url+'.html'
                print ""+url
                main.addDir(title,url,5,'')
        match=re.compile('<a href="http://www.zzstream.li/([^"]*)" rel="nofollow">([^"]*)</a>([^"]*)</strong>').findall(link)
        for url,episode,title in match:
                title='[COLOR blue]'+episode+'[/COLOR]'+ ' - ' +'[COLOR red]'+title+'[/COLOR]'
                url='http://www.zzstream.li/'+url
                print ""+url
                main.addDir(title,url,5,'')             


####################################################################################################################################################
def getListFile(url, path, excepturl = None ):
    link = ''
    t = threading.Thread(target=setListFile,args=(url,path,excepturl))
    t.start()
    if not os.path.exists(path): t.join()
    if os.path.exists(path):
        try: link = open(path).read()
        except: pass
    return link

def setListFile(url, path, excepturl = None):
    content = None
    try: content=main.OPENURL(url, verbose=False)
    except:
        if excepturl: content=main.OPENURL(excepturl, verbose=False)
    if content:
        try: open(path,'w+').write(content)
        except: pass
    return


################################################################################ XBMCHUB Repo & Hub Maintenance Installer ##########################################################################################################
hubpath = xbmc.translatePath(os.path.join('special://home/addons', ''))
maintenance=os.path.join(hubpath, 'plugin.video.hubmaintenance')

def downloadFileWithDialog(url,dest):
    try:
        dp = xbmcgui.DialogProgress()
        dp.create("channel_cut","Downloading & Copying File",'')
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: main._pbhook(nb,bs,fs,dp,time.time()))
    except Exception, e:
        dialog = xbmcgui.Dialog()
        main.ErrorReport(e)
        dialog.ok("channel_cut", "Report the error below at " + main.supportsite, str(e), "We will try our best to help you")

def UploadLog():
    from resources.fixes import addon
    addon.LogUploader()

################################################################################ XBMCHUB POPUP ##########################################################################################################
class HUB( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/theme.ogg'%selfAddon.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()
        if controlID == 7:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()
        
def pop():
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUB('hub1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    if xbmc.getCondVisibility('system.platform.android'):
        popup = HUB('hub1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    else:
        popup = HUB('hub.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    popup.doModal()
    del popup

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
            except: text=anounce
            self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
            return
    TextBox()
############################################################################################################################################
###################################################################################

def addDirB(name,url,mode,iconimage,types):
        ok=True
        type = types
        if type != None:
                infoLabels = GRABMETA(name,types)
        else: infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img= iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)

        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

######################


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
        return ok

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
        
################################################################################ Modes ##########################################################################################################


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
              
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
plot=None
genre=None
title=None
season=None
episode=None
location=None
path=None

try: name=urllib.unquote_plus(params["name"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: mode=int(params["mode"])
except: pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
    iconimage = iconimage.replace(' ','%20')
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
    fanart = fanart.replace(' ','%20')
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: title=urllib.unquote_plus(params["title"])
except: pass
try: episode=int(params["episode"])
except: pass
try: season=int(params["season"])
except: pass
try: location=urllib.unquote_plus(params["location"])
except: pass
try: path=urllib.unquote_plus(params["path"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
    MAIN()
    main.VIEWSB()

elif mode==1:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.NewRelease(url)

elif mode==2:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.PLAY(name,url)

elif mode==3:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.SEARCH(url)
    
elif mode==4:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.Searchhistory()

elif mode==5:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.LINK(name,url)


elif mode==7:
    AtoZ()

elif mode==8:
    AZLIST(url)

elif mode==9:
    Episodes(url)

elif mode==10:
    FirstLinks(name,url)


elif mode==11:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.Seasons(url)
    


elif mode==45:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.TVLINK(name,url)







    

elif mode==100:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.VIDEOLINKS(name,url) 

elif mode==110:
        from resources.libs import couchtuner
        print ""+url
        couchtuner.Searchhistory()
        
elif mode==120:
        from resources.libs import couchtuner
        print ""+url
        couchtuner.SEARCH(url)
        
elif mode==128:
        main.Clearhistory(url)
        
elif mode==130:
        from resources.libs import couchtuner
        print ""+url
        couchtuner.Searchhistorytv()

        
        
    
elif mode==190:
    print ""+url
    main.Download_Source(name,url)


  

elif mode == 776:
    main.jDownloader(url) 


xbmcplugin.endOfDirectory(int(sys.argv[1]))
