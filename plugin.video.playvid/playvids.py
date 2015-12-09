'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib, urllib2, re, cookielib, os.path, sys, socket
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import json

import utils

# 522 Main
# 523 List
# 524 Playvid
# 525 Search
# 526 Cat

main_url = 'https://www.playvids.com/' 

def Main():
    utils.addDir('[COLOR yellow]Search[/COLOR]','https://www.playvids.com/sq?q=/',525,'','')
    utils.addDir('[COLOR yellow]HD[/COLOR]','https://www.playvids.com/top',523,'','')
    utils.addDir('[COLOR yellow]Top Rated[/COLOR]','https://www.playvids.com/hd',523,'','')
    utils.addDir('[COLOR yellow]Categories[/COLOR]','https://www.playvids.com/categories',526,'','')
    List('https://www.playvids.com')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def List(url):
    listhtml = utils.getHtml2(url)
    listhtml = utils.unescapes(listhtml)
    match = re.compile('data-href.+?title="([^"]*?)"><span class="image"><a href="([^"]*?)" class="ajax"><img src="([^"]*?)"></a>.+?<span class="duration">([^"]*?)</span>', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for name,url,thumb,duration in match:
        name = utils.cleantext(name)
        name = name + " [COLOR blue]" + duration + "[/COLOR]"
        url = main_url + url
        utils.addDownLink(name, url, 524, thumb, '')

    matchnext = re.findall('class="next ajax" href="([^"]*?)">Next</a>',listhtml)
    for url in matchnext:
     url = main_url + url
     utils.addDir('Next Page >', url, 523, '', '')
    xbmcplugin.endOfDirectory(utils.addon_handle)

##################################################    

def Playvid(url, name, download=None):
    listhtml = utils.getHtml2(url)
    listhtml = utils.unescapes(listhtml)
    match480 = re.search(r'[[]480p[]]=([^"]*?)&video_vars', listhtml)
    if match480: videourl = match480.group(1)
    else:
     match360 = re.search(r'[[]360p[]]=([^"]*?)&video_vars', listhtml)
     videourl = match360.group(1)
     
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        listitem.setProperty("IsPlayable","true")
        if int(sys.argv[1]) == -1:
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            pl.clear()
            pl.add(videourl, listitem)
            xbmc.Player().play(pl)
        else:
            listitem.setPath(str(videourl))
            xbmcplugin.setResolvedUrl(utils.addon_handle, True, listitem)
        return

def Cat(url):
        listhtml = utils.getHtml(url,'')
        listhtml = utils.unescapes(listhtml)
        match = re.findall('data-url="([^"]*?)".+?data-image="([^"]*?)".+?ajax overlay" href=".+?" title="([^"]*?)"></a></div>', listhtml)
        for url,thumb,name in match:
         utils.addDir(name,url,523,thumb)
         

def Search(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title 
    print "Searching URL: " + searchUrl
    List(searchUrl)
