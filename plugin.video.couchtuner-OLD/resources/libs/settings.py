import xbmc,xbmcaddon,os
addon_id = 'plugin.video.couchtuner'
selfAddon = xbmcaddon.Addon(id=addon_id)
# Examples:
#Commands.append(('Add-on settings','XBMC.RunScript('+xbmc.translatePath('special://home/addons/' + addon_id + '/resources/libs/settings.py')+')'))
# or
#Commands.append(('Add-on settings','XBMC.RunScript('+xbmc.translatePath(couchtunerpath + '/resources/libs/settings.py')+')'))
# or
#Commands.append(('[B][COLOR lime]couchtuner[/COLOR] Settings[/B]','XBMC.RunScript('+xbmc.translatePath(couchtunerpath + '/resources/libs/settings.py')+')'))
def getHomeItems():
    d=[]
    for x in range(38): 
        d.append(None);
        itemid = str(x + 1)
        if selfAddon.getSetting("homeitem_" +itemid+ "_enabled")== "true":
            d[x]=int(selfAddon.getSetting("homeitem_" + itemid))
    return d

def getRefreshRequiredSettings():
    s=[]
    s.append(selfAddon.getSetting("meta-view"))
    s.append(selfAddon.getSetting("meta-view-tv"))
    s.append(selfAddon.getSetting("groupfavs"))
    s.append(selfAddon.getSetting("skin"))
    s.append(selfAddon.getSetting("stracker"))
    s.append(selfAddon.getSetting("con-view"))
    s.append(selfAddon.getSetting("xpr-view"))
    s.append(selfAddon.getSetting("artwork"))
    s.append(selfAddon.getSetting("ddtv_my"))
    s.append(selfAddon.getSetting("ddtv_hdtv720p"))
    s.append(selfAddon.getSetting("ddtv_webdl720p"))
    s.append(selfAddon.getSetting("ddtv_webdl1080p"))
    s.append(selfAddon.getSetting("ddtv_hdtv480p"))
    s.append(selfAddon.getSetting("ddtv_pdtv"))
    s.append(selfAddon.getSetting("ddtv_dsr"))
    s.append(selfAddon.getSetting("ddtv_dvdrip"))
    return s

def getAccountSettings():
    s=[]
    s.append(selfAddon.getSetting("username"))
    s.append(selfAddon.getSetting("password"))
    s.append(selfAddon.getSetting("rlsusername"))
    s.append(selfAddon.getSetting("rlspassword"))
    s.append(selfAddon.getSetting("srusername"))
    s.append(selfAddon.getSetting("srpassword"))
    s.append(selfAddon.getSetting("ghusername"))
    s.append(selfAddon.getSetting("ghpassword"))
    s.append(selfAddon.getSetting("skyusername"))
    s.append(selfAddon.getSetting("skypassword"))
    return s
    
def openSettings():
    d = getHomeItems()
    s = getRefreshRequiredSettings()
    a = getAccountSettings()
    selfAddon.openSettings()
    dnew = getHomeItems()
    snew = getRefreshRequiredSettings()
    anew = getAccountSettings()
    if a != anew:
        ClearDir(os.path.join(xbmc.translatePath(selfAddon.getAddonInfo('profile')),'Cookies'))
        ClearDir(os.path.join(os.path.join(xbmc.translatePath(selfAddon.getAddonInfo('profile')),'Cache'),'Sidereel'))
        snew = []
    if d != dnew or s != snew:
        ClearDir(os.path.join(xbmc.translatePath(selfAddon.getAddonInfo('profile')),'Temp'))
        xbmc.executebuiltin("XBMC.Container.Refresh")  

def ClearDir(dir):
    if os.path.exists(dir):
        if os.path.isfile(dir): os.remove(dir)
        else:
            for the_file in os.listdir(dir):
                file_path = os.path.join(dir, the_file)
                try:os.unlink(file_path)
                except Exception, e: print str(e)

if  __name__ == "__main__": openSettings()
