import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib,urllib2,re,cookielib,string,urlparse,os,time,datetime,threading
from BeautifulSoup import BeautifulSoup
try:
    import urlresolver
    from t0mm0.common.net import Net as net
    from t0mm0.common.addon import Addon
    from metahandler import metahandlers

    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.vdeobull/resources/art/sadface.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]VideoBull Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]Xbmchub.com[/COLOR] to Fix')
    xbmc.log('VideoBull ERROR - Importing Modules: '+str(e))

    
from resources.src import main
from resources.src.scripts import settings


#VideoBull.com - by Kasik 2013.

MainUrl='http://videobull.to/'
base_url ='http://videobull.com/'
addon_id = 'plugin.video.vdeobull'
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
     
def MAIN(index=False):
        main.addDir('Latest Tv Shows',MainUrl,860,art+'/latest.png',index=index)
        main.addDir('A-Z Tv Shows',MainUrl+'tv-shows/',861,art+'/AZ.png',index=index)
        #main.addDirHome('Popular Shows',base_url,2,art+'popular.png')
        main.addDir('Search for Tv Shows',MainUrl,866,art+'/search.png',index=index)
        main.VIEWSB()






def MAINB():
        main.addDirHome('Search TV Shows',base_url,10,art+'/search.png')
        main.addDirHome('Latest TV Shows',base_url,1,art+'latest.png')
        main.addDirHome('Popular Shows',base_url,2,art+'popular.png')
        main.addDirHome('All Tv Shows',base_url+'tv-shows/',3,art+'AZ.png')

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
               
       
elif mode==1:
        from resources.src import vdeobull
        print ""+url
        vdeobull.Index(url)
               
elif mode==2:
        from resources.src import vdeobull
        print ""+url
        vdeobull.Popular(url)

elif mode==3:
        from resources.src import vdeobull
        print ""+url
        vdeobull.AtoZ(url,name)

elif mode==4:
        from resources.src import vdeobull
        print ""+url
        vdeobull.Search(url)
        
elif mode==5:
        from resources.src import vdeobull
        print ""+url
        vdeobull.Searchhistory()

elif mode==6:
        from resources.src import vdeobull
        print ""+url
        vdeobull.ALPHA(url,name)

elif mode==7:
        from resources.src import vdeobull
        print ""+url
        vdeobull.Popular2(url)

elif mode==10:
        from resources.src import vdeobull
        print ""+url
        vdeobull.SEARCHS(url)

elif mode==11:
        from resources.src import vdeobull
        print ""+url
        vdeobull.SearchResults(url)        

        

elif mode==20:
        main.Clearhistory(url)


elif mode==75:
       from resources.src import vdeobull
       print ""+url
       vdeobull.VIDEOLINKS(name,url)

elif mode==100:
       from resources.src import vdeobull
       print ""+url
       vdeobull.Play(url,name)

elif mode==134:
       from resources.src import vdeobull
       print ""+url
       vdeobull.Play64(url,name)

elif mode==150:
       from resources.src import vdeobull
       print ""+url
       vdeobull.PlayB(name,url)
       
    
###################################################################################################################################################################################################

elif mode==859:
    from resources.src import videobull
    print " " + url
    videobull.VIDBULLMAIN()

elif mode==860:
    from resources.src import videobull
    print " " + url
    videobull.List(url)

elif mode==861:
    from resources.src import videobull
    print " " + url
    videobull.VBAtoZ()

elif mode==862:
    from resources.src import videobull
    print " " + url
    videobull.SEASON()

elif mode==863:
    from resources.src import videobull
    print " " + url
    videobull.EPISODES()    

elif mode==864:
    from resources.src import videobull
    print " " + url
    videobull.List2(url)

   
elif mode==865:
    from resources.src import videobull
    print " " + url
    videobull.GRABFEED(name,url)

elif mode==866:
    from resources.src import videobull
    print ""+url
    videobull.Searchhistory()
        
elif mode==867:
    from resources.src import videobull
    print ""+url
    videobull.SEARCH(url)

elif mode==868:
    from resources.src import videobull
    print ""+url
    videobull.PLAYB(name,url)

elif mode==869:
    from resources.src import videobull
    print " " + url
    videobull.A(url)
elif mode==870:
    from resources.src import videobull
    print " " + url
    videobull.B(url)
elif mode==871:
    from resources.src import videobull
    print " " + url
    videobull.C(url)
elif mode==872:
    from resources.src import videobull
    print " " + url
    videobull.D(url)
elif mode==873:
    from resources.src import videobull
    print " " + url
    videobull.E(url)
elif mode==874:
    from resources.src import videobull
    print " " + url
    videobull.F(url)
elif mode==875:
    from resources.src import videobull
    print " " + url
    videobull.G(url)
elif mode==876:
    from resources.src import videobull
    print " " + url
    videobull.H(url)
elif mode==877:
    from resources.src import videobull
    print " " + url
    videobull.I(url)
elif mode==878:
    from resources.src import videobull
    print " " + url
    videobull.J(url)
elif mode==879:
    from resources.src import videobull
    print " " + url
    videobull.K(url)
elif mode==880:
    from resources.src import videobull
    print " " + url
    videobull.L(url)
elif mode==881:
    from resources.src import videobull
    print " " + url
    videobull.M(url)
elif mode==882:
    from resources.src import videobull
    print " " + url
    videobull.N(url)
elif mode==883:
    from resources.src import videobull
    print " " + url
    videobull.O(url)
elif mode==884:
    from resources.src import videobull
    print " " + url
    videobull.P(url)
elif mode==885:
    from resources.src import videobull
    print " " + url
    videobull.Q(url)
elif mode==886:
    from resources.src import videobull
    print " " + url
    videobull.R(url)
elif mode==887:
    from resources.src import videobull
    print " " + url
    videobull.S(url)
elif mode==888:
    from resources.src import videobull
    print " " + url
    videobull.T(url)
elif mode==889:
    from resources.src import videobull
    print " " + url
    videobull.U(url)
elif mode==890:
    from resources.src import videobull
    print " " + url
    videobull.V(url)
elif mode==891:
    from resources.src import videobull
    print " " + url
    videobull.W(url)
elif mode==892:
    from resources.src import videobull
    print " " + url
    videobull.X(url)
elif mode==893:
    from resources.src import videobull
    print " " + url
    videobull.Y(url)
elif mode==894:
    from resources.src import videobull
    print " " + url
    videobull.Z(url)

elif mode==895:
    from resources.src import videobull
    print " " + url
    videobull.ONE(url)
elif mode==896:
    from resources.src import videobull
    print " " + url
    videobull.TWO(url)
elif mode==897:
    from resources.src import videobull
    print " " + url
    videobull.THREE(url)
elif mode==898:
    from resources.src import videobull
    print " " + url
    videobull.FOUR(url)
elif mode==899:
    from resources.src import videobull
    print " " + url
    videobull.FIVE(url)
elif mode==900:
    from resources.src import videobull
    print " " + url
    videobull.SIX(url)
elif mode==901:
    from resources.src import videobull
    print " " + url
    videobull.SEVEN(url)
elif mode==902:
    from resources.src import videobull
    print " " + url
    videobull.EIGHT(url)
elif mode==903:
    from resources.src import videobull
    print " " + url
    videobull.NINE(url)    
    
elif mode==904:
    from resources.src import videobull
    print " " + url
    videobull.SEARCH2(url)























































elif mode == 1999:
    settings.openSettings()

elif mode == 2000:
    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
