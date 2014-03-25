import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading
from BeautifulSoup import MinimalSoup as BeautifulSoup
try:
    from resources.libs import main,settings    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.filmesonlinegratis/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]Filmesonlinegratis Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module to Fix')
    xbmc.log('Filmesonlinegratis ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)
reload(sys)
sys.setdefaultencoding( "UTF-8" )   
    
#Filmesonlinegratis.net - by Kasik 2014.

base_url ='http://www.filmesonlinegratis.net'
addon_id = 'plugin.video.filmesonlinegratis'
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

        main.addDirHome('Search',base_url,100,art+'/search.png')
        #main.addDirHome('NEW MOVIES AT LAUNCH','http://www.filmesonlinegratis.net/filmes-lancamentos',1,art+'/.png')
        #main.addDirHome('LATEST SERIES ADDED','http://www.filmesonlinegratis.net/series',1,art+'/.png')
        main.addDirHome('LATEST ADDED','http://www.filmesonlinegratis.net/',1,art+'/latest.png')
        main.addDirHome('MOVIES BY GENRE','http://www.filmesonlinegratis.net/',2,art+'/genre.png')
        #main.addDirHome('Novel','http://www.filmesonlinegratis.net/novelas',1,art+'/.png')
        main.addDirHome('Series [COLOR red](NOT FULLY FUCTIONAL, VIDIG RESOLVER NEEDED!!)[/COLOR]','http://www.filmesonlinegratis.net/series',3,art+'/series.png')
        main.VIEWSB()

def GENRES():
        main.addDirHome('Action','http://www.filmesonlinegratis.net/acao',1,art+'/.png')
        main.addDirHome('Animation','http://www.filmesonlinegratis.net/animacao',1,art+'/.png')
        main.addDirHome('Adventure','http://www.filmesonlinegratis.net/aventura',1,art+'/.png')
        main.addDirHome('Comedy','http://www.filmesonlinegratis.net/comedia',1,art+'/.png')
        main.addDirHome('Romantic Comedy','http://www.filmesonlinegratis.net/comedia-romantica',1,art+'/.png')
        main.addDirHome('Crime','http://www.filmesonlinegratis.net/crime',1,art+'/.png')
        main.addDirHome('Documentary','http://www.filmesonlinegratis.net/documentario',1,art+'/.png')
        main.addDirHome('Drama','http://www.filmesonlinegratis.net/drama',1,art+'/.png')
        main.addDirHome('Western','http://www.filmesonlinegratis.net/faroeste',1,art+'/.png')
        main.addDirHome('Science Fiction','http://www.filmesonlinegratis.net/ficcao-cientifica',1,art+'/.png')
        main.addDirHome('War','http://www.filmesonlinegratis.net/guerra',1,art+'/.png')
        main.addDirHome('Musical','http://www.filmesonlinegratis.net/musical',1,art+'/.png')
        main.addDirHome('Cop','http://www.filmesonlinegratis.net/policial',1,art+'/.png')
        main.addDirHome('Romance','http://www.filmesonlinegratis.net/romance',1,art+'/.png')
        main.addDirHome('Suspense','http://www.filmesonlinegratis.net/suspense',1,art+'/.png')
        main.addDirHome('Terror','http://www.filmesonlinegratis.net/terror',1,art+'/.png')
        main.addDirHome('Thriller','http://www.filmesonlinegratis.net/thriller',1,art+'/.png')
        
        
                     
      
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
            dialog.ok("filmesonlinegratis", "Report the error below", str(e), "We will try our best to help you")


def DownloaderClass(url,dest):
        try:
            dp = xbmcgui.DialogProgress()
            dp.create("filmesonlinegratis","Downloading & Copying File",'')
            urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        except Exception, e:
            dialog = xbmcgui.Dialog()
            main.ErrorReport(e)
            dialog.ok("filmesonlinegratis", "Report the error below", str(e), "We will try our best to help you")
 
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
        main.VIEWSB()        
       
elif mode==1:
        from resources.libs import filmesonlinegratis
        filmesonlinegratis.MOVIES(url)
        
elif mode==2:
        print ""+url
        GENRES()

elif mode==3:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.TV(url)        

elif mode==4:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.SEARCH(url)
        
elif mode==5:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.Searchhistory()

elif mode==6:
        from resources.libs import filmesonlinegratis
        filmesonlinegratis.EPISODES(url)

elif mode==7:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.GRABLINKS(url)        

elif mode==8:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.PLAY(name,url)

elif mode==9:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.PLAYB(name,url)


    





        

elif mode==100:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.Searchhistory()
elif mode==120:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.SEARCH(url)
elif mode==128:
        main.Clearhistory(url)
elif mode==130:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.Searchhistorytv()
elif mode==135:
        from resources.libs import filmesonlinegratis
        print ""+url
        filmesonlinegratis.SEARCHTV(url)        




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
