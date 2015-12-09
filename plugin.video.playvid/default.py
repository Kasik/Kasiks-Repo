#-*- coding: utf-8 -*-
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
import urllib,urllib2,re,string,os,time,threading
import cookielib,os.path,sys,socket
try:
    import utils,playvids    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.playvid/resources/images/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]Playvid Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]Github @ Kasik[/COLOR] to Fix')
    xbmc.log('Playvid ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)

#######################################
addon_id = 'plugin.video.playvid'
selfAddon = xbmcaddon.Addon(id=addon_id)    
#######################################  

socket.setdefaulttimeout(60)
xbmcplugin.setContent(utils.addon_handle, 'movies')
addon = xbmcaddon.Addon(id=utils.__scriptid__)
progress = utils.progress
dialog = utils.dialog
imgDir = utils.imgDir


def INDEX():
    playvids.Main
    #utils.addDir('[COLOR yellow]Playvids[/COLOR]','https://www.playvids.com',522,os.path.join(imgDir, 'playvid.png'),'')    
    download_path = addon.getSetting('download_path')
    if download_path != '' and os.path.exists(download_path):
        addDir('[COLOR white]Playvids[/COLOR] [COLOR yellow]Download Folder[/COLOR]',download_path,4,'','')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def getParams():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


params = getParams()
url = None
name = None
mode = None
img = None
page = 1
download = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    page = int(params["page"])
except:
    pass
try:
    img = urllib.unquote_plus(params["img"])
except:
    pass
try:
    download = int(params["download"])
except:
    pass

if mode is None: playvids.Main()

elif mode == 4: xbmc.executebuiltin('ActivateWindow(Videos, '+url+')')

elif mode == 522: playvids.Main()
elif mode == 523: playvids.List(url)
elif mode == 524: playvids.Playvid(url, name, download)
elif mode == 525: playvids.Search(url)
elif mode == 526: playvids.Cat(url)

xbmcplugin.endOfDirectory(utils.addon_handle)
