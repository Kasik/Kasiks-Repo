import urllib,urllib2,re,cookielib,xbmcplugin,xbmcgui,xbmcaddon,time,socket,string,os,shutil
from t0mm0.common.addon import Addon

#SET DIRECTORIES
addon_id = 'plugin.video.tvrule'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
datapath = addon.get_profile()

favpath=os.path.join(datapath,'Favourites')
tvfav=os.path.join(favpath,'Live')
FavFile=os.path.join(tvfav,'LiveFav') 

def delFAVS(url,title,mode,thumb,plot,type):
    Favs=re.compile('url="(.+?)",name="(.+?)",mode="(.+?)",thumb="(.+?)",plot="(.+?)",type="(.+?)"').findall(open(FavFile,'r').read())
    if not str(Favs).find(title):
        xbmc.executebuiltin("XBMC.Notification([B][COLOR green]TV Rule[/COLOR][/B],[B][COLOR orange]"+title+"[/COLOR]not in Favourites.[/B],1000,"")")
    if len(Favs)<=1 and str(Favs).find(title):
        os.remove(FavFile)
        xbmc.executebuiltin("Container.Refresh")
    if os.path.exists(FavFile):
        for url,name,mode,thumb,plot,type in reversed(Favs):
            if title == name:
                Favs.remove((url,name,mode,thumb,plot,type))
                os.remove(FavFile)
                for url,name,mode,thumb,plot,type in Favs:
                    try:
                        open(FavFile,'a').write('url="%s",name="%s",mode="%s",thumb="%s",plot="%s",type="%s",'%(url,name,mode,thumb,plot,type))
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
mode = bits[2].replace(" ",'').replace("'",'')
print "Mode= "+mode
thumb = bits[3].replace(" ",'').replace("'",'')
print "Thumb= "+thumb
plot = bits[4].replace("'",'').replace('"','').replace("(",'').replace(")",'').replace("]",'')
print "Plot= "+plot
type=bits[5].replace(" ",'').replace("'",'').replace('"','').replace("(",'').replace(")",'').replace("]",'')
print "Type= "+type

delFAVS(url.replace('[(',''),title.replace("'",'').replace(')]',''),mode,thumb,plot,type)
