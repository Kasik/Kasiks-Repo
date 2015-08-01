'''
Created on 09 Jan 2011

@author: nteg
'''
import sys, os, time
import urllib
import xbmc, xbmcgui, xbmcaddon
from traceback import print_exc
from t0mm0.common.addon import Addon
selfAddon = xbmcaddon.Addon(id='plugin.video.couchtuner')
addon_path = selfAddon.getAddonInfo('path')
addon_id = 'plugin.video.couchtuner'
addon = Addon(addon_id)
class StopDownloading(Exception): 
    def __init__(self, value): 
        self.value = value 
    def __str__(self): 
        return repr(self.value)
  
uq_url  = urllib.unquote_plus(sys.argv[1])
uq_dest = urllib.unquote_plus(sys.argv[2])
uq_file = urllib.unquote_plus(sys.argv[3])
uq_Oname = urllib.unquote_plus(sys.argv[4])
NotifyPercent = int(sys.argv[5])

print uq_url
print uq_dest
print 'Setting NotifyPercent every : ' + str(NotifyPercent)
   
DeleteIncomplete = 'true'
#DeleteIncomplete=selfAddon.getSetting('delete-incomplete-downloads')
playFile = True

art = xbmc.translatePath('special://home/addons/plugin.video.couchtuner/resources/art/')
NotifyPercents = range(0, 100 + NotifyPercent, NotifyPercent)
start_time = time.time()
datapath = addon.get_profile()
DownloadLog=os.path.join(datapath,'Downloads')
try:
    os.makedirs(DownloadLog)
except:
    pass
DownloadFile=os.path.join(DownloadLog,'DownloadLog')

def xbmcpath(path,filename):
    translatedpath = os.path.join(xbmc.translatePath( path ), ''+filename+'')
    return translatedpath

def Notification(currentPercent):
    if currentPercent in NotifyPercents:
        #print '        Notified percent for file ' + uq_file
        #print NotifyPercents
        try: del NotifyPercents[NotifyPercents.index(currentPercent)]
        except: 
            print 'Could not clean Notified percents .....'
            pass
        
        icon_file =art+'/smallicon.png'
        print '        Download progress...' + str(currentPercent)+'% for file ' + uq_file
        xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i,%s)" % ( 'Download Progress - ' + str(currentPercent)+'%', uq_file, 5000,icon_file ) )

def progress(numblocks, blocksize, filesize, start_time):
    
    try:
        
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        ''' # keep this, we might need it, if we want to show more information in the notification
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0 
        kbps_speed = kbps_speed / 1024 
        total = float(filesize) / (1024 * 1024)
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
        e = 'Speed: %.02f Kb/s ' % kbps_speed 
        e += 'ETA: %02d:%02d' % divmod(eta, 60) 
        
        line2 = mbs + ' | ' + e
        '''
        
        Notification(percent)
        
    except:
        print_exc()


try: 
    urllib.urlretrieve(uq_url, uq_dest, lambda nb, bs, fs: progress(nb, bs, fs, start_time)) 
    open(DownloadFile,'a').write('{name="%s",destination="%s"}'%(uq_Oname,uq_dest))
except:
    if DeleteIncomplete == 'true':
        #delete partially downloaded file if setting says to.
        while os.path.exists(uq_dest): 
            try: 
                os.remove(uq_dest) 
                break 
            except: 
                pass
    
    # display error dialog
    dialog = xbmcgui.Dialog()
    dialog.ok('Error in download', 'There was an error downloading file ' + uq_file)
    
    #only handle StopDownloading (from cancel), ContentTooShort (from urlretrieve), and OS (from the race condition); let other exceptions bubble 
    if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): 
        print 'Error downloading'
        #return 'false' 
    else: 
        print 'Error downloading. Something else happened'
        raise 

# Display Download Complete dialog
dialog = xbmcgui.Dialog()
dialog.ok('Download Complete', 'Completed download of file ' + uq_file)
