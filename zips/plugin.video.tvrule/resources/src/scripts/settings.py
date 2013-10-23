import xbmc, xbmcaddon
addon_id = 'plugin.video.tvrule'
selfAddon = xbmcaddon.Addon(id=addon_id)



def getHomeItems():
    d=[]
    for x in range(24): 
        d.append(None);
        itemid = str(x + 1)
        if selfAddon.getSetting("home_item_" +itemid+ "_enabled")== "true":
            d[x]=int(selfAddon.getSetting("home_item_" + itemid))
    return d

def getRefreshRequiredSettings():
    s=[]
    s.append(selfAddon.getSetting("meta-view"))
    s.append(selfAddon.getSetting("meta-view-tv"))
    s.append(selfAddon.getSetting("groupfavs"))
    s.append(selfAddon.getSetting("con-view"))
    s.append(selfAddon.getSetting("xpr-view"))
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
