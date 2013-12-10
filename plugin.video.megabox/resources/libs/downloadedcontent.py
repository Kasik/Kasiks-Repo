import urllib,urllib2,re,cookielib,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main

#Megabox - by Kasik 2013.

from t0mm0.common.addon import Addon
addon_id = 'plugin.video.megabox'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.megabox', sys.argv)
art = main.art    
wh = watchhistory.WatchHistory('plugin.video.megabox')
DownloadLog=os.path.join(main.datapath,'Downloads')
DownloadFile=os.path.join(DownloadLog,'DownloadLog')

def LIST():
        if os.path.exists(DownloadFile):
                DownloadLog=re.compile('{name="(.+?)",destination="(.+?)"}').findall(open(DownloadFile,'r').read())
                for name,video in reversed(DownloadLog):
                    main.addDLog(name,video,242,'','','','','','')

def LINK(mname,murl):
        sources = []
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,2000)")
        match=re.compile('Source: <a href="([^"]*)" target="_blank"').findall(link)
        for url in match:
                url=url
                print url
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('target="_blank">([^"]*)</a>').findall(link)
        for url in match:
                url=url
                print url
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('action="([^"]*)" style').findall(link)
        for url in match:
                url=url
                print url
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('location.href = \'([^"]*)\';').findall(link)
        for url in match:
                url=url
                print url
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('location.href = "([^"]*)";').findall(link)
        for url in match:
                url=url
                print url
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)        
        if (len(sources)==0):
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Show doesn't have playable links,5000)")
      
        else:
                source = urlresolver.choose_source(sources)
                if source:
                        stream_url = source.resolve()
                        if source.resolve()==False:
                                xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Cannot Be Resolved,5000)")
                                return
                else:
                      stream_url = False
                      return
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                listitem.setInfo('video', {'Title': name, 'Year': ''} )       
                xbmc.Player().play(str(stream_url), listitem)
                main.addDir('','','','')    

def REMOVE(mname,murl):
    try:
        os.remove(murl)
    except:
        pass
    if os.path.exists(DownloadFile):
        DownloadLog=re.compile('{name="(.+?)",destination="(.+?)"}').findall(open(DownloadFile,'r').read())
        if len(DownloadLog)<=1 and str(DownloadLog).find(mname):
            os.remove(DownloadFile)
            xbmc.executebuiltin("Container.Refresh")
        if os.path.exists(DownloadFile):
            for name,video in reversed(DownloadLog):
                if mname == name:
                    DownloadLog.remove((name,video))
                    os.remove(DownloadFile)
                    for name,video in DownloadLog:
                        try:
                            open(DownloadFile,'a').write('{name="%s",destination="%s"}'%(name,video))
                            xbmc.executebuiltin("Container.Refresh")
                            xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]"+mname+"[/COLOR][/B],[B]Removed from Downloads[/B],1000,"")")
                        except: pass
        else: xbmc.executebuiltin("XBMC.Notification([B][COLOR green]MegaBox[/COLOR][/B],[B]You Have No Downloaded Content[/B],1000,"")")
