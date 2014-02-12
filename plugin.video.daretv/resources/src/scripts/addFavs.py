import urllib,urllib2,re,cookielib,sys,xbmcplugin,xbmcgui,xbmcaddon,time,socket,string,os,shutil,stat
from t0mm0.common.addon import Addon

#SET DIRECTORIES
addon_id = 'plugin.video.vdeobull'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
datapath = addon.get_profile()
favpath=os.path.join(datapath,'Favourites')
moviefav=os.path.join(favpath,'Movies')
try:
    os.makedirs(moviefav)
except:
    pass
FavFile=os.path.join(moviefav,'Fav') 

def addFAVS(url,name):
    if open(FavFile,'r').read().find(name)>0:
        xbmc.executebuiltin("XBMC.Notification([B][COLOR green]"+name+"[/COLOR][/B],[B]Already added to Favourites[/B],1000,"")")
    else:    
        open(FavFile,'a').write('url="%s",name="%s",'%(url,name))
        xbmc.executebuiltin("XBMC.Notification([B][COLOR green]"+name+"[/COLOR][/B],[B]Added to Favourites[/B],1000,"")")
    
bits = sys.argv[1].split(',')
print "BaseUrl= "+sys.argv[0]
url = bits[0].replace("[(u'",'').replace("'",'')
print "Url= "+url
name = bits[1].replace("'[B][COLOR green]",'').replace("[/COLOR][/B]')]",'').replace("'",'').replace(')]','').strip()
print "name= "+name

if not os.path.exists(FavFile):
    open(FavFile,'w').write('url="%s",name="%s",'%(url,name))
    xbmc.executebuiltin("XBMC.Notification([B][COLOR green]"+name+"[/COLOR][/B],[B]Favourites file Created.[/B],1000,"")")
else:
    addFAVS(url,name)
