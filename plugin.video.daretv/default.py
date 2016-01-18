import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib,urllib2,re,cookielib,string,urlparse,os,time,datetime,threading
from BeautifulSoup import BeautifulSoup
try:
    import urlresolver
    from t0mm0.common.net import Net as net
    from t0mm0.common.addon import Addon
    from metahandler import metahandlers

    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.daretv/resources/art/sadface.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]The DareTv Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]Twitter @Kasik04a[/COLOR] to Fix')
    xbmc.log('The DareTv ERROR - Importing Modules: '+str(e))

    
from resources.src import main
from resources.src.scripts import settings


#The DareTv - by Kasik 2014.


base_url ='http://www.thedaretube.com/tv/'
addon_id = 'plugin.video.daretv'
selfAddon = xbmcaddon.Addon(id=addon_id)
grab = metahandlers.MetaData(preparezip = False)
addon = Addon(addon_id)
art = main.art

AddonPath = addon.get_path()
IconPath = AddonPath + "/resources/art/"




UpdatePath=os.path.join(main.datapath,'Update')
try:
    os.makedirs(UpdatePath)
except: pass
ListsPath=os.path.join(main.datapath,'Lists')
try:
    os.makedirs(ListsPath)
except: pass


############################# Main ###########################################################################################
      
def MAIN():
        main.addDirHome('TV',base_url,70,art+'/tv.png')
        main.addDirHome('Movies',base_url,10,art+'/movies.png')
        #main.addDirHome('Live Sports',base_url,20,art+'/.png')
        
def TV():
        main.addDirHome('Search','http://www.thedaretube.com/tv/index.php?menu=search&query=',215,art+'/search2.png')
        main.addDirHome('Latest Episodes','http://www.thedaretube.com/tv/new-shows',1,art+'/latesteps.png')
        main.addDirHome('TV Shows A-Z','http://www.thedaretube.com/tv/',2,art+'az.png')
        main.addDirHome('TV Show Genres','http://www.thedaretube.com/tv/tv-shows',4,art+'genres.png')
        main.addDirHome('Premiers','http://www.thedaretube.com/tv/premiers',6,art+'premiers.png')
        

        
def MOVIES():        
        main.addDirHome('Search','http://www.thedaretube.com/tv/index.php?menu=search&query=',14,art+'/search2.png')
        main.addDirHome('Latest Movies','http://www.thedaretube.com/tv/movies/date',11,art+'latestmovies.png')
        main.addDirHome('Movie Genres','http://www.thedaretube.com/tv/movies',12,art+'genres.png')
        main.addDirHome('Box Office','http://www.thedaretube.com/tv/movie-tags/boxoffice',13,art+'box.png')
        main.addDirHome('DVD Release','http://www.thedaretube.com/tv/dvdrelease',13,art+'dvd.png')
        #main.addDirHome('Theater',base_url+'',9,art+'.png')
        main.VIEWSB()
        
def LIVE():
        main.addDirHome('Live Sports','',99,art+'.png')
        main.addDirHome('Live NFL FootBall','',12,art+'.png')
        main.addDirHome('Live Sports 2','',13,art+'.png')
        main.addDirHome('Live Sports 3','',14,art+'.png')
        main.addDirHome('Search Airtime','',15,art+'.png')
        main.addDirHome('Search By Year','',16,art+'.png')
        main.VIEWSB()
        

#############################################################################################################################                


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

################################################################################ Message Box ##########################################################################################################

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


try:
        name=urllib.unquote_plus(params["name"])
except:
        pass

try:
        
        url=urllib.unquote_plus(params["url"])
        
except:
        pass

try:
        mode=int(params["mode"])
except:
        pass

try:
        iconimage=urllib.unquote_plus(params["iconimage"])
        iconimage = iconimage.replace(' ','%20')
except:
        pass
try:
        plot=urllib.unquote_plus(params["plot"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
        fanart = fanart.replace(' ','%20')
except:
        pass

try:
        genre=urllib.unquote_plus(params["genre"])
except:
        pass

try:
        title=urllib.unquote_plus(params["title"])
except:
        pass
try:
        episode=int(params["episode"])
except:
        pass
try:
        season=int(params["season"])
except:
        pass
try:
        location=urllib.unquote_plus(params["location"])
except:
        pass
try:
        path=urllib.unquote_plus(params["path"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
        MAIN()
        
elif mode==70:
        TV()
        
elif mode==1:
        from resources.src import daretv
        print ""+url
        daretv.TVIndex(url)
               
elif mode==2:
        from resources.src import daretv
        print ""+url
        daretv.TVTags(url,name)

elif mode==3:
        from resources.src import daretv
        print ""+url
        daretv.TVIndex2(url,name)       

elif mode==4:
        from resources.src import daretv
        print ""+url
        daretv.TVGenres(url,name)

elif mode==5:
        from resources.src import daretv
        print ""+url
        daretv.TVIndex3(url,name)        

elif mode==6:
        from resources.src import daretv
        print ""+url
        daretv.Premiers(url,name)

elif mode==7:
        from resources.src import daretv
        print ""+url
        daretv.TvSeasons(url,name)

elif mode==8:
        from resources.src import daretv
        print ""+url
        daretv.Episodes(url,name)

   


elif mode==10:
        MOVIES()
        
elif mode==11:
        from resources.src import daremovies
        print ""+url
        daremovies.MoviesIndex(url,name)

elif mode==12:
        from resources.src import daremovies
        print ""+url
        daremovies.MoviesTags(url,name)

elif mode==13:
        from resources.src import daremovies
        print ""+url
        daremovies.MovieIndex2(url,name)

elif mode==14:
        from resources.src import daremovies
        print ""+url
        daremovies.SEARCHS(url)

elif mode==15:
        from resources.src import daremovies
        print ""+url
        daremovies.SearchResults(url)        
        
elif mode==16:
        from resources.src import daremovies
        print ""+url
        daremovies.MovieIndex2(url,name)

elif mode==17:
        from resources.src import daremovies
        print ""+url
        daremovies.MovieIndex2(url,name)        

        

elif mode==20:
        LIVE()        
        
        

elif mode==75:
       from resources.src import daretv
       print ""+url
       daretv.VIDEOLINKS(name,url)

elif mode==80:
       from resources.src import daremovies
       print ""+url
       daremovies.VIDEOLINKS(name,url)  

elif mode==100:
       from resources.src import daretv
       print ""+url
       daretv.Play(url,name)

elif mode==150:
       from resources.src import daretv
       print ""+url
       daretv.PlayB(name,url)
       
    

elif mode==200:
        from resources.src import daretv
        print ""+url
        daretv.Searchhistory()

elif mode==215:
        from resources.src import daretv
        print ""+url
        daretv.SEARCHS(url)

elif mode==220:
        from resources.src import daretv
        print ""+url
        daretv.SearchResults(url)        

        

elif mode==20:
        main.Clearhistory(url)



















































elif mode == 1999:
    settings.openSettings()

elif mode == 2000:
    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
