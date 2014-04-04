#-*- coding: utf-8 -*-
import urllib,re,sys,os,urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import urlresolver
from BeautifulSoup import MinimalSoup as BeautifulSoup
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
net = Net()
reload(sys)
sys.setdefaultencoding( "UTF-8" )


#Megabox - by Kasik 2013.

addon_id = 'plugin.video.megabox'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
base_url='http://megabox.li/'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

######################################################################################################################
def addDir(name, url, mode, iconimage, metainfo=False, total=False, season=None):
         meta = metainfo
         ###  addDir with context menus and meta support  ###

         #encode url and name, so they can pass through the sys.argv[0] related strings
         sysname = urllib.quote_plus(name)
         sysurl = urllib.quote_plus(url)
         dirmode=mode
         
         #get nice unicode name text.
         #name has to pass through lots of weird operations earlier in the script,
         #so it should only be unicodified just before it is displayed.
         #name = htmlcleaner.clean(name)
         
         
         u = sys.argv[0] + "?url=" + sysurl + "&mode=" + str(mode) + "&name=" + sysname + "&season="+str(season)
         ok = True
         
         if meta is not False:
             print str(meta)
         #handle adding context menus
         contextMenuItems = []
         contextMenuItems.append(('Show Information', 'XBMC.Action(Info)',))
         
         #handle adding meta
         if meta == False:
             liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
             liz.setInfo(type="Video", infoLabels={"Title": name})

         else:
             
             if meta.has_key('watched') == False :
                 meta['watched']=6
                 
             liz = xbmcgui.ListItem(name, iconImage=str(meta['cover_url']), thumbnailImage=str(meta['cover_url']))


             liz.setInfo('video', infoLabels=meta)
             liz.setProperty('fanart_image', meta['backdrop_url'])

                
             infoLabels = {}
             infoLabels['title'] = name
             infoLabels['plot'] = cleanUnicode(meta['plot']) # to-check if we need cleanUnicode
             infoLabels['duration'] = str(meta['duration'])
             infoLabels['premiered'] = str(meta['premiered'])
             infoLabels['mpaa'] = str(meta['mpaa'])
             infoLabels['code'] = str(meta['imdb_id'])
             infoLabels['rating'] = float(meta['rating'])
             infoLabels['overlay'] = meta['watched'] # watched 7, unwatched 6

            
             
             try:
                     trailer_id = re.match('^[^v]+v=(.{11}).*', meta['trailer_url']).group(1)
                     infoLabels['trailer'] = "plugin://plugin.video.youtube/?action=play_video&videoid=%s" % trailer_id
             except:
                     infoLabels['trailer'] = ''
             
             if meta.has_key('season_num'):
                 infoLabels['Episode'] = int(meta['episode_num'])
                 infoLabels['Season'] =int(meta['season_num'])
                 print 'No refresh for episodes yet'
                   
             
             liz.setInfo(type="Video", infoLabels=infoLabels)
                           
         if contextMenuItems:
             #print str(contextMenuItems)
             liz.addContextMenuItems(contextMenuItems, replaceItems=True)
         #########

         print '          Mode=' + str(mode) + ' URL=' + str(url)
         #Do some crucial stuff
         if total is False:
             ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
         else:
             ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True, totalItems=int(total))
         return ok
######################################################################################################################




def MOVIES(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match = re.findall('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div><ul class=\'star-rating\'><li class="current-rating" style="[^"]*"></li></ul><div class="item-genres"><a href="[^"]*">([^"]*)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre in match:
                name=name.replace('-','').replace('&','').replace('acute;','').strip()
                main.addInfo(name+'[COLOR blue] Genre: '+genre+'[/COLOR]',base_url+url,8,thumb,genre,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        
        
        nextpage=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
        for url in nextpage:
                main.addDir('Next Page >>',base_url+url,1,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()

def YOUTUBE(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match = re.findall('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div><ul class=\'star-rating\'><li class="current-rating" style="[^"]*"></li></ul><div class="item-genres"><a href="[^"]*">([^"]*)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre in match:
                name=name.replace('-','').replace('&','').replace('acute;','').strip()
                main.addDir(name+'[COLOR blue] Genre: '+genre+'[/COLOR]',base_url+url,8,thumb,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        
        
        nextpage=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
        for url in nextpage:
                main.addDir('Next Page >>',base_url+url,50,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()        


def TV(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match = re.findall('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div><ul class=\'star-rating\'><li class="current-rating" style="[^"]*"></li></ul><div class="item-genres"><a href="[^"]*">([^"]*)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre in match:
                name=name.replace('-','').replace('&','').replace('acute;','').strip()
                main.addDir('[COLOR green]'+name+'[/COLOR]'+'[COLOR blue] Genre: '+genre+'[/COLOR]',base_url+url,12,thumb,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        
        
        nextpage=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
        for url in nextpage:
                main.addDir('[COLOR aqua]'+'Next Page >>'+'[/COLOR]',base_url+url,11,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def Seasons(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<h2>Season ([^"]*)</h2>').findall(link)
        #match.sort() # sort list so it shows season one first
        #match = f7(match)
        for season in match:
                print 'SeAsOn:'+season
                #main.addDir("Season "+season,url,13,'','')
                addDir('[COLOR blue]'+'SEASON '+season+'[/COLOR]',url,13,'',season=season)
        
def Episodes(url,season):
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read().replace('&#039;',"'")
        response.close()
        season = str(season)
        print 'SeaSon:'+season
        match=re.compile('<a href="info.php[?]id=([^"]*)&season='+season+'&episode=([^"]*)&tv">[^"]*<span class="ep_title">([^"]*)</span> <span class="total">([^"]*)</span>').findall(link)
        #match.sort() # sort list so it shows first episode first
     
        for linkid,episode,title,links in match:
                url = base_url + 'info.php?id='+linkid+'&season='+season+'&episode='+episode+'&tv'
                name = '[COLOR green]'+"Episode "+episode + '[/COLOR] ' + '[COLOR aqua]'+title + '[/COLOR]  ' + '[COLOR red]' +links+'[/COLOR]'
                main.addDir(name,url,14,'','')




                
def Season2(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=2&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season3(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=3&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season4(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=4&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season5(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=5&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season6(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=6&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season7(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=7&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season8(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=8&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season9(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=9&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season10(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=10&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season11(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=11&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season12(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=12&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season13(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=13&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season14(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=14&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season15(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=15&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season16(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=16&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season17(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=17&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season18(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=18&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season19(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=19&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season20(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=20&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season21(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=21&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season22(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=22&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season23(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=23&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season24(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=24&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season25(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=25&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')
def Season65(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=65&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')

def Season2013(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=2013&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=2013&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')

def Season2012(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=2012&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=2012&episode='+episode+'&tv'
                main.addDir(name,url,14,'','')                

def GRABTVLINKS(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('<img src=images/star.gif>','')
        match = re.findall('<a id="link-[^"]*" href="info.php[?]id=([^"]*)&season=[^"]*&episode=[^"]*&tv&link=([^"]*)&host=([^"]*)">',link)
        for link1,link2,host in match:
                name=host
                url = base_url + 'player.php?authid=&id='+link1+'&link='+link2+'&type=tv2'
                main.addDown2('[COLOR yellow]'+name+'[/COLOR]',url,6,'','')
                xbmcplugin.setContent(int(sys.argv[1]), 'Shows')

                
def TVVIDEOLINKS(url):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    match=re.compile('<strong>Watch [^"]* on ([^"]*) </strong></span><div class="clear"></div></div><div class="player"><a href="player5.php[?]id=([^"]*)&movie=[^"]*&episode=[^"]*&link=([^"]*)&type=tv2&ref=1" target').findall(link)
    for name,link1,link2 in match:
     url = base_url + 'player.php?authid=&id='+link1+'&link='+link2+'&type=tv2&part=&site=inactive&ref=1'
     print url
     name = '[COLOR yellow]'+name+'[/COLOR]'
     main.addDown2(name,url,6,'','')                   
                


  

def GRABLINKS(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('<img src=images/star.gif>','')
        match=re.compile('id="link-[^"]*" href="info.php[?]id=([^"]*)&older&link=([^"]*)&host=([^"]*)">').findall(link)
        for link1,link2,name in match:
         #url = base_url + 'player.php?authid=&id='+link1+'&link='+link2+'&type=older_v2&part=&site=inactive&ref=1'
         url = base_url + 'player.php?authid=&id='+link1+'&link='+link2+'&type=older_v2&ref=1'
         main.addDown2('[COLOR yellow]'+name+'[/COLOR]',url,6,'','')         
               
                           


def VIDEOLINKS(name,url):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    match=re.compile('<strong>Watch [^"]* on ([^"]*)</strong></span><div class="clear"></div></div><div class="player"><a href="player5.php[?]id=([^"]*)&movie=[^"]*&link=([^"]*)&type=([^"]*)&ref=1" target').findall(link)    
    #match=re.compile('<strong>Watch [^"]* on ([^"]*) </strong></span><div class="clear"></div></div><div class="player"><a href="[^"]*.php[?]id=([^"]*)&movie=[^"]*&link=([^"]*)&type=older_v2&ref=1" target').findall(link)
    for name,link1,link2,types in match:
     url = base_url + 'player.php?authid=&id='+link1+'&link='+link2+'&type='+types+'&part=&site=inactive&ref=1'
     print url
     name = '[COLOR yellow]'+name+'[/COLOR]'
     main.addDown2(name,url,6,'','')
    match1=re.compile('href="info.php[?]id=([^"]*)&older&link=([^"]*)">Part 1</a>').findall(link)
    for link1,link2 in match1:
     url = base_url + 'player.php?authid=&id='+link1+'&link='+link2+'&type=older_v2&part=&site=inactive&ref=1'
     print url
     name = '[COLOR yellow]Part 1''[/COLOR]'
     main.addDown2(name,url,6,'','')
    match2=re.compile('href="info.php[?]id=([^"]*)&older&link=([^"]*)&part=2">Part 2</a>').findall(link)
    for link1,link2 in match2:
     url = base_url + 'player.php?authid=&id='+link1+'&link='+link2+'&type=older_v2&part=&site=inactive&ref=1'
     print url
     name = '[COLOR yellow]Part 2''[/COLOR]'
     main.addDown2(name,url,6,'','') 
    
      
      

def GRABMORE(name,url):
     link=main.OPENURL(url)
     link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
     match=re.compile('<div class="player"><a href="player5.php[?]id=([^"]*)&movie=[^"]*&link=([^"]*)&type=older_v2&ref=1" target').findall(link)
     for link1,link2 in match:
      url = base_url + 'player.php?authid=&id='+link1+'&link='+link2+'&type=tv2&part=&site=inactive&ref=1'
      print url
      main.addDown2(name,url,6,'','')
     match2=re.compile('<div class="player"><a href="player5.php[?]id=([^"]*)&movie=[^"]*&link=([^"]*)&type=older_v2&ref=1" target').findall(link)
     for link1,link2 in match2:
      url = base_url + 'player.php?authid=&id='+link1+'&link='+link2+'&type=tv2&part=&site=inactive&ref=1'
      print url
      main.addDown2(name,url,6,'','')   
        



def PLAY(name,url):
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

       




def Searchhistory():
    seapath=os.path.join(main.datapath,'Search')
    SeaFile=os.path.join(seapath,'SearchHistoryMB')
    if not os.path.exists(SeaFile):
        SEARCH()
    else:
        main.addDir('Search Movies','###',120,art+'/search.png')
        main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
        for seahis in reversed(searchis):
            url=seahis
            seahis=seahis.replace('%20',' ')
            main.addDir(seahis,url,120,thumb)

def Searchhistorytv():
    seapath=os.path.join(main.datapath,'Search')
    SeaFile=os.path.join(seapath,'SearchHistoryTv')
    if not os.path.exists(SeaFile):
        SEARCHTV()
    else:
        main.addDir('Search Tv Shows','###',135,art+'/search.png')
        main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
        for seahis in reversed(searchis):
            url=seahis
            seahis=seahis.replace('%20',' ')
            main.addDir(seahis,url,135,thumb)            

def SEARCH(url = ''):
        encode = main.updateSearchFile(url,'Movies')
        if not encode: return False   
        surl=base_url + 'index.php?search=' + encode + '&movie=&x=0&y=0'
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match = re.findall('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div><ul class=\'star-rating\'><li class="current-rating" style="[^"]*"></li></ul><div class="item-genres"><a href="[^"]*">([^"]*)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre in match:
                name=name.replace('-','').replace('&','').replace('acute;','').strip()
                main.addInfo(name+'[COLOR blue] Genre: '+genre+'[/COLOR]',base_url+url,8,thumb,genre,'')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False 
        dialogWait.close()
        del dialogWait
        
        nextpage=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
        for url in nextpage:
                main.addDir('Next Page >>',base_url+url,1,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()

def SEARCHTV(url = ''):
        encode = main.updateSearchFile(url,'TV')
        if not encode: return False   
        surl=base_url + 'index.php?search=' + encode + '&tv=&x=0&y=0'
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match = re.findall('<a href="([^"]*)"><img alt="[^"]*" src="([^"]*)" /></a><div class="title"><a title="[^"]*" href="[^"]*">([^"]*)</a></div><ul class=\'star-rating\'><li class="current-rating" style="[^"]*"></li></ul><div class="item-genres"><a href="[^"]*">([^"]*)</a>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,genre in match:
                name=name.replace('-','').replace('&','').replace('acute;','').strip()
                main.addDir(name+'[COLOR blue] Genre: '+genre+'[/COLOR]',base_url+url,12,'','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False 
        dialogWait.close()
        del dialogWait
        
        nextpage=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
        for url in nextpage:
                main.addDir('Next Page >>',base_url+url,1,art+'/next.png')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        main.VIEWS()        


     



def PLAYB(name,url):
        ok=True
        hname=name
        name  = name.split('[COLOR blue]')[0]
        name  = name.split('[COLOR red]')[0]
        infoLabels = main.GETMETAT(name,'','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }

        try:
            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
            stream_url = main.resolve_url(url)

            infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
            # play with bookmark
            from universal import playbackengine
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                from universal import watchhistory
                wh = watchhistory.WatchHistory('plugin.video.megabox')
                wh.add_item(hname+' '+'[COLOR green]MegaBox[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
            player.KeepAlive()
            return ok
        except Exception, e:
            if stream_url != False:
                    main.ErrorReport(e)
            return ok

####################################
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

              
params=get_params()
url=None
name=None
mode=None
season=None

try:
        season=urllib.unquote_plus(params["season"])
except:
        pass
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Season: "+str(season)        
####################################        

     
