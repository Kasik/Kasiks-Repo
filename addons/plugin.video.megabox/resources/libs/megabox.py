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

def SEASONS(url,name):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        season1 = re.findall('<h2>Season 1</h2>',link)
        if len(season1) > 0:
               main.addDir('[COLOR orange]Season 1[/COLOR]',url,20,'','')
        season2 = re.findall('<h2>Season 2</h2>',link)
        if len(season2) > 0:
               main.addDir('[COLOR orange]Season 2[/COLOR]',url,21,'','')
        season3 = re.findall('<h2>Season 3</h2>',link)
        if len(season3) > 0:
               main.addDir('[COLOR orange]Season 3[/COLOR]',url,22,'','')
        season4 = re.findall('<h2>Season 4</h2>',link)
        if len(season4) > 0:
               main.addDir('[COLOR orange]Season 4[/COLOR]',url,23,'','')
        season5 = re.findall('<h2>Season 5</h2>',link)
        if len(season5) > 0:
               main.addDir('[COLOR orange]Season 5[/COLOR]',url,24,'','')
        season6 = re.findall('<h2>Season 6</h2>',link)
        if len(season6) > 0:
               main.addDir('[COLOR orange]Season 6[/COLOR]',url,25,'','')
        season7 = re.findall('<h2>Season 7</h2>',link)
        if len(season7) > 0:
               main.addDir('[COLOR orange]Season 7[/COLOR]',url,26,'','')
        season8 = re.findall('<h2>Season 8</h2>',link)
        if len(season8) > 0:
               main.addDir('[COLOR orange]Season 8[/COLOR]',url,27,'','')
        season9 = re.findall('<h2>Season 9</h2>',link)
        if len(season9) > 0:
               main.addDir('[COLOR orange]Season 9[/COLOR]',url,28,'','')
        season10 = re.findall('<h2>Season 10</h2>',link)
        if len(season10) > 0:
               main.addDir('[COLOR orange]Season 10[/COLOR]',url,29,'','')
        season11 = re.findall('<h2>Season 11</h2>',link)
        if len(season11) > 0:
               main.addDir('[COLOR orange]Season 11[/COLOR]',url,30,'','')
        season12 = re.findall('<h2>Season 12</h2>',link)
        if len(season12) > 0:
               main.addDir('[COLOR orange]Season 12[/COLOR]',url,31,'','')
        season13 = re.findall('<h2>Season 13</h2>',link)
        if len(season13) > 0:
               main.addDir('[COLOR orange]Season 13[/COLOR]',url,32,'','')
        season14 = re.findall('<h2>Season 14</h2>',link)
        if len(season14) > 0:
               main.addDir('[COLOR orange]Season 14[/COLOR]',url,33,'','')
        season15 = re.findall('<h2>Season 15</h2>',link)
        if len(season15) > 0:
               main.addDir('[COLOR orange]Season 15[/COLOR]',url,34,'','')
        season16 = re.findall('<h2>Season 16</h2>',link)
        if len(season16) > 0:
               main.addDir('[COLOR orange]Season 16[/COLOR]',url,35,'','')
        season17 = re.findall('<h2>Season 17</h2>',link)
        if len(season17) > 0:
               main.addDir('[COLOR orange]Season 17[/COLOR]',url,36,'','')
        season18 = re.findall('<h2>Season 18</h2>',link)
        if len(season18) > 0:
               main.addDir('[COLOR orange]Season 18[/COLOR]',url,37,'','')
        season19 = re.findall('<h2>Season 19</h2>',link)
        if len(season19) > 0:
               main.addDir('[COLOR orange]Season 19[/COLOR]',url,38,'','')
        season20 = re.findall('<h2>Season 20</h2>',link)
        if len(season20) > 0:
               main.addDir('[COLOR orange]Season 20[/COLOR]',url,39,'','')
        season21 = re.findall('<h2>Season 21</h2>',link)
        if len(season21) > 0:
               main.addDir('[COLOR orange]Season 21[/COLOR]',url,40,'','')
        season22 = re.findall('<h2>Season 22</h2>',link)
        if len(season22) > 0:
               main.addDir('[COLOR orange]Season 22[/COLOR]',url,41,'','')
        season23 = re.findall('<h2>Season 23</h2>',link)
        if len(season23) > 0:
               main.addDir('[COLOR orange]Season 23[/COLOR]',url,42,'','')
        season24 = re.findall('<h2>Season 24</h2>',link)
        if len(season24) > 0:
               main.addDir('[COLOR orange]Season 24[/COLOR]',url,43,'','')
        season25 = re.findall('<h2>Season 25</h2>',link)
        if len(season25) > 0:
               main.addDir('[COLOR orange]Season 25[/COLOR]',url,44,'','')
        season65 = re.findall('<h2>Season 65</h2>',link)
        if len(season65) > 0:
               main.addDir('[COLOR orange]Season 65[/COLOR]',url,45,'','')        

        season2013 = re.findall('<h2>Season 2013</h2>',link)
        if len(season2013) > 0:
               main.addDir('[COLOR orange]Season 2013[/COLOR]',url,46,'','')
        season2012 = re.findall('<h2>Season 2012</h2>',link)
        if len(season2012) > 0:
               main.addDir('[COLOR orange]Season 2012[/COLOR]',url,47,'','')       
        
        
        
def Season1(url):
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<div class=".*?"><a href="info.php[?]id=([^"]*)&season=1&episode=([^"]*)&tv">Episode .*?<span class="ep_title">([^"]*)</span> <span').findall(link)
        for showid,episode,name in match:
                name = '[COLOR green]'+"Episode "+ episode + "[/COLOR]" + '[COLOR teal]'+name+'[/COLOR]'
                url = base_url+'info.php?id='+showid+'&season=1&episode='+episode+'&tv'
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
        match = re.findall('<div id="links"><a href="([^"]*)"><div class="col1"><span class="([^"]*)"></span></div><div class="col2">([^"]*)</div><div class="col3">([^"]*)</di',link)
        for url,quality,host,views in match:
                name=host
                main.addDir('[COLOR green]'+name+'[/COLOR] [COLOR blue] Quality: '+quality+'[/COLOR] [COLOR orange]' ' Views: '+views+'[/COLOR]',base_url+url,15,'','')
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
        match=re.findall('<a href="([^"]*)"><div class="col1"><span class="([^"]*)"></span></div><div class="col2">([^"]*)</div><div class="col3">([^"]*)</div>',link)
        #match = re.findall('<div id="links"><a  href="([^"]*)"><div class="col1"><span class="([^"]*)"></span></div><div class="col2">([^"]*)</div><div class="col3">([^"]*) views</div>',link)
        for url,quality,host,views in match:
                name=host
                main.addDir('[COLOR green]'+name+'[/COLOR] [COLOR blue] Quality: '+quality+'[/COLOR] [COLOR orange]' ' Views: '+views+'[/COLOR]',base_url+url,3,'','')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        match = re.findall('<a class="active" href="([^"]*)"><div class="col1"><span class="([^"]*)"></span></div><div class="col2"> ([^"]*)</div><div class="col3">([^"]*)</div>',link)
        for url,quality,host,views in match:
                name=host
                main.addDir('[COLOR green]'+name+'[/COLOR] [COLOR blue] Quality: '+quality+'[/COLOR] [COLOR orange]' ' Views: '+views+'[/COLOR]',base_url+url,3,'','')
                xbmcplugin.setContent(int(sys.argv[1]), 'Movies')                

                           


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



     
