# -*- coding: cp1252 -*-
# Main Module by: Blazetamer

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon
from metahandler import metahandlers

try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.pollystreaming'

addon = Addon(addon_id, sys.argv)
try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()
        

import threading

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer
import time

# Cache  
cache = StorageServer.StorageServer("pollystreaming", 0)
#=========Download Thread Module by: Blazetamer and o9r1sh1=========================
settings = xbmcaddon.Addon(id='plugin.video.pollystreaming')     
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')

print 'Mode is: ' + mode
print 'Url is: ' + url
print 'Name is: ' + name
print 'Thumb is: ' + thumb
print 'Extension is: ' + ext
print 'File Type is: ' + console
print 'DL Folder is: ' + dlfoldername
print 'Favtype is: ' + favtype
print 'Main Image is: ' + mainimg


download_path = settings.getSetting('download_folder')
artwork = xbmc.translatePath(os.path.join('http://rowthreemedia.com/xbmchub/2movies/art/', ''))
#================Threading===========================================


class downloadThread (threading.Thread):
    def __init__(self, name, url, thumb, console, ext):
        threading.Thread.__init__(self)
        self.thumb = thumb
          
    def run(self):
     queue = cache.get('queue')
  
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          for item in queue_items:
               self.name = item[0]
               self.url = item[1]
               self.ext = item[3]
               self.console = item[4]
               thumb = item[2]
                                
               self.path = download_path + self.console
               if not os.path.exists(self.path):
                    os.makedirs(self.path)
  
               self.file_name = self.name + self.ext
  
               addon.show_small_popup(title='[COLOR gold]Downloads Started[/COLOR]', msg=self.name + ' Is Downloading', delay=int(7000), image=thumb)
               u = urllib.urlopen(self.url)
               f = open(os.path.join(self.path,self.file_name), 'wb')
               meta = u.info()
               file_size = int(meta.getheaders("Content-Length")[0])
  
               file_size_dl = 0
               block_sz = 8192
  
               
                 
               while True:
                   buffer = u.read(block_sz)
                   if not buffer:
                       break
  
                   file_size_dl += len(buffer)
                   f.write(buffer)
                   status = int( file_size_dl * 1000. / file_size)
                  
                   if status > 99 and status < 101:
                         addon.show_small_popup(title=self.name, msg='10% Complete',delay=int(10), image=thumb)

                   elif status > 199 and status < 201:
                         addon.show_small_popup(title=self.name, msg='20% Complete',delay=int(10), image=thumb)
                         
                   elif status > 299 and status < 301:
                         addon.show_small_popup(title=self.name, msg='30% Complete',delay=int(10), image=thumb)

                   elif status > 399 and status < 401:
                         addon.show_small_popup(title=self.name, msg='40% Complete',delay=int(10), image=thumb)

                   elif status > 499 and status < 501:
                         addon.show_small_popup(title=self.name, msg='50% Complete',delay=int(10), image=thumb)

                   elif status > 599 and status < 601:
                         addon.show_small_popup(title=self.name, msg='60% Complete',delay=int(10), image=thumb)      
                   
                   elif status > 699 and status < 701:
                         addon.show_small_popup(title=self.name, msg='70% Complete',delay=int(10), image=thumb)

                   elif status > 799 and status < 801:
                         addon.show_small_popup(title=self.name, msg='80% Complete',delay=int(10), image=thumb)

                   elif status > 899 and status < 901:
                         addon.show_small_popup(title=self.name, msg='90% Complete',delay=int(10), image=thumb)

                   elif status > 994 and status < 996:
                         addon.show_small_popup(title=self.name, msg='95% Complete',delay=int(10), image=thumb)       
                   
                   
               f.close()
  
               removeFromQueue(self.name,self.url,thumb,self.ext,self.console)
  
  
               try:
                    addon.show_small_popup(title='[COLOR gold]Download Complete[/COLOR]', msg=self.name + ' Completed', delay=int(5000), image=thumb)
               except:
                    addon.show_small_popup(title='Error', msg=self.name + ' Failed To Download File', delay=int(5000), image=thumb)
                    print 'ERROR - File Failed To Download'
  
                 
               addon.show_small_popup(title='[COLOR gold]Process Complete[/COLOR]', msg=self.name + ' is in your downloads folder', delay=int(5000), image=thumb) 

               


############## End DownloadThread Class ################

def addQDir(name,url,mode,thumb,console):
     contextMenuItems = []

     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,'console':console, 'ext':ext}

     contextMenuItems.append(('[COLOR red]Remove From Queue[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removeFromQueue', 'name': name,'url': url,'thumb': thumb,'ext': ext,'console': console})))

     addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)
     
def addToQueue(name,url,thumb,ext,console):
     queue = cache.get('queue')
     queue_items = []
     if queue:
          queue_items = eval(queue)
          if queue_items:
               if (name,url,thumb,ext,console) in queue_items:
                    addon.show_small_popup(title='[COLOR red]Item Already In Your Queue[/COLOR]', msg=name + ' Is Already In Your Download Queue', delay=int(5000), image=thumb)
                    return
     queue_items.append((name,url,thumb,ext,console))         
     cache.set('queue', str(queue_items))
     addon.show_small_popup(title='[COLOR gold]Item Added To Your Queue [/COLOR]', msg=name + ' Was Added To Your Download Queue', delay=int(5000), image=thumb)

def viewQueue():
     addDir('[COLOR blue]Start Downloads[/COLOR]','none','download',artwork +'downloads/Downloads_Start.png','','')
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          for item in queue_items:
               addQDir(item[0],item[1],'viewQueue',item[2],item[4])

def KILLSLEEP(self):
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          for item in queue_items:
               self.name = item[0]
               self.url = item[1]
               self.ext = item[3]
               self.console = item[4]
               self.thumb = item[2]

               time.sleep(3)
     removeFromQueue(self.name,self.url,self.thumb,self.ext,self.console)
     
     
          
def removeFromQueue(name,url,thumb,ext,console):
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          try:
               queue_items.remove((name,url,thumb,'.mp4',console))
          except:
               try:
                    queue_items.remove((name,url,thumb,'.flv',console))
               except:
                    queue_items.remove((name,url,thumb,'.avi',console))
          cache.set('queue', str(queue_items))
          xbmc.executebuiltin("XBMC.Container.Refresh")


def download():
     download_path = settings.getSetting('download_folder')
     if download_path == '':
          addon.show_small_popup(title='File Not Downloadable', msg='You need to set your download folder in addon settings first', delay=int(5000), image='')
     else:
          #viewQueue()
          dlThread = downloadThread(name, url, thumb, console, ext)
          dlThread.start() 

                   

#=============END DLFUNCTION======================================================================================================================


     



# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)



def nameCleaner(name):
          name = name.replace('&#8211;','')
          name = name.replace("&#8217;","")
          name = name.replace("&#039;s","'s")
          #name = unicode(name, errors='ignore')
          return(name)
     


#Metadata    
grab=metahandlers.MetaData()

def GRABMETA(name,year):
        meta = grab.get_meta('movie',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                
        return infoLabels
        
        

def GRABTVMETA(name,year):
        meta = grab.get_meta('tvshow',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
        'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id'],'year': meta['year']}
                
        return infoLabels
        

def GRABEPISODEMETA(name,imdb_id,season,episode):
        meta = grab.get_episode_meta('tvshow',name,imdb_id,season,episode)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id']}
                
        return infoLabels
                


#Add Directory Stuff
def addDiralt(name,url,mode,thumb):
     name = nameCleaner(name)
     if thumb == '':
          thumb = artwork + '/main/noepisode.png'
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':'movie'}
     addon.add_directory(params, {'title':name}, img= thumb, fanart= artwork + '/main/fanart.jpg')



     
#******************For Movie Download*********************************
def addDLDir(name,url,mode,thumb,labels,dlfoldername,favtype,mainimg):
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype, 'mainimg':mainimg}
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dlvidpage', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)                             
       

#********************TV DOWNLOAD DIR***************************
def addTVDLDir(name,url,mode,thumb,labels,dlfoldername,favtype,mainimg):
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype,'mainimg':mainimg}
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dltvvidpage', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)
     
#*******************For Chia DownloadDir***********************
def addCHIADLDir(name,url,mode,thumb,labels,dlfoldername,favtype,mainimg):
        contextMenuItems = []
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype,'mainimg':mainimg}
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'chiadlvidpage', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)



     
#Resolve Movie DL Links******************************************
def RESOLVEDL(name,url,thumb):  
     data=0
     try:
          data = GRABMETA(movie_name,year)
     except:
           data=0
     hmf = urlresolver.HostedMediaFile(url)
     host = ''
     if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'
          if not ext == '':
          
          
               console = 'Downloads/Movies/'+ dlfoldername
               params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 
             

               xbmc.sleep(1000)
        
               addToQueue(name,url,thumb,ext,console)

#********Resolve TV DL Links*****************************************

def RESOLVETVDL(name,url,thumb):
         
     data=0
     try:
          data = GRABMETA(movie_name,year)
     except:
           data=0
     hmf = urlresolver.HostedMediaFile(url)
     host = ''
     if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'
          if not ext == '':
          
               console = 'Downloads/TV Shows/'+ dlfoldername
               params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 
     
               xbmc.sleep(1000)
        
               addToQueue(name,url,thumb,ext,console)
        
     
# HELPDIR



def addHELPDir(name,url,mode,iconimage,fanart,description,filetype):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def add2HELPDir(name,url,mode,iconimage,fanart,description,filetype):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok          

     
# Standard addDir
def addDir(name,url,mode,thumb,labels,favtype):
        contextMenuItems = []
        sitethumb = thumb
        sitename = name
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                
        if thumb == '':
                thumb = sitethumb
                
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('[COLOR gold]Movie Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'tvshow':
                contextMenuItems.append(('[COLOR gold]TV Show  Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'episode':
                contextMenuItems.append(('[COLOR gold]Episode  Information[/COLOR]', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
# AddDir for TV SHows to add a year forpass

def addTVDir(name,url,mode,thumb,labels,favtype,year):
        contextMenuItems = []
        sitethumb = thumb
        sitename = name 
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                
        if thumb == '':
                thumb = sitethumb
          
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&year="+urllib.quote_plus(year)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('[COLOR gold]Movie Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'tvshow':
                contextMenuItems.append(('[COLOR gold]TV Show  Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'episode':
                contextMenuItems.append(('[COLOR gold]Episode  Information[/COLOR]', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#Season Directory for TV Shows

def addSDir(name,url,mode,thumb,year,types,data):
     name = nameCleaner(name)
     contextMenuItems = []
     meta = {}
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':types, 'show':name}

     if settings.getSetting('metadata') == 'true':
          meta = grab.get_meta('tvshow',name)
          if meta['backdrop_url'] == '':
               fanart = artwork + 'fanart.jpg'
          else:
               fanart = meta['backdrop_url']
     else:
          fanart = artwork + 'fanart.jpg'
          

     if settings.getSetting('metadata') == 'true':
               if settings.getSetting('banners') == 'false':
                    if thumb == '':
                         thumb = meta['cover_url']
               else:
                    thumb = meta['banner_url']
     if thumb == '':
          thumb = artwork + 'noepisode.png'
     
     contextMenuItems.append(('[COLOR gold]Tv Show Information[/COLOR]', 'XBMC.Action(Info)'))

     
     if settings.getSetting('metadata') == 'true':
          addon.add_directory(params, meta, contextmenu_items=contextMenuItems, img=thumb, fanart=fanart)          
     else:
          addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb, fanart=fanart)     



# Episode add DirFunction 
def AaddEPDir(name,url,thumb,mode,show,dlfoldername,mainimg,season,episode):
        name = nameCleaner(name)
        contextMenuItems = []
        fullname = name
        ep_meta = None
        show_id = None
        meta = None
        othumb = thumb
        if settings.getSetting('metadata') == 'true':
          meta = grab.get_meta('tvshow',show)
          show_id = meta['imdb_id']
        else:
          fanart = artwork + 'fanart.jpg'
        s,e = GET_EPISODE_NUMBERS(name)
        if settings.getSetting('metadata') == 'true':
          try:
              ep_meta = grab.get_episode_meta(show,show_id,s,e)
              if ep_meta['cover_url'] == '':
                    thumb = mainimg
              else:
                    thumb = str(ep_meta['cover_url'])
          except:
               ep_meta=None
               thumb = mainimg
             
        else:
          thumb = othumb
          if thumb == '':
               thumb = mainimg
     
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':s, 'episode':e, 'show':show, 'types':'episode','dlfoldername':dlfoldername, 'mainimg':mainimg}        
        if settings.getSetting('metadata') == 'true':

          if ep_meta==None:
               fanart = artwork + 'fanart.jpg'
               addon.add_directory(params, {'title':name}, img=thumb, fanart=fanart) 
          else:
               if meta['backdrop_url'] == '':
                    fanart = artwork + 'fanart.jpg'
               else:
                    fanart = meta['backdrop_url']
               ep_meta['title'] = name
               addon.add_directory(params, ep_meta, fanart=fanart, img=thumb)
        else:
            addon.add_directory(params, {'title':name},fanart=fanart, img=thumb)
            

def addEPDir(name,url,thumb,mode,show,dlfoldername,mainimg,season,episode):
        #params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':s, 'episode':e, 'show':show, 'types':'episode','dlfoldername':dlfoldername, 'mainimg':mainimg}
        name = nameCleaner(name)
        contextMenuItems = []
        fullname = name
        ep_meta = None
        show_id = None
        meta = None
        othumb = thumb
        if settings.getSetting('metadata') == 'true':
          #meta = grab.get_meta('tvshow',dlfoldername,'',season,episode)
          inc = 0
          movie_name = show[:-6]
          year = show[-6:]
          print 'Meta Year is ' +year
          print 'Meta Name is ' +movie_name
          
              
          meta = GRABTVMETA(movie_name,year)
          thumb = meta['cover_url']               
          yeargrab = meta['year']
          year = str(yeargrab)       
          #meta = grab.get_meta('tvshow',name,'')
          show_id = meta['imdb_id']
          print 'IMDB ID is ' +show_id
        else:
          fanart = artwork + 'fanart.jpg'
        s,e = GET_EPISODE_NUMBERS(name)
        if settings.getSetting('metadata') == 'true':
          try:
              
              ep_meta = GRABEPISODEMETA(show_id,season,episode,'')
              if ep_meta['cover_url'] == '':
                    thumb = mainimg
              else:
                    thumb = str(ep_meta['cover_url'])
          except:
               ep_meta=None
               thumb = mainimg
             
        else:
          thumb = othumb
          if thumb == '':
               thumb = mainimg
     
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':season, 'episode':episode, 'show':show, 'types':'episode','dlfoldername':dlfoldername, 'mainimg':mainimg}        
        if settings.getSetting('metadata') == 'true':
         contextMenuItems.append(('[COLOR gold]Tv Show Information[/COLOR]', 'XBMC.Action(Info)'))
         if ep_meta==None:
               fanart = artwork + 'fanart.jpg'
               addon.add_directory(params, {'title':name},contextmenu_items=contextMenuItems, img=thumb, fanart=fanart) 
         else:
               if meta['backdrop_url'] == '':
                    fanart = artwork + 'fanart.jpg'
               else:
                    fanart = meta['backdrop_url']
               ep_meta['title'] = name
               addon.add_directory(params, ep_meta,contextmenu_items=contextMenuItems, fanart=fanart, img=thumb)
        else:
            addon.add_directory(params, {'title':name},contextmenu_items=contextMenuItems,fanart=fanart, img=thumb)            
     

#Host directory function for  Host Dir , hthumb =  host thumb and should be grabbed using the 'GETHOSTTHUMB(host)' function before 
def addHDir(name,url,mode,thumb,hthumb):
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':types, 'season':season, 'episode':episode, 'show':show}
     addon.add_directory(params, {'title':name}, img=hthumb, fanart=fanart)




#Resolve Functions
     
def RESOLVE(name,url,iconimage):
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         AUTO_VIEW('')

#Resolve 2

    

def RESOLVE2(name,url,thumb):
         
     
     data=0
     url = urlresolver.resolve(url)    
     params = {'url':url, 'name':name, 'thumb':thumb}
     if data == 0:
          addon.add_video_item(params, {'title':name}, img=thumb)
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)

     else:
          addon.add_video_item(params, {'title':name}, img=data['cover_url'])
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=data['cover_url'])
          liz.setInfo('video',infoLabels=data)

     xbmc.sleep(1000)
        
     xbmc.Player ().play(url, liz, False)

     

#AutoView
def AUTO_VIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        
                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('movies-view') )
                        if content == 'tvshows':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('tvshows-view') )

                        if content == 'episode':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('episode-view') )
                        if content == 'season':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('season-view') )
                        if content == 'list':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('list-view') )
                                
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )

        


     

#Returns the host thumbnail so that you can pass it as and argument 
def GETHOSTTHUMB(host):
     if host.endswith('.com'):
          host = host[:-4]
     if host.endswith('.org'):
          host = host[:-4]
     if host.endswith('.eu'):
          host = host[:-3]
     if host.endswith('.ch'):
          host = host[:-3]
     if host.endswith('.in'):
          host = host[:-3]
     if host.endswith('.es'):
          host = host[:-3]
     if host.endswith('.tv'):
          host = host[:-3]
     if host.endswith('.net'):
          host = host[:-4]
     if host.endswith('.me'):
          host = host[:-3]
     if host.endswith('.ws'):
          host = host[:-3]
     if host.endswith('.sx'):
          host = host[:-3]
     if host.startswith('www.'):
             host = host[4:]
     
     
     host = artwork + '/hosts/' + host +'.png'
     return(host)

#Episode directory function to be used when adding a Episode, all metadata scrapes and context menu items are handled within_________
def addEDir(name,url,mode,thumb,show):
     ep_meta = None
     show_id = None
     meta = None
     othumb = thumb
                
     if settings.getSetting('metadata') == 'true':
          data = GRABTVMETA('tvshow',show)
          

     else:
          fanart = artwork + '/main/fanart.jpg'
     
     s,e = GET_EPISODE_NUMBERS(name)

     if settings.getSetting('metadata') == 'true':
          try:
               ep_meta = GRABTVMETA(show,show_id,int(s),int(e))
               if ep_meta['cover_url'] == '':
                    thumb = artwork + '/main/noepisode.png'
               else:
                    thumb = str(ep_meta['cover_url'])
          except:
               ep_meta=None
               thumb = artwork + '/main/noepisode.png'
             
     else:
          thumb = othumb
          if thumb == '':
               thumb = artwork + '/main/noepisode.png'
     
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':s, 'episode':e, 'show':show, 'types':'episode'}        
     if settings.getSetting('metadata') == 'true':

          if ep_meta==None:
               fanart = artwork + '/main/fanart.jpg'
               addon.add_directory(params, {'title':name}, img=thumb, fanart=fanart) 
          else:
               if data['backdrop_url'] == '':
                    fanart = artwork + '/main/fanart.jpg'
               else:
                    fanart = data['backdrop_url']
               ep_meta['title'] = name
               addon.add_directory(params, ep_meta, fanart=fanart, img=thumb)
     else:
          addon.add_directory(params, {'title':name},fanart=fanart, img=thumb) 


#Called within the addEDir function, returns needed season and episode numbers needed for metadata scraping___________________________

def GET_EPISODE_NUMBERS(ep_name):
     s = None
     e = None
     ep_name = re.sub('×','X',ep_name)

     S00E00 = re.findall('[Ss]\d\d[Ee]\d\d',ep_name)
     SXE = re.findall('\d[Xx]\d',ep_name)
     SXEE = re.findall('\d[Xx]\d\d',ep_name)
     SXEEE = re.findall('\d[Xx]\d\d\d',ep_name)

     SSXE = re.findall('\d\d[Xx]\d',ep_name)
     SSXEE = re.findall('\d\d[Xx]\d\d',ep_name)
     SSXEEE = re.findall('\d\d[Xx]\d\d\d',ep_name)
     
     if S00E00:
          print 'Naming Style Is S00E00'
          S00E00 = str(S00E00)
          S00E00.strip('[Ss][Ee]')
          S00E00 = S00E00.replace("u","")
          e = S00E00[-4:]
          e = e[:-2]
          s = S00E00[:5]
          s = s[-2:]
          
     if SXE:
          print 'Naming Style Is SXE'
          SXE = str(SXE)
          SXE = SXE.replace("u","")
          print 'Numer String is ' + SXE
          s = SXE[2]
          e = SXE[4]

     if SXEE:
          print 'Naming Style Is SXEE'
          SXEE = str(SXEE)
          SXEE = SXEE.replace("u","")
          print 'Numer String is ' + SXEE
          s = SXEE[2]
          e = SXEE[4] + SXEE[5]

     if SXEEE:
          print 'Naming Style Is SXEEE'
          SXEEE = str(SXEEE)
          SXEEE = SXEEE.replace("u","")
          print 'Numer String is ' + SXEEEE
          s = SXEEE[2]
          e = SXEEE[4] + SXEEE[5] + SXEEE[6]

     if SSXE:
          print 'Naming Style Is SSXE'
          SSXE = str(SSXE)
          SSXE = SSXE.replace("u","")
          print 'Numer String is ' + SSXE
          s = SSXE[2] + SSXE[3]
          e = SSXE[5]

     if SSXEE:
          print 'Naming Style Is SSXEE'
          SSXEE = str(SSXEE)
          SSXEE = SSXEE.replace("u","")
          print 'Numer String is ' + SSXEE
          s = SSXEE[2] + SSXEE[3]
          e = SSXEE[5] + SSXEE[6]

     if SSXEEE:
          print 'Naming Style Is SSXEEE'
          SSXEEE = str(SSXEEE)
          SSXEEE = SSXEEE.replace("u","")
          print 'Numer String is ' + SSXEEE
          s = SSXEEE[2] + SSXEE[3]
          e = SSXEEE[5] + SSXEEE[6] + SSXEEE[7]

     return s,e




                              



