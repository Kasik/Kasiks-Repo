import urllib,urllib2,re,cookielib,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main

#Couchtuner - by Kasik04a 2014.

from t0mm0.common.addon import Addon
from resources.universal import playbackengine, watchhistory
addon_id = 'plugin.video.couchtuner'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.couchtuner', sys.argv)
art = main.art    
wh = watchhistory.WatchHistory('plugin.video.couchtuner')
DownloadLog=os.path.join(main.datapath,'Downloads')
DownloadFile=os.path.join(DownloadLog,'DownloadLog')

def LIST():
        if os.path.exists(DownloadFile):
                DownloadLog=re.compile('{name="(.+?)",destination="(.+?)"}').findall(open(DownloadFile,'r').read())
                for name,video in reversed(DownloadLog):
                    main.addDLog(name,video,242,'','','','','','')

def LINK(mname,murl):
        ok=True
        if re.findall('(.+?)\ss(\d+)e(\d+)\s',mname,re.I):
                infoLabels =main.GETMETAEpiT(mname,'','')
                video_type='episode'
                season=infoLabels['season']
                episode=infoLabels['episode']
        elif re.findall('Season(.+?)Episode([^<]+)',mname,re.I):
                infoLabels =main.GETMETAEpiT(mname,'','')
                video_type='episode'
                season=infoLabels['season']
                episode=infoLabels['episode']
        else:
                infoLabels =main.GETMETAT(mname,'','','')
                video_type='movie'
                season=''
                episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        stream_url = murl
        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]DownloadedContent[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
        player.KeepAlive()
        return ok

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
        else: xbmc.executebuiltin("XBMC.Notification([B][COLOR green]couchtuner[/COLOR][/B],[B]You Have No Downloaded Content[/B],1000,"")")
