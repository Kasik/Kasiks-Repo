import xbmc, xbmcaddon
addon_id = 'plugin.video.megabox'
selfAddon = xbmcaddon.Addon(id=addon_id)

def getHomeItems():
    d=[]
    for x in range(34): 
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
    s.append(selfAddon.getSetting("con-view"))
    s.append(selfAddon.getSetting("xpr-view"))
    s.append(selfAddon.getSetting("artwork"))
    s.append(selfAddon.getSetting("ddtv_hdtv720p"))
    s.append(selfAddon.getSetting("ddtv_webdl720p"))
    s.append(selfAddon.getSetting("ddtv_webdl1080p"))
    s.append(selfAddon.getSetting("ddtv_hdtv480p"))
    s.append(selfAddon.getSetting("ddtv_pdtv"))
    s.append(selfAddon.getSetting("ddtv_dsr"))
    s.append(selfAddon.getSetting("ddtv_dvdrip"))
    return s

def openSettings():
    d = getHomeItems()
    s = getRefreshRequiredSettings()
    selfAddon.openSettings()
    dnew = getHomeItems()
    snew = getRefreshRequiredSettings()
    if d != dnew or s != snew:
        xbmc.executebuiltin("XBMC.Container.Refresh")  

if  __name__ == "__main__": openSettings()
