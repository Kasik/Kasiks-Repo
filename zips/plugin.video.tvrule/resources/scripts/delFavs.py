import urllib,urllib2,re,cookielib,xbmcplugin,xbmcgui,xbmcaddon,time,socket,string,os,shutil
from t0mm0.common.addon import Addon

#SET DIRECTORIES
addon_id = 'plugin.video.tvrule'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
datapath = addon.get_profile()

favpath=os.path.join(datapath,'Favourites')
moviefav=os.path.join(favpath,'Movies')
FavFile=os.path.join(moviefav,'Fav') 

def delFAVS(url,title):
    if os.path.exists(FavFile):
        Favs=re.compile('url="(.+?)",name="(.+?)"').findall(open(FavFile,'r').read())
        if not str(Favs).find(title):
            xbmc.executebuiltin("XBMC.Notification([B][COLOR green]TV Rule[/COLOR][/B],[B][COLOR orange]"+title+"[/COLOR]not in Favourites.[/B],1000,"")")
        if len(Favs)<=1 and str(Favs).find(title):
            os.remove(FavFile)
            xbmc.executebuiltin("Container.Refresh")
        if os.path.exists(FavFile):
            for url,name in reversed(Favs):
                if title == name:
                    Favs.remove((url,name))
                    os.remove(FavFile)
                    for url,name in Favs:
                        try:
                            open(FavFile,'a').write('url="%s",name="%s"'%(url,name))
                            xbmc.executebuiltin("Container.Refresh")
                            xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]"+title+"[/COLOR][/B],[B]Removed from Favourites[/B],1000,"")")
                        except: pass
        else: xbmc.executebuiltin("XBMC.Notification([B][COLOR green]TV Rule[/COLOR][/B],[B]You Have No Favourites to delete[/B],1000,"")")

bits = sys.argv[1].split(',')
print "BaseUrl= "+sys.argv[0]
url = bits[0].replace("[(u'",'').replace("'",'')
print "Url= "+url
title = bits[1].replace("'[B][COLOR green]",'').replace("[/COLOR][/B]')]",'').strip()
print "name= "+title

delFAVS(url.replace('[(',''),title.replace("'",'').replace(')]',''))
