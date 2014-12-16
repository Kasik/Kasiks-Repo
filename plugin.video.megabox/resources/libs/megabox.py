#-*- coding: utf-8 -*-
import urllib,re,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import urlresolver

#Megabox - by Kasik04a 2014.

addon_id = 'plugin.video.megabox'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
MainUrl='http://megashare.li/'
prettyName='Megabox'

def LISTMOVIES(murl,index=False):
    link=main.OPENURL(murl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match = re.findall('lass="item"><a href="([^"]*)"><img alt=".+?src="([^"]*)" /></a><div class="title"><a title="watch movie([^"]*)".+?<div class="year"> ([^"]*)</div>',link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for url,thumb,name,date in match:
        name = name.upper()
        main.addInfo(name+'[COLOR blue] '+date+'[/COLOR]',MainUrl+url,50,thumb,'','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False   
    dialogWait.close()
    del dialogWait
        
    paginate=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
    if paginate:
       xurl=MainUrl+paginate[0]
       main.addDir('[COLOR blue]Next Page ->[/COLOR]',xurl,1,art+'/next.jpg',index=index)
       xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
       main.VIEWS()


def GENRES(url,index=False):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match = re.findall('<a href="[?]genre=([^"]*)">([^"]*)</a></li>',link)
    for url,name in match:
     url = MainUrl + '?genre=' + url
     if 'adult' in url:
      HideAdult = selfAddon.getSetting('Hide-Adult')
      if HideAdult == 'false':    
       name = "[B][COLOR red]" + name + "[/COLOR][/B]"    
       main.addDir(name,url,17,'','')
     else:
      main.addDir(name,url,1,'','')   


def YEARS(url,index=False):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match = re.findall('<li><a href="[?]year=([^"]*)">([^"]*)</a>',link)
    for url,name in match:
     url = MainUrl + '?year=' + url   
     main.addDir(name,url,1,'','')




def Searchhistory(index=False):
    seapath=os.path.join(main.datapath,'Search')
    SeaFile=os.path.join(seapath,'SearchHistoryMB')
    if not os.path.exists(SeaFile):
        SEARCH(index=index)
    else:
        main.addDir('Search','###',20,art+'/search.png',index=index)
        main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
        for seahis in reversed(searchis):
            url=seahis
            seahis=seahis.replace('%20',' ')
            main.addDir(seahis,url,20,thumb,index=index)
            
def SEARCH(murl = '',index=False):
    encode = main.updateSearchFile(murl,'Movies')
    if not encode: return False   
    surl='http://megashare.li/index.php?search='+encode+'&movie=&x=0&y=0'
    link=main.OPENURL(surl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('class="item"><a href="([^"]*)"><img alt=".+?src="([^"]*)" /></a><div class="title"><a title="watch movie([^"]*)" href=".+?<div class="year"> ([^"]*)</div>').findall(link)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Movie list is cached.')
    totalLinks = len(match)
    loadedLinks = 0
    remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
    xbmc.executebuiltin("XBMC.Dialog.Close(busydialog,true)")
    for url,thumb,name,date in match:
        name=name.replace('-','').replace('&','').replace('acute;','')
        furl= MainUrl+url
        main.addInfo(name+'[COLOR blue] '+date +'[/COLOR]',furl,50,thumb,'','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False 
    dialogWait.close()
    del dialogWait
    exist = re.findall('<a href="([^"]*)" class="next">Next &#187;</a>',link)
    if exist:
        main.addDir('[COLOR blue]Next Page ->[/COLOR]',MainUrl+url,20,art+'/next.jpg',index=index)
        
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')



def GRABLINKS(url):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('<img src=images/star.gif>','').replace('player=2','') 
    matchname=re.compile('<div align="left"><strong>Watch ([^"]*) on:</strong></div>').findall(link)
    for name in matchname:
     match=re.compile('<a id="link-[^"]*" href="info.php[?]id=([^"]*)&([^"]*)&link=([^"]*)&host=[^"]*"><div class="[^"]*"><span class="([^"]*)"></span></div><div class="[^"]*">([^"]*)</div>').findall(link)
     for link,age,link1,quality,host in match:
      if 'older' in age:    
       url = MainUrl+ 'player.php?authid=&id='+link+'&link='+link1+'&type=older_v2&part=&site=inactive&ref=1'
       main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,90,'.png','.png')
    else:
       match=re.compile('href="info.php[?]id=([^"]*)&link=([^"]*)&host=[^"]*"><div class="[^"]*"><span class="([^"]*)"></span></div><div class="[^"]*">([^"]*)</div>').findall(link)
       for link,link1,quality,host in match:
        url = MainUrl + 'player.php?authid=&id='+link+'&link='+link1+'&type=new&part=&site=inactive&ref=1'
        main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,90,'.png','.png')









def resolveMBurl(url):
    html=main.OPENURL(url)
    match = re.search('<p> Source: <a href="([^>]*)" target',html)
    if match: return match.group(1)
    return        
    match2 = re.search('location.href = \'([^>]*)\';',html)
    if match2: return match.group(2)
    return    
    match3 = re.search('action=\'([^>]*)\'>',html)
    if match3: return match.group(3)
    return        
    match4 = re.search('src="([^>]*)" frameborder="0" allowfullscreen=""></iframe></textarea></p>',html)
    if match4: return match.group(4)
    return        
    match5 = re.search('src=\'([^>]*)\' scrolling=\'no\'></iframe></textarea>',html)
    if match5: return match.group(5)
    match6 = re.search('target="_blank" href="([^"]*)"',html)
    if match6: return match.group(6)
    return        
        



def PLAY(name,url):
        sources = []
        link=main.ADULT_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,2000)")
        match=re.compile('<p> Source: <a href="([^>]*)" target').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('location.href = \'([^>]*)\';').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('action=\'([^>]*)\'>').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src="([^>]*)" frameborder="0" allowfullscreen=""></iframe></textarea></p>').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)        
        match=re.compile('src="([^"]*)" scrolling="no" allowfullscreen></iframe></textarea>').findall(link)
        for url in match:
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)

        match=re.compile('src="http://play.flashx.tv/player/embed.php[?]hash=([^"]*)" scrolling="no" allowfullscreen></iframe></center>').findall(link)
        for url in match:
                url = 'http://flashx.tv/video/' + url + '/'
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src="http://played.to/embed-([^"]*)-[^"]*.html" scrolling="no" allowfullscreen></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://played.to/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('<p> Source: <a href="http://cloudyvideos.com/([^"]*)" target').findall(link)
        for url in match:
                url = 'http://cloudyvideos.com/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('location.href = \'http://dropvideo.com/video/([^"]*)\';</script>').findall(link)
        for url in match:
                url = 'http://dropvideo.com/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('<embed src="http://www.youtube.com/v/([^"]*)=en&fs=1&rel=0" type="application/x-shockwave-flash.+?</textarea>').findall(link)
        for url in match:
                url = 'https://www.youtube.com/watch?feature=player_embedded&v=' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src=\'http://embed.divxstage.eu/embed.php[?]v=([^"]*)&width=[^"]*&height=[^"]*\' scrolling=\'no\'></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.divxstage.eu/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)         
        match=re.compile('src=\'http://embed.movshare.net/embed.php[?]v=([^"]*)&width=[^"]*&height=[^"]*&color=[^"]*\' scrolling=\'no\'></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.movshare.net/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src="http://embed.videoweed.es/embed.php[?]v=([^"]*)&width=[^"]*&height=[^"]*" scrolling="no"></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.videoweed.es/file/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src=\'http://embed.novamov.com/embed.php[?]width=[^"]*&height=[^"]*&v=([^"]*)&px=1\' scrolling=\'no\'></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.novamov.com/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)         
        match=re.compile('src=\'http://embed.nowvideo.sx/embed.php[?]width=[^"]*&height=[^"]*&v=([^"]*)\' scrolling=\'no\'></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.nowvideo.sx/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('href="http://mightyupload.com/embed-([^"]*)-.+?"><img src').findall(link)
        for url in match:
                url = 'http://mightyupload.com/' + url 
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

       

def PLAYB(name,url):
        sources = []
        link=main.ADULT_URL(url)
        #link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,2000)")
        match=re.compile('src="http://play.flashx.tv/player/embed.php[?]hash=([^"]*)" scrolling="no" allowfullscreen></iframe></center>').findall(link)
        for url in match:
                url = 'http://flashx.tv/video/' + url + '/'
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src="http://played.to/embed-([^"]*)-[^"]*.html" scrolling="no" allowfullscreen></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://played.to/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('<p> Source: <a href="http://cloudyvideos.com/([^"]*)" target').findall(link)
        for url in match:
                url = 'http://cloudyvideos.com/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('location.href = \'http://dropvideo.com/video/([^"]*)\';</script>').findall(link)
        for url in match:
                url = 'http://dropvideo.com/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('<embed src="http://www.youtube.com/v/([^"]*)=en&fs=1&rel=0" type="application/x-shockwave-flash.+?</textarea>').findall(link)
        for url in match:
                url = 'https://www.youtube.com/watch?feature=player_embedded&v=' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src=\'http://embed.divxstage.eu/embed.php[?]v=([^"]*)&width=[^"]*&height=[^"]*\' scrolling=\'no\'></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.divxstage.eu/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)         
        match=re.compile('src=\'http://embed.movshare.net/embed.php[?]v=([^"]*)&width=[^"]*&height=[^"]*&color=[^"]*\' scrolling=\'no\'></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.movshare.net/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src="http://embed.videoweed.es/embed.php[?]v=([^"]*)&width=[^"]*&height=[^"]*" scrolling="no"></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.videoweed.es/file/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src=\'http://embed.novamov.com/embed.php[?]width=[^"]*&height=[^"]*&v=([^"]*)&px=1\' scrolling=\'no\'></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.novamov.com/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)         
        match=re.compile('src=\'http://embed.nowvideo.sx/embed.php[?]width=[^"]*&height=[^"]*&v=([^"]*)\' scrolling=\'no\'></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.nowvideo.sx/video/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)         
        
        match=re.compile('src="http://www.putlocker.com/embed/([^"]*)" width="[^"]*" height="[^"]*" frameborder="0" scrolling="no"></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.firedrive.com/file/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)
        match=re.compile('src="http://www.sockshare.com/embed/([^"]*)" width="[^"]*" height="[^"]*" frameborder="0" scrolling="no"></iframe></textarea>').findall(link)
        for url in match:
                url = 'http://www.sockshare.com/file/' + url 
                hosted_media = urlresolver.HostedMediaFile(url=url)
                sources.append(hosted_media)        
        match=re.compile('href="http://mightyupload.com/embed-([^"]*)-.+?"><img src').findall(link)
        for url in match:
                url = 'http://mightyupload.com/' + url 
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





################################################


def GRABADULT(url):
    link=main.ADULT_URL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('<img src=images/star.gif>','').replace('player=2','').replace('play.','').replace('embed.','')
    matchname=re.compile('<div align="left"><strong>Watch ([^"]*) on:</strong></div>').findall(link)
    for name in matchname:
     match=re.compile('<a id="link-[^"]*" href="info.php[?]id=([^"]*)&([^"]*)&link=([^"]*)&host=[^"]*"><div class="[^"]*"><span class="([^"]*)"></span></div><div class="[^"]*">([^"]*)</div>').findall(link)
     for link1,age,link2,quality,host in match:
      url = MainUrl+ 'player.php?authid=&id='+link1+'&link='+link2+'&type=older_v2&part=&site=inactive&ref=1'
      main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,91,'.png','.png')

      

def ADULTGENRE(url):
        link=main.ADULT_GENRE(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('&#x27;',"'")
        match=re.findall('class="item"><a href="([^"]*)"><img alt=".+?src="([^"]*)" /></a><div class="title"><a title="watch movie([^"]*)" href=".+?<div class="year"> ([^"]*)</div>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Adult list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Adult List loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,date in match:
                main.addDir(name+'[COLOR blue] '+date+'[/COLOR]',MainUrl+url,51,thumb,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Adult List loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        pagenext=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
        if pagenext:
          url = 'http://megabox.li/index.php' + pagenext[0]
          main.addDir('[COLOR red]Next Page ->[/COLOR]',url,17,art+'/next.jpg')        
      














