#-*- coding: utf-8 -*-
import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading

try:
    from resources.libs import main,settings    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.megabox/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]Megabox Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]Twitter @ Kasik04a[/COLOR] to Fix')
    xbmc.log('Megabox ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)
    
#Megabox/Megashare - by Kasik04a 2014.

#################### Set Environment ######################
ENV = "Prod"  # "Prod" or "Dev"
###########################################################
MainUrl='http://megashare.li/'
addon_id = 'plugin.video.megabox'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art

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


def MegaBox(index=False):
    main.addDirHome('Search Movies','http://megashare.li/',21,art+'/searchmovies.jpg')
    main.addDirHome('Latest Added','http://megashare.li/?sort=latest-added',1,art+'/latest.jpg')
    main.addDirHome('New Releases','http://megashare.li/?sort=release',1,art+'/newr.jpg')
    main.addDirHome('Popular Movies','http://megashare.li/?sort=views',1,art+'/popular.jpg')
    main.addDirHome('Movies by Ratings','http://megashare.li/?sort=ratings',1,art+'/rating.jpg')
    main.addDirHome('Featured Movies','http://megashare.li/?sort=featured',1,art+'/featured.jpg')
    main.addDirHome('Movies By Year','http://megashare.li/?sort=year',6,art+'/years.jpg')
    main.addDirHome('Genres','http://megashare.li/',5,art+'/genres.jpg')    
    #main.addDirHome('Coming Soon','http://megashare.li/?sort=coming-soon',1,art+'/soon.jpg')
    main.addDirHome('TV','http://megashare.li/?tv',10,art+'/tv.jpg')
    HideXXX = selfAddon.getSetting('Hide-XXX')
    if HideXXX == 'false':
                main.addDirHome('XXX Movies',MainUrl,69,art+'/adult.jpg')    
    #main.addPlayc('Need Help?','URL',100,art+'/help.png','','','','','')
    #main.addPlayc('Upload Log','URL',156,art+'/loguploader.png','','','','','')
    #main.addPlayc('Megabox Settings','URL',1999,art+'/.png','','','','','')

        
    
def TV():
    main.ClearDir(TempPath)
    main.addDirHome('Search Tv Shows','http://megashare.li/',16,art+'/searchmovies.jpg')
    main.addDir('Latest Episodes','http://megashare.li/?sort=latest-added&tv',11,art+'/.png')
    main.addDir('New Releases','http://megashare.li/?sort=release&tv',11,art+'/.png')
    main.addDir('Popular Tv Shows','http://megashare.li/?sort=views&tv',11,art+'/.png')
    main.addDir('Tv Shows by Rating','http://megashare.li/?sort=ratings&tv',11,art+'/.png')
    main.addDir('Featured Tv Shows','http://megashare.li/?sort=featured&tv',11,art+'/.png')
    main.addDir('TV Genres','http://megashare.li/?tv',12,art+'/.png')
    
    


def ADULT():
    main.addDir('Latest Added','http://megabox.li/?xxx',70,art+'/latest.jpg')
    main.addDir('Rating','http://megabox.li/?sort=ratings&xxx',70,art+'/rating.jpg')
    main.addDir('Popular','http://megabox.li/?sort=views&xxx',70,art+'/popular.jpg')
    main.addDir('Random','http://megabox.li/?sort=random&xxx',70,art+'/random.jpg')
    main.addDir('Search','http://megabox.li/index.php?search=',75,art+'/searchxxx.jpg')
    main.addDir('A-Z','http://megabox.li/?xxx',76,art+'/az.jpg')

        

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

def cacheSideReel():
    user = selfAddon.getSetting('srusername')
    passw = selfAddon.getSetting('srpassword')
    cached_path = os.path.join(CachePath, 'Sidereel')
    import datetime
    if (user and passw) and (not os.path.exists(cached_path) or time.mktime(datetime.date.today().timetuple()) > os.stat(cached_path).st_mtime):
        from resources.libs.movies_tv import sidereel
        sidereel.MAINSIDE(True)
        
def cacheTrakt():
    user = selfAddon.getSetting('trusername')
    passw = selfAddon.getSetting('trpassword')
    cached_path = os.path.join(CachePath, 'Trakt')
    import datetime
    if (user and passw) and (not os.path.exists(cached_path) or time.mktime(datetime.date.today().timetuple()) > os.stat(cached_path).st_mtime):
        from resources.libs.movies_tv import trakt
        trakt.showList(True)

############################################################################### TV GUIDE DIXIE ###################################################################################################

def openMGuide():
   try:
       dialog = xbmcgui.DialogProgress()
       dialog.create('Pleat Wait!', 'Opening TV Guide Dixie...')
       dialog.update(0)
       dixie = xbmcaddon.Addon('script.tvguidedixie')
       path  = dixie.getAddonInfo('path') 
       sys.path.insert(0, os.path.join(path, ''))
       xbmc.executebuiltin('ActivateWindow(HOME)')
       dialog.update(33)
       dixie.setSetting('mashmode', 'true')
       import gui
       dialog.update(66)
       w = gui.TVGuide()
       dialog.update(100)
       dialog.close()
       w.doModal()
       del w
       

       cmd = 'AlarmClock(%s,RunAddon(%s),%d,True)' % ('Restart', addon_id, 0)
       
       xbmc.executebuiltin(cmd)
   except Exception, e:
       #print str(e)
       pass
       


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
#######################################################################################

class HUBx( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                   
    def onInit( self ):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/theme.ogg'%selfAddon.getAddonInfo('path'))# Music
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
            
    def onFocus( self, controlID ): pass

    def onClick( self, controlID ): 
        if controlID == 12 or controlID == 7:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.megabox/resources/skins/DefaultSkin','media'))
        popimage=os.path.join(path, 'tempimage.jpg')
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()
        os.remove(popimage)
        
def popVIP(image):
    path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.megabox/resources/skins/DefaultSkin','media'))
    popimage=os.path.join(path, 'tempimage.jpg')
    main.downloadFile(image,popimage)
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUBx('pop1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'),)
    if xbmc.getCondVisibility('system.platform.android'):
        popup = HUBx('pop1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    else:
        popup = HUBx('pop.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    popup.doModal()
    del popup
################################################################################ Favorites Function##############################################################################################################
def getFavorites(section_title = None):
    from resources.universal import favorites
    fav = favorites.Favorites(addon_id, sys.argv)
    
    if(section_title):
        fav_items = fav.get_my_favorites(section_title=section_title, item_mode='addon')
    else:
        fav_items = fav.get_my_favorites(item_mode='addon')
    
    if len(fav_items) > 0:
    
        for fav_item in fav_items:
            if (fav_item['isfolder'] == 'false'):
                if (fav_item['section_addon_title'] == "iWatchOnline Fav's" or 
                    fav_item['section_addon_title'] == "Movie Fav's"):
                    main.addPlayM(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "TV Show Fav's"):
                    main.addPlayT(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "TV Episode Fav's"):
                    main.addPlayTE(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Misc. Fav's"):
                    main.addPlayMs(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Live Fav's"):
                    main.addPlayL(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "megabox Fav's"):
                    main.addInfo(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('genre',''), fav_item['infolabels'].get('year',''))
            else:
                if (fav_item['section_addon_title'] == "iWatchOnline Fav's" or 
                    fav_item['section_addon_title'] == "Movie Fav's"):
                    main.addDirM(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "TV Show Fav's"):
                    main.addDirT(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "TV Episode Fav's"):
                    main.addDirTE(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Misc. Fav's"):
                    main.addDirMs(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "Live Fav's"):
                    main.addDirL(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                        fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                        fav_item['infolabels'].get('year',''))
                elif (fav_item['section_addon_title'] == "megabox Fav's"):
                    main.addInfo(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                        fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                        fav_item['infolabels'].get('genre',''), fav_item['infolabels'].get('year',''))
    else:
            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]Megabox[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
    return
    
def ListglobalFavALL():
    getFavorites()
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavM25():
    getFavorites("megabox Fav's")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    
def ListglobalFavIWO():
    getFavorites("iWatchOnline Fav's")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavT():
    getFavorites("TV Show Fav's")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    
def ListglobalFavTE():
    getFavorites("TV Episode Fav's")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavM():
    getFavorites("megabox Fav's")
    getFavorites("Movie Fav's")
    getFavorites("iWatchOnline Fav's")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavMs():
    getFavorites("Misc. Fav's")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavL():
    getFavorites("Live Fav's")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    
################################################################################ Histroy ##########################################################################################################
def WHClear(url):
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('MashUp Watch History', 'Are you sure you want to clear your','watch history, you can not restore','once you press yes','No', 'Yes')
    if ret:
        os.remove(url)
        xbmc.executebuiltin("XBMC.Container.Refresh")


def History():
    whprofile = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
    whdb=os.path.join(whprofile,'Universal','watch_history.db')
    if  os.path.exists(whdb):
        main.addPlayc('Clear Watch History',whdb,414,art+'/cleahis.png','','','','','')
    from resources.universal import watchhistory
    wh = watchhistory.WatchHistory(addon_id)
    if selfAddon.getSetting("whistory") == "true":
        history_items = wh.get_my_watch_history()
        for item in history_items:
            item_title = item['title']
            item_url = item['url']
            item_image = item['image_url']
            item_fanart = item['fanart_url']
            item_infolabels = item['infolabels']
            item_isfolder = item['isfolder']
            if item_image =='':
                item_image= art+'/noimage.png'
            item_title=item_title.replace('[COLOR green]','[COLOR=FF67cc33]')
            main.addLink(item_title,item_url,item_image)
    else:
        dialog = xbmcgui.Dialog()
        ok=dialog.ok('[B]Megabox History[/B]', 'Watch history is disabled' ,'To enable go to addon settings','and enable Watch History')
        history_items = wh.get_my_watch_history()
        for item in history_items:
            item_title = item['title']
            item_url = item['url']
            item_image = item['image_url']
            item_fanart = item['fanart_url']
            item_infolabels = item['infolabels']
            item_isfolder = item['isfolder']
            item_title=item_title.replace('[COLOR green]','[COLOR=FF67cc33]')
            main.addLink(item_title,item_url,item_image)
    
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
index=None

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
try: index=urllib.unquote_plus(params["index"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
    MegaBox()
       
    main.VIEWSB()        
   
elif mode==1:
    from resources.libs import megabox
    megabox.LISTMOVIES(url,index=index)

  
elif mode==5:
    from resources.libs import megabox
    print ""+url
    megabox.GENRES(url,index=index)

elif mode==6:
    from resources.libs import megabox
    print ""+url
    megabox.YEARS(url,index=index)
    


elif mode==10:
    TV()

elif mode==11:
    from resources.libs import megaboxtv
    print ""+url
    megaboxtv.TV(url)

elif mode==12:
    from resources.libs import megaboxtv
    print ""+url
    megaboxtv.TVGENRES(url,index=index)

elif mode==13:
    from resources.libs import megaboxtv
    print ""+url
    megaboxtv.TV(url)

elif mode==14:
    from resources.libs import megaboxtv
    print ""+url
    megaboxtv.TV(url)    


elif mode==15:
    from resources.libs import megabox
    print ""+url
    megabox.SEARCHTV(url,index=index)
    
elif mode==16:
    from resources.libs import megaboxtv
    print ""+url
    megaboxtv.SearchhistoryTV(index=index)



elif mode==17:
    from resources.libs import megabox
    print ""+url
    megabox.ADULTGENRE(url)



elif mode==20:
    from resources.libs import megabox
    print ""+url
    megabox.SEARCH(url,index=index)
    
elif mode==21:
    from resources.libs import megabox
    print ""+url
    megabox.Searchhistory(index=index)


elif mode==22:
    from resources.libs import megaboxtv
    print ""+url
    megaboxtv.Seasons(url,name)
elif mode==23:
    from resources.libs import megaboxtv
    print ""+url
    megaboxtv.Episodes(url,season)















elif mode==50:
    from resources.libs import megabox
    print ""+url
    megabox.GRABLINKS(url)


elif mode==51:
        from resources.libs import megabox
        megabox.GRABADULT(url)     

elif mode==52:
        from resources.libs import megaboxtv
        print ""+url
        megaboxtv.GRABTVLINKS(url)

####################### - ADULT - ######################################
elif mode==69:
        print ""+url
        ADULT()
        
elif mode==70:
        from resources.libs import megaxxx
        megaxxx.XXX(url)
        
elif mode==71:
        from resources.libs import megaxxx
        megaxxx.GRABXXX(url)

elif mode==72:
        from resources.libs import megaxxx
        megaxxx.PLAYXXX(name,url)

elif mode==73:
        from resources.libs import megaxxx
        megaxxx.Epornik1(url)

elif mode==74:
        from resources.libs import megaxxx
        megaxxx.Epornik2(url,name)

elif mode==75:
        from resources.libs import megaxxx
        megaxxx.SEARCHXXX(url)

elif mode==76:
        from resources.libs import megaxxx
        megaxxx.AZXXX()          

########################################################################



elif mode==90:
    from resources.libs import megabox
    print ""+url
    megabox.PLAY(name,url)

elif mode==91:
    from resources.libs import megabox
    print ""+url
    megabox.PLAYB(name,url)

    















elif mode==128:
        main.Clearhistory(url)


















elif mode==150:
        print ""+url
        main.Download_Source(name,url)

elif mode==222:
        print ""+url
        History()        


elif mode == 500:
        main.TRAILERSEARCH(url, name, iconimage)
elif mode == 776:
        main.jDownloader(url)   
elif mode == 777:
        main.ChangeWatched(iconimage, url, name, '', '')
elif mode == 779:
        main.ChangeWatched(iconimage, url, name, season, episode)        
elif mode == 780:
        main.episode_refresh(name, iconimage, season, episode)  
elif mode == 781:
    main.trailer(url)
elif mode == 782:
    main.TRAILERSEARCH(url, name, iconimage)




    
elif mode == 1998:
    if ENV is 'Prod':
        CheckForAutoUpdate(False)
    else:
        CheckForAutoUpdateDev(False)
elif mode == 1999:
    settings.openSettings()
elif mode == 2000:
    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
