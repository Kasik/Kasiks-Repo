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
base_url = 'DELETE'

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
    
    main.addDir('New Release','http://couchtuner2.to/latest-episodes',1,art+'/New.png')
    main.addDir('TV A-Z Index ','http://couchtuner2.to/tv',7,art+'/showlist.png')
    main.addDir('Search','http://couchtuner2.to/search?q=',110,art+'/search.png')

########################################################################################################################################################################

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
    from resources.libs import couchtuner
    print " " + url
    couchtuner.AtoZ()

elif mode==8:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.AZLIST(name,url)

elif mode==9:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.SEASONS(name,url,index=False)

elif mode==10:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.EPISODES(name,url,index=False)    


elif mode==11:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.Seasons(url)
    


elif mode==20:
    from resources.libs import couchtuner
    print " " + url
    couchtuner.resolveURL(name,url)

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
