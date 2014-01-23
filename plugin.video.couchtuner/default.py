import xbmc,xbmcgui, xbmcaddon, xbmcplugin,urllib2
import urllib,re,string,os,time,threading
from BeautifulSoup import MinimalSoup as BeautifulSoup
try:
    from resources.libs import main,settings    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.couchtuner/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]couchtuner Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module to Fix')
    xbmc.log('couchtuner ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)

    
#CouchTuner - by Kasik 2014.

base_url ='http://www.couchtuner.eu/'
addon_id = 'plugin.video.couchtuner'
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

        main.addDirHome('New Releases',base_url,1,art+'/New.png')
        main.addDirHome('Tv Show List',base_url + 'tv-streaming/',2,art+'/showlist.png')
        main.VIEWSB()

########################################################        


def TVLIST(url):
        for i in string.ascii_uppercase:
                main.addDir(i,base_url +'tv-streaming/#'+i.upper(),3,art+'/'+i.lower()+'.png')

def TVLISTB(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','')
        response.close()
        match=re.compile('<li><a href="([^"]*)" title="[^"]*">[%s]([^"]*)</a>'% name).findall(link)
        for url,title in match:
            title=name+title
            url = base_url + url
            print url
            main.addDir(title,url,5,'')  
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Seasons(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('&#8230;','-...').replace('&#8217;',"'").replace('\n','').replace('\t','').replace('\r','')
        response.close()
		
        match=re.compile('<span style="color: #339966;"><strong>([^"]*)</strong></span></p><ul><li>').findall(link)
        for season in match:
                main.addDir(season,url,5,'')

def Episodes(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read().replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#8211;','-').replace('&#8217;',"'").replace('season-','s').replace('episode-','e').replace('#038;','')
        response.close()
		
        match=re.compile('<a href="http://www.couchtuner.eu/([^"]*)/">([^"]*)</a>([^"]*)</strong></li>').findall(link)
        for url,episode,title in match:
                title='[COLOR blue]'+episode+'[/COLOR]'+ ' - ' +'[COLOR red]'+title+'[/COLOR]'
                url = 'http://www.zzstream.li/'+url+'.html'
                print ""+url
                main.addPlayTE(title,url,75,'','','','','','')
        match=re.compile('<a href="http://www.zzstream.li/([^"]*)">([^"]*)</a>([^"]*)</strong>').findall(link)
        for url,episode,title in match:
                title='[COLOR blue]'+episode+'[/COLOR]'+ ' - ' +'[COLOR red]'+title+'[/COLOR]'
                url='http://www.zzstream.li/'+url
                print ""+url
                main.addPlayTE(title,url,75,'','','','','','')     
                
        

################################################################################
                
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

base_url='http://www.couchtuner.eu/'



print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        print base_url 
        MAIN()

elif mode==1:
        from resources.libs import couchtuner
        print " "+url
        couchtuner.NEWRELEASE(url)
       
elif mode==2:
        print " "+url
        TVLIST(url)

elif mode==3:
        print " "+url
        TVLISTB(url)

elif mode==4:
        print " "+url
        Seasons(url)

elif mode==5:
        print " "+url
        Episodes(url)

elif mode==6:
        from resources.libs import couchtuner
        print " "+url
        couchtuner.VIDEOLINKS(url,name)

      

        

elif mode==50:
        from resources.libs import couchtuner
        print " "+url
        couchtuner.Resolve()


elif mode==75:
        from resources.libs import couchtuner
        print " "+url
        couchtuner.Play(url,name)         

       


        
   

        

xbmcplugin.endOfDirectory(int(sys.argv[1]))
