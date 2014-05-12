#-*- coding: utf-8 -*-
import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading
from BeautifulSoup import MinimalSoup as BeautifulSoup
try:
    from resources.libs import main,settings    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.megabox/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]Megabox Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module to Fix')
    xbmc.log('Megabox ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)
reload(sys)
sys.setdefaultencoding( "UTF-8" )   
    
#Megabox - by Kasik 2013.

base_url ='http://megabox.li/'
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


def MAIN():
        
        main.addDirHome('Search Movies',base_url,100,art+'/searchmovies.jpg')
        main.addDirHome('New Releases',base_url + '?sort=release',1,art+'/newr.jpg')
        main.addDirHome('Latest Added',base_url + '?sort=latest-added',1,art+'/latest.jpg')
        main.addDirHome('Featured',base_url + '?sort=featured',1,art+'/featured.jpg')
        main.addDirHome('Ratings',base_url + '?sort=ratings',1,art+'/rating.jpg')
        main.addDirHome('Popular',base_url + '?sort=views',1,art+'/popular.jpg')
        main.addDirHome('2013 Movies',base_url + '?year=2013',1,art+'/2013.jpg')
        main.addDirHome('2012 Movies',base_url + '?year=2012',1,art+'/2012.jpg')
        main.addDirHome('Youtube Movies',base_url + '?sort=youtube-movies',50,art+'/youtubem.jpg')
        main.addDirHome('Coming Soon',base_url + '?sort=coming-soon',1,art+'/soon.jpg')
        main.addDirHome('Movie Genres',base_url,2,art+'/genres.jpg')
        main.addDirHome('TV SHOWS',base_url,9,art+'/tv.jpg')
        HideXXX = selfAddon.getSetting('Hide-XXX')
        if HideXXX == 'false':
                main.addDirHome('XXX',base_url,69,art+'/adult.jpg')
        main.VIEWSB()
                     
      

def MOVIEGENRE(url):
        main.addDir('Action',base_url +'?genre=action',1,art+'/action.jpg')
        HideAdult = selfAddon.getSetting('Hide-Adult')
        if HideAdult == 'false':
                main.addDir('Adult','http://megabox.li/accept_terms.php?genre=adult&accept=1',17,art+'/adultgenre.jpg')
        main.addDir('Animation',base_url +'?genre=animation',1,art+'/anim.jpg')
        main.addDir('Comedy',base_url +'?genre=comedy',1,art+'/comedy.jpg')
        main.addDir('Crime',base_url +'?genre=crime',1,art+'/crime.jpg')
        main.addDir('Documentary',base_url +'?genre=documentary',1,art+'/docs.jpg')
        main.addDir('Drama',base_url +'?genre=drama',1,art+'/drama.jpg')
        main.addDir('Family',base_url +'?genre=family',1,art+'/family.jpg')
        main.addDir('Horror',base_url +'?genre=horror',1,art+'/horror.jpg')
        main.addDir('Romance',base_url +'?genre=romance',1,art+'/romance.jpg')
        main.addDir('Sci-Fi',base_url +'?genre=sci-fi',1,art+'/scifi.jpg')
        main.addDir('Thriller',base_url +'?genre=thriller',1,art+'/thriller.jpg')
        main.VIEWSB()
        
####################################### TV SECTION #########################################################################################
   
def TV():
        main.addDir('Search Tv Shows','none',130,art+'/searchtv.jpg')
        main.addDir('Featured',base_url+'?sort=featured&tv',11,art+'/featured.jpg')
        main.addDir('Rating',base_url+'?sort=ratings&tv',11,art+'/rating.jpg')
        main.addDir('Popular',base_url+'?sort=views&tv',11,art+'/popular.jpg')
        main.addDir('New Releases',base_url+'?sort=release&tv',11,art+'/newr.jpg')
        main.addDir('Latest Added',base_url+'?sort=latest-added&tv',11,art+'/latest.jpg')
        main.addDir('2013 TV Shows',base_url+'?year=2013&tv',11,art+'/2013.jpg')
        main.addDir('2012 TV Shows',base_url+'?year=2012&tv',11,art+'/2012.jpg')
        main.addDir('Tv Genres',base_url,10,art+'/genres.jpg')
        main.VIEWSB() 


def TVGENRES():
        main.addDir('Action',base_url +'index.php?genre=action&tv',11,art+'/action.jpg')
        main.addDir('Animation',base_url +'index.php?genre=animation&tv',11,art+'/anim.jpg')
        main.addDir('Comedy',base_url +'index.php?genre=comedy&tv',11,art+'/comedy.jpg')
        main.addDir('Crime',base_url +'index.php?genre=crime&tv',11,art+'/crime.jpg')
        main.addDir('Documentary',base_url +'index.php?genre=documentary&tv',11,art+'/docs.jpg')
        main.addDir('Drama',base_url +'index.php?genre=drama&tv',11,art+'/drama.jpg')
        main.addDir('Family',base_url +'index.php?genre=family&tv',11,art+'/family.jpg')
        main.addDir('Horror',base_url +'index.php?genre=horror&tv',11,art+'/horror.jpg')
        main.addDir('Romance',base_url +'index.php?genre=romance&tv',11,art+'/romance.jpg')
        main.addDir('Sci-Fi',base_url +'index.php?genre=sci-fi&tv',11,art+'/scifi.jpg')
        main.addDir('Thriller',base_url +'index.php?genre=thriller&tv',11,art+'/thriller.jpg')    
        main.VIEWSB()

def ADULT():
    main.addDir('Latest Added','http://megabox.li/?xxx',70,art+'/latest.jpg')
    main.addDir('Rating','http://megabox.li/?sort=ratings&xxx',70,art+'/rating.jpg')
    main.addDir('Popular','http://megabox.li/?sort=views&xxx',70,art+'/popular.jpg')
    main.addDir('Random','http://megabox.li/?sort=random&xxx',70,art+'/random.jpg')
    main.addDir('Search','http://megabox.li/index.php?search=',75,art+'/searchxxx.jpg')
    main.addDir('A-Z','http://megabox.li/?xxx',76,art+'/az.jpg')

#############################################################################################################################################        
       

def getListFile(url, path, excepturl = None ):
        link = ''
        t = threading.Thread(target=setListFile,args=(url,path,excepturl))
        t.start()
        if not os.path.exists(path):
            t.join()
        if os.path.exists(path):
            try: link = open(path).read()
            except: pass
        return link       
def setListFile(url, path, excepturl = None):
        content = None
        try:
            content=main.OPENURL(url, verbose=False)
        except:
            if excepturl:
                content=main.OPENURL(excepturl, verbose=False)
        if content:
            try:
                open(path,'w+').write(content)
            except: pass
        return

def DownloaderClass2(url,dest):
        try:
            urllib.urlretrieve(url,dest)
        except Exception, e:
            dialog = xbmcgui.Dialog()
            main.ErrorReport(e)
            dialog.ok("Megabox", "Report the error below", str(e), "We will try our best to help you")


def DownloaderClass(url,dest):
        try:
            dp = xbmcgui.DialogProgress()
            dp.create("Megabox","Downloading & Copying File",'')
            urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        except Exception, e:
            dialog = xbmcgui.Dialog()
            main.ErrorReport(e)
            dialog.ok("Megabox", "Report the error below", str(e), "We will try our best to help you")
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
        try:
            percent = min((numblocks*blocksize*100)/filesize, 100)
            dp.update(percent)
        except:
            percent = 100
            dp.update(percent)
        if (dp.iscanceled()): 
            print "DOWNLOAD CANCELLED" # need to get this part working
            return False
        dp.close()
        del dp

####################Messages##########################################################################################################

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
        from resources.libs import megabox
        megabox.MOVIES(url)
        
elif mode==2:
        print ""+url
        MOVIEGENRE(url)

elif mode==3:
        from resources.libs import megabox
        print ""+url
        megabox.VIDEOLINKS(name,url)        

elif mode==4:
        from resources.libs import megabox
        print ""+url
        megabox.SEARCH(url)
        
elif mode==5:
        from resources.libs import megabox
        print ""+url
        megabox.Searchhistory()

elif mode==6:
        from resources.libs import megabox
        print ""+url
        megabox.PLAY(name,url)

elif mode==7:
        from resources.libs import megabox
        print ""+url
        megabox.PLAYB(name,url)

elif mode==8:
        from resources.libs import megabox
        print ""+url
        megabox.GRABLINKS(url)
    
elif mode==9:
        print ""+url
        TV()
        
elif mode==10:
        print ""+url
        TVGENRES()

elif mode==11:
        from resources.libs import megabox
        megabox.TV(url)

elif mode==12:
        from resources.libs import megabox
        megabox.Seasons(url,name)

elif mode==13:
        from resources.libs import megabox
        megabox.Episodes(url,season)

elif mode==14:
        from resources.libs import megabox
        print ""+url
        megabox.GRABTVLINKS(url)

elif mode==15:
        from resources.libs import megabox
        print ""+url
        megabox.TVVIDEOLINKS(url)

elif mode==16:
        from resources.libs import megabox
        print ""+url
        megabox.GRABMORE(name,url)

elif mode==17:
        from resources.libs import megabox
        megabox.ADULTGENRE(url)             


elif mode==40:
        from resources.libs import megabox
        megabox.GRABADULT(url)        

elif mode==50:
        from resources.libs import megabox
        megabox.YOUTUBE(url)

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


        

elif mode==100:
        from resources.libs import megabox
        print ""+url
        megabox.Searchhistory()
elif mode==120:
        from resources.libs import megabox
        print ""+url
        megabox.SEARCH(url)
elif mode==128:
        main.Clearhistory(url)
elif mode==130:
        from resources.libs import megabox
        print ""+url
        megabox.Searchhistorytv()
elif mode==135:
        from resources.libs import megabox
        print ""+url
        megabox.SEARCHTV(url)        




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


elif mode == 1999:
    settings.openSettings()

elif mode == 2000:
    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
