# Autoupdate Module By: Blazetamer 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,time,shutil
import downloader
import extract


try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.twomovies'
ADDON = xbmcaddon.Addon(id='plugin.video.twomovies')
#addon = Addon(addon_id, sys.argv)


try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()

settings=xbmcaddon.Addon(id='plugin.video.twomovies')
#====================Start update procedures=======================

def UPDATEFILES():
        url='https://raw.github.com/Blazetamer/twomoviesautoupdate/master/plugin.video.twomovies.zip'
        path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
        addonpath=xbmc.translatePath(os.path.join('special://','home/addons'))
        name= 'mdbupdatepackage.zip'
        lib=os.path.join(path,name)
        try: os.remove(lib)
        except: pass
        downloader.download(url, lib, '')
        extract.all(lib,addonpath,'')
        LogNotify('Update Complete', 'Resetting Menus', '5000', 'http://addonrepo.com/xbmchub/twomovies/images/icon.png')
        return
        



def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")       
