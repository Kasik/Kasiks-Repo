import urllib,urllib2,re,cookielib,sys,xbmcplugin,xbmcgui,xbmcaddon,time,socket,string,os,shutil,stat
from t0mm0.common.addon import Addon

#SET DIRECTORIES
addon_id = 'plugin.video.tvrule'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
datapath = addon.get_profile()
favpath=os.path.join(datapath,'Favourites')
tvfav=os.path.join(favpath,'Movies')
try:
    os.makedirs(tvfav)
except:
    pass
FavFile=os.path.join(tvfav,'OtherFav') 

def addFAVS(url,name,mode,thumb,plot,type):
    if open(FavFile,'r').read().find(name)>0:
        xbmc.executebuiltin("XBMC.Notification([B][COLOR green]"+name+"[/COLOR][/B],[B]Already added to Favourites[/B],1000,"")")
    else:    
        open(FavFile,'a').write('url="%s",name="%s",mode="%s",thumb="%s",plot="%s",type="%s",'%(url,name,mode,thumb,plot,type))
        xbmc.executebuiltin("XBMC.Notification([B][COLOR green]"+name+"[/COLOR][/B],[B]Added to Favourites[/B],1000,"")")
    
bits = sys.argv[1].split(',')
print "BaseUrl= "+sys.argv[0]
url = bits[0].replace("[(u'",'').replace("'",'').replace("[(",'')
print "Url= "+url
name = bits[1].replace("u'",'').replace("'[B][COLOR green]",'').replace("[/COLOR][/B]')]",'').replace("'",'').replace(')]','').strip()
print "name= "+name
mode = bits[2].replace("u'",'').replace(" ",'').replace("'",'')
print "Mode= "+mode
thumb = bits[3].replace("u'",'').replace(" ",'').replace("'",'')
print "Thumb= "+thumb
plot = bits[4].replace("u'",'').replace("'",'').replace('"','').replace("(",'').replace(")",'').replace("]",'').replace(",",'.')
print "Plot= "+plot
type=bits[5].replace("u'",'').replace(" ",'').replace("'",'').replace('"','').replace("(",'').replace(")",'').replace("]",'')
print "Type= "+type

if not os.path.exists(FavFile):
    open(FavFile,'w').write('url="%s",name="%s",mode="%s",thumb="%s",plot="%s",type="%s",'%(url,name,mode,thumb,plot,type))
    xbmc.executebuiltin("XBMC.Notification([B][COLOR green]"+name+"[/COLOR][/B],[B]Favourites file Created.[/B],1000,"")")
else:
    addFAVS(url,name,mode,thumb,plot,type)
