#-*- coding: utf-8 -*-
import urllib,re,sys,os,urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import main
import urlresolver

#Megabox - by Kasik04a 2052.

addon_id = 'plugin.video.megabox'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
MainUrl='http://megashare.li/'
prettyName='Megabox'

def TV(url):
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match = re.findall('class="item"><a href="([^"]*)"><img alt=".+?src="([^"]*)" /></a><div class="title"><a title="watch tv([^"]*)" href=".+?<div class="year"> ([^"]*)</div>',link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Shows list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0, '[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,date in match:
                main.addDirTE(name+' '+date,MainUrl+url,22,thumb,'','','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Shows loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        
        nextpage=re.compile('<a href="([^"]*)" class="next">Next &#187;</a>').findall(link)
        for url in nextpage:
                main.addDir('[COLOR aqua]'+'Next Page >>'+'[/COLOR]',MainUrl+url,11,art+'/next.jpg')
                
        xbmcplugin.setContent(int(sys.argv[1]), 'TV')
        main.VIEWS()


def TVGENRES(url,index=False):
    link=main.OPENURL(url)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match = re.findall('<a href="[?]genre=([^"]*)">([^"]*)</a></li>',link)
    for url,name in match:
     url = MainUrl + '?genre=' + url
     main.addDir(name,url,11,'','')





################################################################################################################################################
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def Seasons(url,name):
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<h2>Season ([^"]*)</h2>').findall(link)
        #match.sort() # sort list so it shows season one first
        #match = f7(match)
        for season in match:
                #main.addDir("Season "+season,url,13,'','')
                main.addDirG('[COLOR blue]'+'SEASON '+season+'[/COLOR]',url,23,'',season=season)


        
def Episodes(url,season):
        link=main.OPEN_URL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        season = str(season)
        match=re.compile('<a href="info.php[?]id=([^"]*)&season='+season+'&episode=([^"]*)&tv">[^"]*<span class="ep_title">([^"]*)</span>').findall(link)
        #match.sort() # sort list so it shows first episode first
     
        for linkid,episode,title in match:
                url = MainUrl + 'info.php?id='+linkid+'&season='+season+'&episode='+episode+'&tv'
                name = '[COLOR green]'+"Episode "+episode + '[/COLOR] ' + '[COLOR aqua]'+title + '[/COLOR]  '
                main.addDir(name,url,52,'','')







def GRABTVLINKS(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('<img src=images/star.gif>','')
        matchname=re.compile('div align="left"><strong>Watch ([^"]*) on:</strong>').findall(link)
        for name in matchname:
         match = re.findall('<a id="link-[^"]*" href="info.php[?]id=([^"]*)&season=[^"]*&episode=[^"]*&tv&link=([^"]*)&host=([^"]*)">',link)
         for link1,link2,host in match:
                url = MainUrl + 'player.php?authid=&id='+link1+'&link='+link2+'&type=tv2'
                main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,90,'.png','.png')
                xbmcplugin.setContent(int(sys.argv[1]), 'Shows')






def SearchhistoryTV(index=False):
    seapath=os.path.join(main.datapath,'Search')
    SeaFile=os.path.join(seapath,'SearchHistoryTV')
    if not os.path.exists(SeaFile):
        SEARCHTV(index=index)
    else:
        main.addDir('Search','###',15,art+'/search.png',index=index)
        main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
        for seahis in reversed(searchis):
            url=seahis
            seahis=seahis.replace('%20',' ')
            main.addDir(seahis,url,15,thumb,index=index)
            
def SEARCHTV(murl = '',index=False):
    encode = main.updateSearchFile(murl,'Shows')
    if not encode: return False   
    surl='http://megashare.li/index.php?search='+encode+'&tv=&x=0&y=0'
    link=main.OPENURL(surl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('class="item"><a href="([^"]*)"><img alt=".+?src="([^"]*)" /></a><div class="title"><a title="watch tv([^"]*)" href=".+?<div class="year"> ([^"]*)</div>').findall(link)
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
        main.addDirTE(name+'[COLOR blue] '+date +'[/COLOR]',furl,22,thumb,'','','','','')
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if dialogWait.iscanceled(): return False 
    dialogWait.close()
    del dialogWait
    exist = re.findall('<a href="([^"]*)" class="next">Next &#187;</a>',link)
    if exist:
        main.addDir('[COLOR blue]Next Page ->[/COLOR]',MainUrl+url,15,art+'/next.jpg',index=index)
        
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')








