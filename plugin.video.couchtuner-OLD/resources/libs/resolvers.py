# -*- coding: cp1252 -*-
import urllib,urllib2,re,cookielib,string,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from t0mm0.common.net import Net as net

addon_id = 'plugin.video.couchtuner'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
elogo = xbmc.translatePath('special://home/addons/plugin.video.couchtuner/resources/art/bigx.png')

class ResolverError(Exception):
    def __init__(self, value, value2):
        value = value
        value2 = value2
    def __str__(self):
        return repr(value,value2)

def resolve_url(url, filename = False):
    stream_url = False
    if(url):
        try:
            url = url.split('"')[0]
            match = re.search('xoxv(.+?)xoxe(.+?)xoxc',url)
            print "host "+url
            if(match):
                import urlresolver
                source = urlresolver.HostedMediaFile(host=match.group(1), media_id=match.group(2))
                if source:
                    stream_url = source.resolve()
            elif re.search('billionuploads',url,re.I):
                stream_url=resolve_billionuploads(url, filename)
            elif re.search('180upload',url,re.I):
                stream_url=resolve_180upload(url)
            elif re.search('veehd',url,re.I):
                stream_url=resolve_veehd(url)
            elif re.search('vidto',url,re.I):
                stream_url=resolve_vidto(url)
            elif re.search('epicshare',url,re.I):
                stream_url=resolve_epicshare(url)
            elif re.search('lemuploads',url,re.I):
                stream_url=resolve_lemupload(url)
            elif re.search('mightyupload',url,re.I):
                stream_url=resolve_mightyupload(url)               
            elif re.search('hugefiles',url,re.I):
                stream_url=resolve_hugefiles(url)
            elif re.search('megarelease',url,re.I):
                stream_url=resolve_megarelease(url)
            elif re.search('movreel',url,re.I):
                stream_url=resolve_movreel(url)
            elif re.search('bayfiles',url,re.I):
                stream_url=resolve_bayfiles(url)
            elif re.search('nowvideo',url,re.I):
                stream_url=resolve_nowvideo(url)
            elif re.search('novamov',url,re.I):
                stream_url=resolve_novamov(url)
            elif re.search('vidspot',url,re.I):
                stream_url=resolve_vidspot(url)
            elif re.search('videomega',url,re.I):
                stream_url=resolve_videomega(url)
            elif re.search('youwatch',url,re.I):
                stream_url=resolve_youwatch(url)
            elif re.search('vk.com',url,re.I):
                stream_url=resolve_VK(url)
            elif re.search('(?i)(firedrive|putlocker)',url):
                stream_url=resolve_firedrive(url)               
            elif re.search('project-free-upload',url,re.I):
                stream_url=resolve_projectfreeupload(url)
            elif re.search('yify.tv',url,re.I):
                stream_url=resolve_yify(url)
            elif re.search('mail.ru',url,re.I):
                stream_url=resolve_mailru(url)
            elif re.search('youtube',url,re.I):
                try:url=url.split('watch?v=')[1]
                except:
                    try:url=url.split('com/v/')[1]
                    except:url=url.split('com/embed/')[1]
                stream_url='plugin://plugin.video.youtube/?action=play_video&videoid=' +url
            else:
                import urlresolver
                print "host "+url
                source = urlresolver.HostedMediaFile(url)
                if source:
                    stream_url = source.resolve()
                    if isinstance(stream_url,urlresolver.UrlResolver.unresolvable):
                        showUrlResoverError(stream_url)
                        stream_url = False
                else:
                    stream_url=url
            try:
                stream_url=stream_url.split('referer')[0]
                stream_url=stream_url.replace('|','')
            except:
                pass
        except ResolverError as e:
            #logerror(str(e))
            #showpopup('[COLOR=FF67cc33]couchtuner URLresolver Error[/COLOR] ' + e.value2,'[B][COLOR red]'+e.value+'[/COLOR][/B]',5000, elogo)
            try:
                import urlresolver
                source = urlresolver.HostedMediaFile(url)
                if source:
                    stream_url = source.resolve()
                    if isinstance(stream_url,urlresolver.UrlResolver.unresolvable):
                        showUrlResoverError(stream_url)
                        stream_url = False
            except Exception as e:
                logerror(str(e))
                showpopup('[COLOR=FF67cc33]couchtuner URLresolver Error[/COLOR]','[B][COLOR red]'+str(e)+'[/COLOR][/B]',5000, elogo)
        except Exception as e:
            logerror(str(e))
            showpopup('[COLOR=FF67cc33]couchtuner URLresolver Error[/COLOR]','[B][COLOR red]'+str(e)+'[/COLOR][/B]',5000, elogo)
    else:
        logerror("video url not valid")
        showpopup('[COLOR=FF67cc33]couchtuner URLresolver Error[/COLOR]','[B][COLOR red]video url not valid[/COLOR][/B]',5000, elogo)
    if stream_url and re.search('\.(zip|rar|7zip)$',stream_url,re.I):
        logerror("video url found is an archive")
        showpopup('[COLOR=FF67cc33]couchtuner URLresolver Error[/COLOR]','[B][COLOR red]video url found is an archive[/COLOR][/B]',5000, elogo)
        return False
    return stream_url

def showUrlResoverError(unresolvable):
    logerror(str(unresolvable.msg))
    showpopup('[B]UrlResolver Error[/B]','[COLOR red]'+str(unresolvable.msg)+'[/COLOR]',10000, elogo)
def logerror(log):
    xbmc.log(log, xbmc.LOGERROR)
def showpopup(title='', msg='', delay=5000, image=''):
    xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")' % (title, msg, delay, image))
    
def grab_cloudflare(url):

    class NoRedirection(urllib2.HTTPErrorProcessor):
        # Stop Urllib2 from bypassing the 503 page.    
        def http_response(self, request, response):
            code, msg, hdrs = response.code, response.msg, response.info()

            return response
        https_response = http_response

    cj = cookielib.CookieJar()
    
    opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
    response = opener.open(url).read()
        
    jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
    if jschl:
        import time
        jschl = jschl[0]    
    
        maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')

        domain_url = re.compile('(https?://.+?/)').findall(url)[0]
        domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
        
        time.sleep(5)
        
        normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        normal.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
        final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
        
        response = normal.open(url).read()

    return response

def millis():
      import time as time_
      return int(round(time_.time() * 1000))
    
def load_json(data):
      def to_utf8(dct):
            rdct = {}
            for k, v in dct.items() :
                  if isinstance(v, (str, unicode)) :
                        rdct[k] = v.encode('utf8', 'ignore')
                  else :
                        rdct[k] = v
            return rdct
      try :        
            from lib import simplejson
            json_data = simplejson.loads(data, object_hook=to_utf8)
            return json_data
      except:
            try:
                  import json
                  json_data = json.loads(data, object_hook=to_utf8)
                  return json_data
            except:
                  import sys
                  for line in sys.exc_info():
                        print "%s" % line
      return None


def resolve_firedrive(url):
    try:
        url=url.replace('putlocker.com','firedrive.com').replace('putlocker.to','firedrive.com')
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner Firedrive Link...')       
        dialog.update(0)
        print 'couchtuner Firedrive - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        dialog.update(50)
        if dialog.iscanceled(): return None
        post_data = {}
        r = re.findall(r'(?i)<input type="hidden" name="(.+?)" value="(.+?)"', html)
        for name, value in r:
            post_data[name] = value
        post_data['referer'] = url
        html = net().http_POST(url, post_data).content
        embed=re.findall('(?sim)href="([^"]+?)">Download file</a>',html)
        if not embed:
            embed=re.findall('(?sim)href="(http://dl.firedrive.com[^"]+?)"',html)
        if dialog.iscanceled(): return None
        if embed:
            dialog.update(100)
            return embed[0]
        else:
            logerror('couchtuner: Resolve Firedrive - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,Firedrive,2000)")
            return False
    except Exception, e:
        logerror('**** Firedrive Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Firedrive[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

       
        
def resolve_bayfiles(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner Bayfiles Link...')       
        dialog.update(0)
        print 'couchtuner Bayfiles - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        try: vfid = re.compile('var vfid = ([^;]+);').findall(html)[0]
        except:pass
        try:urlpremium='http://'+ re.compile('<a class="highlighted-btn" href="http://(.+?)">Premium Download</a>').findall(html)[0]
        except:urlpremium=[]
        if urlpremium:
                return urlpremium
        else:
                try:
                    delay = re.compile('var delay = ([^;]+);').findall(html)[0]
                    delay = int(delay)
                except: delay = 300
                t = millis()
                html2 = net().http_GET("http://bayfiles.net/ajax_download?_=%s&action=startTimer&vfid=%s"%(t,vfid)).content
                datajson=load_json(html2)
                if datajson['set']==True:
                    token=datajson['token']
                    url_ajax = 'http://bayfiles.net/ajax_download'
                    post = "action=getLink&vfid=%s&token=%s" %(vfid,token)
                    finaldata=net().http_GET(url_ajax + '?' + post).content
                    patron = 'onclick="javascript:window.location.href = \'(.+?)\''
                    matches = re.compile(patron,re.DOTALL).findall(finaldata)
                    return matches[0] #final url mp4
    except:
        html = net().http_GET(url).content
        try:
                match2=re.compile('<div id="content-inner">\n\t\t\t\t<center><strong style="color:#B22B13;">Your IP (.+?) has recently downloaded a file. Upgrade to premium or wait (.+?) min.</strong>').findall(html)[0]
                raise ResolverError('You recently downloaded a file. Upgrade to premium or wait',"Bayfiles")
                return
        except:
                match3=re.compile('<div id="content-inner">\n\t\t\t\t<center><strong style="color:#B22B13;">Your IP (.+?) is already downloading. Upgrade to premium or wait.</strong>').findall(html)
                raise ResolverError('You are already downloading. Upgrade to premium or wait.',"Bayfiles")
                return

def resolve_mailru(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner MailRU Link...')       
        dialog.update(0)
        print 'couchtuner MailRU - Requesting GET URL: %s' % url
        link = net().http_GET(url).content
        match=re.compile('videoSrc = "(.+?)",',re.DOTALL).findall(link)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler())
        req = urllib2.Request(url)
        f = opener.open(req)
        html = f.read()
        for cookie in cj:
            cookie=str(cookie)

        rcookie=cookie.replace('<Cookie ','').replace(' for .video.mail.ru/>','')

        vlink=match[0]+'&Cookie='+rcookie
        return vlink
    except Exception, e:
        logerror('**** MailRU Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]MailRU[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)


def resolve_yify(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner Yify Link...')       
        dialog.update(0)
        print 'couchtuner Yify - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        url = re.compile('showPkPlayer[(]"(.+?)"[)]').findall(html)[0]
        url = 'http://yify.tv/reproductor2/pk/pk/plugins/player_p.php?url=https%3A//picasaweb.google.com/' + url
        html = net().http_GET(url).content
        html = re.compile('{(.+?)}').findall(html)[-1]
        stream_url = re.compile('"url":"(.+?)"').findall(html)[0]
        return stream_url
    except Exception, e:
        logerror('**** Yify Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Yify[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)


def resolve_VK(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner VK Link...')       
        dialog.update(0)
        print 'couchtuner VK - Requesting GET URL: %s' % url
        useragent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
        link2 = net(user_agent=useragent).http_GET(url).content
        if re.search('This video has been removed', link2, re.I):
            logerror('***** couchtuner VK - This video has been removed')
            xbmc.executebuiltin("XBMC.Notification(This video has been removed,VK,2000)")
            return False
        match = re.search('(?i)<source src="(.+?\.1080.mp4)"',link2)
        if not match:
            match = re.search('(?i)<source src="(.+?\.720.mp4)"',link2)
            if not match:
                match = re.search('(?i)<source src="(.+?\.480.mp4)"',link2)
                if not match:
                    match = re.search('(?i)<source src="(.+?\.360.mp4)"',link2)
                    if not match:
                        match = re.search('(?i)<source src="(.+?\.240.mp4)"',link2)
        if match: 
            return match.group(1).replace("\/",'/')
    except Exception, e:
        logerror('**** VK Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]VK[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

def resolve_youwatch(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner Youwatch Link...')       
        dialog.update(0)
        print 'couchtuner Youwatch - Requesting GET URL: %s' % url
        if 'embed' not in url:
            mediaID = re.findall('http://youwatch.org/([^<]+)', url)[0]
            url='http://youwatch.org/embed-'+mediaID+'.html'
        else:url=url
        html = net().http_GET(url).content
        try:
                html=html.replace('|','/')
                stream=re.compile('/mp4/video/(.+?)/(.+?)/(.+?)/setup').findall(html)
                for id,socket,server in stream:
                    continue
        except:
                raise ResolverError('This file is not available on',"Youwatch")
        stream_url='http://'+server+'.youwatch.org:'+socket+'/'+id+'/video.mp4?start=0'
        return stream_url
    except Exception, e:
        logerror('**** Youwatch Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Youwatch[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)


def resolve_projectfreeupload(url):
    try:
        import jsunpack
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner Project Free Link...')       
        dialog.update(0)
        print 'couchtuner Project Free - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        r = re.findall(r'\"hidden\"\sname=\"?(.+?)\"\svalue=\"?(.+?)\"\>', html, re.I)
        post_data = {}
        for name, value in r:
            post_data[name] = value
        post_data['referer'] = url
        post_data['method_premium']=''
        post_data['method_free']=''
        html = net().http_POST(url, post_data).content
        embed=re.findall('<IFRAME SRC="(.+?)"',html)
        html = net().http_GET(embed[0]).content
        r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?)</script>',html,re.M|re.DOTALL)
        try:unpack=jsunpack.unpack(r[1])
        except:unpack=jsunpack.unpack(r[0])
        stream_url=re.findall('<param name="src"value="(.+?)"/>',unpack)[0]
        return stream_url
        if dialog.iscanceled(): return None
    except Exception, e:
        logerror('**** Project Free Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Project Free[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

def resolve_videomega(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner Videomega Link...')       
        dialog.update(0)
        print 'couchtuner Videomega - Requesting GET URL: %s' % url
        try:
            mediaID = re.findall('http://videomega.tv/.?ref=([^<]+)', url)[0]
            url='http://videomega.tv/iframe.php?ref='+mediaID
        except:url=url
        html = net().http_GET(url).content
        try:
                encodedurl=re.compile('unescape.+?"(.+?)"').findall(html)
        except:
                raise ResolverError('This file is not available on',"VideoMega")
        url2=urllib.unquote(encodedurl[0])
        stream_url=re.compile('file: "(.+?)"').findall(url2)[0]
        return stream_url
    except Exception, e:
        logerror('**** Videomega Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Videomega[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)
    
def resolve_vidspot(url):
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner Vidspot Link...')       
        dialog.update(0)
        print 'couchtuner Vidspot - Requesting GET URL: %s' % url
        mediaID=re.findall('http://vidspot.net/([^<]+)',url)[0]
        url='http://vidspot.net/embed-'+mediaID+'.html'
        print url
        html = net().http_GET(url).content
        r = re.search('"file" : "(.+?)",', html)
        if r:
            stream_url = urllib.unquote(r.group(1))

        return stream_url

    except Exception, e:
        logerror('**** Vidspot Error occured: %s' % e)
        xbmc.executebuiltin('[B][COLOR white]Vidspot[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)

    
def resolve_novamov(url):
        try:
            import unwise
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving couchtuner Novamov Link...')       
            dialog.update(0)
            print 'couchtuner Novamov - Requesting GET URL: %s' % url
            html = net().http_GET(url).content
            html = unwise.unwise_process(html)
            
            filekey = unwise.resolve_var(html, "flashvars.filekey")
            media_id=re.findall('.+?/video/([^<]+)',url)
            #get stream url from api
            api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % (filekey, media_id)
            html = net().http_GET(api).content
            r = re.search('url=(.+?)&title', html)
            if r:
                stream_url = urllib.unquote(r.group(1))
            else:
                r = re.search('file no longer exists',html)
                if r:
                    raise ResolverError('File Not Found or removed',"Novamov")
                raise ResolverError('Failed to parse url',"Novamov")
                
            return stream_url
        except urllib2.URLError, e:
            logerror('Novamov: got http error %d fetching %s' %
                                    (e.code, web_url))
            return unresolvable(code=3, msg=e)
        except Exception, e:
            logerror('**** Novamov Error occured: %s' % e)
            xbmc.executebuiltin('[B][COLOR white]Novamov[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)
            return unresolvable(code=0, msg=e)

def resolve_nowvideo(url):
        try:
            import unwise
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving couchtuner Nowvideo Link...')       
            dialog.update(0)
            print 'couchtuner Nowvideo - Requesting GET URL: %s' % url
            html = net().http_GET(url).content
            html = unwise.unwise_process(html)
            
            filekey = unwise.resolve_var(html, "flashvars.filekey")
            try:media_id=re.findall('.+?/video/([^<]+)',url)[0]
            except:media_id=re.findall('http://embed.nowvideo.+?/embed.php.?v=([^<]+)',url)[0]
            #get stream url from api
            api = 'http://www.nowvideo.sx/api/player.api.php?key=%s&file=%s' % (filekey, media_id)
            html = net().http_GET(api).content
            r = re.search('url=(.+?)&title', html)
            if r:
                stream_url = urllib.unquote(r.group(1))
            else:
                r = re.search('file no longer exists',html)
                if r:
                    raise ResolverError('File Not Found or removed',"Nowvideo")
                raise ResolverError('Failed to parse url',"Nowvideo")
                
            return stream_url
        except urllib2.URLError, e:
            logerror('Nowvideo: got http error %d fetching %s' %
                                    (e.code, web_url))
            return unresolvable(code=3, msg=e)
        except Exception, e:
            logerror('**** Nowvideo Error occured: %s' % e)
            xbmc.executebuiltin('[B][COLOR white]Nowvideo[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, elogo)
            return unresolvable(code=0, msg=e)

def resolve_movreel(url):

    try:


        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner Movreel Link...')       
        dialog.update(0)
        
        print 'couchtuner Movreel - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        
        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** couchtuner Movreel - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable on the host,Movreel in maintenance,2000)")

        #Set POST data values
        op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        method_free = re.search('<input type="(submit|hidden)" name="method_free" (style=".*?" )*value="(.*?)">', html).group(3)
        method_premium = re.search('<input type="(hidden|submit)" name="method_premium" (style=".*?" )*value="(.*?)">', html).group(3)
        

        rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
        data = {'op': op, 'id': postid, 'referer': url, 'rand': rand, 'method_premium': method_premium}
        
        print 'couchtuner Movreel - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net().http_POST(url, data).content

        #Only do next post if Free account, skip to last page for download link if Premium
        if method_free:
            #Check for download limit error msg
            if re.search('<p class="err">.+?</p>', html):
                logerror('***** Download limit reached')
                errortxt = re.search('<p class="err">(.+?)</p>', html).group(1)
                xbmc.executebuiltin("XBMC.Notification("+errortxt+",Movreel,2000)")
    
            dialog.update(66)
            
            #Set POST data values
            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
    
            if r:
                for name, value in r:
                    data[name] = value
            else:
                logerror('***** couchtuner Movreel - Cannot find data values')
                xbmc.executebuiltin("XBMC.Notification(Unable to resolve Movreel Link,Movreel,2000)") 

            print 'couchtuner Movreel - Requesting POST URL: %s DATA: %s' % (url, data)
            html = net().http_POST(url, data).content

        #Get download link
        dialog.update(100)
        link = re.search('<a href="(.+)">Download Link</a>', html)
        if link:
            return link.group(1)
        else:
            xbmc.executebuiltin("XBMC.Notification(Unable to find final link,Movreel,2000)")

    except Exception, e:
        logerror('**** couchtuner Movreel Error occured: %s' % e)
        raise ResolverError(str(e),"Movreel")
    finally:
        dialog.close()

def resolve_megarelease(url):
    try:
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner MegaRelease Link...')
        dialog.update(0)
        
        print 'MegaRelease couchtuner - Requesting GET URL: %s' % url
        html = net().http_GET(url).content

        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** MegaRelease - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,MegaRelease in maintenance,2000)")                                
            return False
        if re.search('<b>File Not Found</b>', html):
            logerror('couchtuner: Resolve MegaRelease - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,MegaRelease,2000)")
            return False

        filename = re.search('You have requested <font color="red">(.+?)</font>', html).group(1)
        filename = filename.split('/')[-1]
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://megarelease.org/(.+)$', url).group(1)
        
        vid_embed_url = 'http://megarelease.org/vidembed-%s%s' % (guid, extension)
        UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
        ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', UserAgent)
        request.add_header('Accept', ACCEPT)
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        redirect_url = re.search('(http://.+?)video', response.geturl()).group(1)
        download_link = redirect_url + filename
        
        dialog.update(100)

        return download_link
        
    except Exception, e:
        logerror('**** couchtuner MegaRelease Error occured: %s' % e)
        raise ResolverError(str(e),"MegaRelease")
    finally:
        dialog.close()

def resolve_veehd(url):
    name = "veeHD"
    cookie_file = os.path.join(datapath, '%s.cookies' % name)
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    from random import choice
    userName = ['couchtuner1', 'couchtuner3', 'couchtuner4', 'couchtuner5', 'couchtuner6', 'couchtuner7']
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner VeeHD Link...')       
        dialog.update(0)
        loginurl = 'http://veehd.com/login'
        ref = 'http://veehd.com/'
        submit = 'Login'
        terms = 'on'
        remember_me = 'on'
        data = {'ref': ref, 'uname': choice(userName), 'pword': 'xbmcisk00l', 'submit': submit, 'terms': terms, 'remember_me': remember_me}
        html = net(user_agent).http_POST(loginurl, data).content
        if dialog.iscanceled(): return False
        dialog.update(33)
        net().save_cookies(cookie_file)
        headers = {}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'}
        net().set_cookies(cookie_file)
        print 'couchtuner VeeHD - Requesting GET URL: %s' % url
        html = net().http_GET(url, headers).content
        if dialog.iscanceled(): return False
        dialog.update(66)
        fragment = re.findall('playeriframe".+?attr.+?src : "(.+?)"', html)
        frag = 'http://%s%s'%('veehd.com',fragment[1])
        net().set_cookies(cookie_file)
        html = net().http_GET(frag, headers).content
        r = re.search('"video/divx" src="(.+?)"', html)
        if r:
            stream_url = r.group(1)
        if not r:
            print name + '- 1st attempt at finding the stream_url failed probably an Mp4, finding Mp4'
            a = re.search('"url":"(.+?)"', html)
            if a:
                r=urllib.unquote(a.group(1))
                if r:
                    stream_url = r
                else:
                    logerror('***** VeeHD - File Not Found')
                    xbmc.executebuiltin("XBMC.Notification(File Not Found,VeeHD,2000)")
                    return False
            if not a:
                a = re.findall('href="(.+?)">', html)
                stream_url = a[1]
        if dialog.iscanceled(): return False
        dialog.update(100)
        return stream_url
    except Exception, e:
        logerror('**** couchtuner VeeHD Error occured: %s' % e)
        raise ResolverError(str(e),"VeeHD")

def resolve_billionuploads(url, filename):
    try:        
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner BillionUploads Link...')  
        dialog.update(0)
        url = re.sub('(?i)^(.*?\.com/.+?)/.*','\\1',url)
        print 'couchtuner BillionUploads - Requesting GET URL: %s' % url
                   
        cookie_file = os.path.join(os.path.join(datapath,'Cookies'), 'billionuploads.cookies')
        
        cj = cookielib.LWPCookieJar()
        if os.path.exists(cookie_file):
            try: cj.load(cookie_file,True)
            except: cj.save(cookie_file,True)
        else: cj.save(cookie_file,True)

        normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        headers = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'),
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', ''),
            ('DNT', '1'),
            ('Connection', 'keep-alive'),
            ('Pragma', 'no-cache'),
            ('Cache-Control', 'no-cache')
        ]
        normal.addheaders = headers
        class NoRedirection(urllib2.HTTPErrorProcessor):
            # Stop Urllib2 from bypassing the 503 page.
            def http_response(self, request, response):
                code, msg, hdrs = response.code, response.msg, response.info()
                return response
            https_response = http_response
        opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = normal.addheaders
        response = opener.open(url).read()
        decoded = re.search('(?i)var z="";var b="([^"]+?)"', response)
        if decoded:
            decoded = decoded.group(1)
            z = []
            for i in range(len(decoded)/2):
                z.append(int(decoded[i*2:i*2+2],16))
            decoded = ''.join(map(unichr, z))
            incapurl = re.search('(?i)"GET","(/_Incapsula_Resource[^"]+?)"', decoded)
            if incapurl:
                incapurl = 'http://billionuploads.com'+incapurl.group(1)
                opener.open(incapurl)
                cj.save(cookie_file,True)
                response = opener.open(url).read()
        captcha = re.search('(?i)<iframe src="(/_Incapsula_Resource[^"]+?)"', response)
        if captcha:
            captcha = 'http://billionuploads.com'+captcha.group(1)
            opener.addheaders.append(('Referer', url))
            response = opener.open(captcha).read()
            formurl = 'http://billionuploads.com'+re.search('(?i)<form action="(/_Incapsula_Resource[^"]+?)"', response).group(1)
            resource = re.search('(?i)src=" (/_Incapsula_Resource[^"]+?)"', response)
            if resource:
                import random
                resourceurl = 'http://billionuploads.com'+resource.group(1) + str(random.random())
                opener.open(resourceurl)
            recaptcha = re.search('(?i)<script type="text/javascript" src="(https://www.google.com/recaptcha/api[^"]+?)"', response)
            if recaptcha:
                response = opener.open(recaptcha.group(1)).read()
                challenge = re.search('''(?i)challenge : '([^']+?)',''', response)
                if challenge:
                    challenge = challenge.group(1)
                    captchaimg = 'https://www.google.com/recaptcha/api/image?c=' + challenge
#                     site = re.search('''(?i)site : '([^']+?)',''', response).group(1)
#                     reloadurl = 'https://www.google.com/recaptcha/api/reload?c=' + challenge + '&' + site + '&reason=[object%20MouseEvent]&type=image&lang=en'
                    img = xbmcgui.ControlImage(550,15,300,57,captchaimg)
                    wdlg = xbmcgui.WindowDialog()
                    wdlg.addControl(img)
                    wdlg.show()
                    
                    kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
                    kb.doModal()
                    capcode = kb.getText()
                    if (kb.isConfirmed()):
                        userInput = kb.getText()
                        if userInput != '': capcode = kb.getText()
                        elif userInput == '':
                            logerror('BillionUploads - Image-Text not entered')
                            xbmc.executebuiltin("XBMC.Notification(Image-Text not entered.,BillionUploads,2000)")              
                            return None
                    else: return None
                    wdlg.close()
                    captchadata = {}
                    captchadata['recaptcha_challenge_field'] = challenge
                    captchadata['recaptcha_response_field'] = capcode
                    opener.addheaders = headers
                    opener.addheaders.append(('Referer', captcha))
                    resultcaptcha = opener.open(formurl,urllib.urlencode(captchadata)).info()
                    opener.addheaders = headers
                    response = opener.open(url).read()
                    
        ga = re.search('(?i)"text/javascript" src="(/ga[^"]+?)"', response)
        if ga:
            jsurl = 'http://billionuploads.com'+ga.group(1)
            p  = "p=%7B%22appName%22%3A%22Netscape%22%2C%22platform%22%3A%22Win32%22%2C%22cookies%22%3A1%2C%22syslang%22%3A%22en-US%22"
            p += "%2C%22userlang%22%3A%22en-US%22%2C%22cpu%22%3A%22WindowsNT6.1%3BWOW64%22%2C%22productSub%22%3A%2220100101%22%7D"
            opener.open(jsurl, p)
            response = opener.open(url).read()
#         pid = re.search('(?i)PID=([^"]+?)"', response)
#         if pid:
#             normal.addheaders += [('Cookie','D_UID='+pid.group(1)+';')]
#             opener.addheaders = normal.addheaders
        if re.search('(?i)url=/distil_r_drop.html', response) and filename:
            url += '/' + filename
            response = normal.open(url).read()
        jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
        if jschl:
            jschl = jschl[0]    
            maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')
            domain_url = re.compile('(https?://.+?/)').findall(url)[0]
            domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
            final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
            html = normal.open(url).read()
        else: html = response
        
        if dialog.iscanceled(): return None
        dialog.update(25)
        
        #Check page for any error msgs            
        if re.search('This server is in maintenance mode', html):
            logerror('***** BillionUploads - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,BillionUploads in maintenance,2000)")                                
            return None
        if re.search('File Not Found', html, re.I):
            logerror('***** BillionUploads - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,BillionUploads,2000)")
            return False

        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.*?)">', html)
        for name, value in r: data[name] = value
        if not data:
            logerror('couchtuner: Resolve BillionUploads - No Data Found')
            xbmc.executebuiltin("XBMC.Notification(No Data Found,BillionUploads,2000)")               
            return None
        
        if dialog.iscanceled(): return None
        
        captchaimg = re.search('<img src="((?:http://|www\.)?BillionUploads.com/captchas/.+?)"', html)            
        if captchaimg:

            img = xbmcgui.ControlImage(550,15,240,100,captchaimg.group(1))
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            
            kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
            kb.doModal()
            capcode = kb.getText()
            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '': capcode = kb.getText()
                elif userInput == '':
                    showpopup('BillionUploads','[B]You must enter the text from the image to access video[/B]',5000, elogo)
                    return None
            else: return None
            wdlg.close()
            
            data.update({'code':capcode})
        
        if dialog.iscanceled(): return None
        dialog.update(50)
        
        data.update({'submit_btn':''})
        enc_input = re.compile('decodeURIComponent\("(.+?)"\)').findall(html)
        if enc_input:
            dec_input = urllib2.unquote(enc_input[0])
            r = re.findall(r'type="hidden" name="(.+?)" value="(.*?)">', dec_input)
            for name, value in r:
                data[name] = value
        extradata = re.compile("append\(\$\(document.createElement\('input'\)\).attr\('type','hidden'\).attr\('name','(.*?)'\).val\((.*?)\)").findall(html)
        if extradata:
            for attr, val in extradata:
                if 'source="self"' in val:
                    val = re.compile('<textarea[^>]*?source="self"[^>]*?>([^<]*?)<').findall(html)[0]
                data[attr] = val.strip("'")
        r = re.findall("""'input\[name="([^"]+?)"\]'\)\.remove\(\)""", html)
        
        for name in r: del data[name]
        
        normal.addheaders.append(('Referer', url))
        html = normal.open(url, urllib.urlencode(data)).read()
        cj.save(cookie_file,True)
        
        if dialog.iscanceled(): return None
        dialog.update(75)
        
        def custom_range(start, end, step):
            while start <= end:
                yield start
                start += step

        def checkwmv(e):
            s = ""
            i=[]
            u=[[65,91],[97,123],[48,58],[43,44],[47,48]]
            for z in range(0, len(u)):
                for n in range(u[z][0],u[z][1]):
                    i.append(chr(n))
            t = {}
            for n in range(0, 64): t[i[n]]=n
            for n in custom_range(0, len(e), 72):
                a=0
                h=e[n:n+72]
                c=0
                for l in range(0, len(h)):            
                    f = t.get(h[l], 'undefined')
                    if f == 'undefined': continue
                    a = (a<<6) + f
                    c = c + 6
                    while c >= 8:
                        c = c - 8
                        s = s + chr( (a >> c) % 256 )
            return s

        dll = re.compile('<input type="hidden" id="dl" value="(.+?)">').findall(html)
        if dll:
            dl = dll[0].split('GvaZu')[1]
            dl = checkwmv(dl);
            dl = checkwmv(dl);
        else:
            alt = re.compile('<source src="([^"]+?)"').findall(html)
            if alt:
                dl = alt[0]
            else:
                logerror('couchtuner: Resolve BillionUploads - No Video File Found')
                xbmc.executebuiltin("XBMC.Notification(No Video File Found,BillionUploads,2000)")
                return None
        
        if dialog.iscanceled(): return None
        dialog.update(100)                    

        return dl
        
    except Exception, e:
        logerror('BillionUploads - Exception occured: %s' % e)
        raise ResolverError(str(e),"BillionUploads")
        return None
    finally:
        dialog.close()


def resolve_180upload(url):

    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner 180Upload Link...')
        dialog.update(0)
        
        puzzle_img = os.path.join(datapath, "180_puzzle.png")
        url=url.replace('180upload.nl','180upload.com')
        print 'couchtuner 180Upload - Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if ">File Not Found" in html:
            logerror('couchtuner: Resolve 180Upload - File Not Found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,180Upload,2000)")
            return False
        if re.search('\.(rar|zip)</b>', html, re.I):
            logerror('couchtuner: Resolve 180Upload - No Video File Found')
            xbmc.executebuiltin("XBMC.Notification(No Video File Found,180Upload,2000)")
            return False
        if dialog.iscanceled(): return False
        dialog.update(50)
                
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            raise Exception('Unable to resolve 180Upload Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net().http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()

           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   xbmc.executebuiltin("XBMC.Notification(You must enter text in the image to access video,2000)")
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving couchtuner 180Upload Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print 'couchtuner 180Upload - Requesting POST URL: %s' % url
        html = net().http_POST(url, data).content
        if dialog.iscanceled(): return False
        dialog.update(100)
        
        link = re.search('id="lnk_download" href="([^"]+)"', html)
        if link:
            print 'couchtuner 180Upload Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            raise Exception('Unable to resolve 180Upload Link')

    except Exception, e:
        logerror('**** couchtuner 180Upload Error occured: %s' % e)
        raise ResolverError(str(e),"180Upload") 
    finally:
        dialog.close()
        
def resolve_vidto(url):
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    from resources.libs import jsunpack
    import time
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner Vidto Link...')
        dialog.update(0)
        html = net(user_agent).http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(11)
        logerror('couchtuner: Resolve Vidto - Requesting GET URL: '+url)
        r = re.findall(r'<font class="err">File was removed</font>',html,re.I)
        if r:
            logerror('couchtuner: Resolve Vidto - File Was Removed')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,Vidto,2000)")
            return False
        if not r:
            r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                           ,html,re.M|re.DOTALL)
            if r:
                unpacked = jsunpack.unpack(r[0])#this is where it will error, not sure if resources,libs added to os path
                try:
                    r = re.findall(r'label:"360p",file:"(.+?)"}',unpacked)[0]
                except:
                    r = re.findall(r'label:"240p",file:"(.+?)"}',unpacked)[0]
            if not r:
                r = re.findall('type="hidden" name="(.+?)" value="(.+?)">',html)
                post_data = {}
                for name, value in r:
                    post_data[name] = value.encode('utf-8')
                post_data['usr_login'] = ''
                post_data['referer'] = url
                for i in range(7):
                    time.sleep(1)
                    if dialog.iscanceled(): return False
                    dialog.update(22+i*11.3)
                html = net(user_agent).http_POST(url,post_data).content
                r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                               ,html,re.M|re.DOTALL)
                if r:
                    unpacked = jsunpack.unpack(r[0])
                    try:
                        r = re.findall(r'label:"360p",file:"(.+?)"}',unpacked)[0]
                    except:
                        r = re.findall(r'label:"240p",file:"(.+?)"}',unpacked)[0]
                if not r:
                    r = re.findall(r"var file_link = '(.+?)';",html)[0]
        if dialog.iscanceled(): return False
        dialog.update(100)
        return r
    except Exception, e:
        logerror('couchtuner: Resolve Vidto Error - '+str(e))
        raise ResolverError(str(e),"Vidto") 
    finally:
        dialog.close()

def resolve_epicshare(url):
    try:
        puzzle_img = os.path.join(datapath, "epicshare_puzzle.png")
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner EpicShare Link...')
        dialog.update(0)
        
        print 'EpicShare - couchtuner Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            logerror('***** EpicShare - Site reported maintenance mode')
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,EpicShare in maintenance,2000)")  
            return False
        if re.search('<b>File Not Found</b>', html):
            logerror('***** EpicShare - File not found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,EpicShare,2000)")
            return False

        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            logerror('***** EpicShare - Cannot find data values')
            raise Exception('Unable to resolve EpicShare Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net().http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()
   
           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving couchtuner EpicShare Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print 'EpicShare - couchtuner Requesting POST URL: %s' % url
        html = net().http_POST(url, data).content
        if dialog.iscanceled(): return False
        dialog.update(100)
        
        link = re.search('<a id="lnk_download"  href=".+?product_download_url=(.+?)">', html)
        if link:
            print 'couchtuner EpicShare Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            logerror('***** EpicShare - Cannot find final link')
            raise Exception('Unable to resolve EpicShare Link')
        
    except Exception, e:
        logerror('**** EpicShare couchtuner Error occured: %s' % e)
        raise ResolverError(str(e),"EpicShare") 
    finally:
        dialog.close()

def resolve_lemupload(url):
    try:
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner LemUpload Link...')       
        dialog.update(0)
#         
        print 'LemUpload - couchtuner Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            print '***** LemUpload - File Not Found'
            xbmc.executebuiltin("XBMC.Notification(File Not Found,LemUpload,2000)")
            return False
        
        if re.search('This server is in maintenance mode', html):
            print '***** LemUpload - Server is in maintenance mode'
            xbmc.executebuiltin("XBMC.Notification(Site In Maintenance,LemUpload,2000)")
            return False

        filename = re.search('<h2>(.+?)</h2>', html).group(1)
        extension = re.search('(\.[^\.]*$)', filename).group(1)
        guid = re.search('http://lemuploads.com/(.+)$', url).group(1)
        vid_embed_url = 'http://lemuploads.com/vidembed-%s%s' % (guid, extension)
        request = urllib2.Request(vid_embed_url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
        request.add_header('Referer', url)
        response = urllib2.urlopen(request)
        if dialog.iscanceled(): return False
        dialog.update(100)
        link = response.geturl()
        if link:
            redirect_url = re.search('(http://.+?)video', link)
            if redirect_url:
                link = redirect_url.group(1) + filename
            print 'couchtuner LemUpload Link Found: %s' % link
            return  link
        else:
            logerror('***** LemUpload - Cannot find final link')
            raise Exception('Unable to resolve LemUpload Link')

    except Exception, e:
        logerror('**** LemUpload Error occured: %s' % e)
        raise ResolverError(str(e),"LemUpload") 
    finally:
        dialog.close()
        
def resolve_mightyupload(url):
    from resources.libs import jsunpack
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MightyUpload Link...')       
        dialog.update(0)
        html = net().http_GET(url).content
        if dialog.iscanceled(): return False
        dialog.update(50)
        logerror('couchtuner: Resolve MightyUpload - Requesting GET URL: '+url)
        r = re.findall(r'name="(.+?)" value="?(.+?)"', html, re.I|re.M)
        if r:
            post_data = {}
            for name, value in r:
                post_data[name] = value
            post_data['referer'] = url
            html = net().http_POST(url, post_data).content
            if dialog.iscanceled(): return False
            dialog.update(100)
            r = re.findall(r'<a href=\"(.+?)(?=\">Download the file</a>)', html)
            return r[0]
        else:
            logerror('***** MightyUpload - File not found')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,MightyUpload,2000,"+elogo+")")
            return False
    except Exception, e:
        logerror('couchtuner: Resolve MightyUpload Error - '+str(e))
        raise ResolverError(str(e),"MightyUpload") 

def resolve_hugefiles(url):
    from resources.libs import jsunpack
    try:
        import time
        puzzle_img = os.path.join(datapath, "hugefiles_puzzle.png")
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving couchtuner HugeFiles Link...')       
        dialog.update(0)
        html = net().http_GET(url).content
        r = re.findall('File Not Found',html)
        if r:
            xbmc.log('couchtuner: Resolve HugeFiles - File Not Found or Removed', xbmc.LOGERROR)
            xbmc.executebuiltin("XBMC.Notification(File Not Found or Removed,HugeFiles,2000)")
            return False
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)"\s* value="?(.+?)">', html)
        for name, value in r:
            data[name] = value
            data.update({'method_free':'Free Download'})
        if data['fname'] and re.search('\.(rar|zip)$', data['fname'], re.I):
            dialog.update(100)
            logerror('couchtuner: Resolve HugeFiles - No Video File Found')
            xbmc.executebuiltin("XBMC.Notification(No Video File Found,HugeFiles,2000)")
            return False
        if dialog.iscanceled(): return False
        dialog.update(33)
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)
        recaptcha = re.search('<script type="text/javascript" src="(http://www.google.com.+?)">', html)
    
        if solvemedia:
            html = net().http_GET(solvemedia.group(1)).content
            hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
            open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('img src="(.+?)"', html).group(1)).content)
            img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            
            xbmc.sleep(3000)
    
            kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            kb.doModal()
            capcode = kb.getText()
       
            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '':
                    solution = kb.getText()
                elif userInput == '':
                    xbmc.executebuiltin("XBMC.Notification(No text entered, You must enter text in the image to access video,2000)")
                    return False
            else:
                return False
                   
            wdlg.close()
            dialog.update(66)
            if solution:
                data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        elif recaptcha:
            html = net().http_GET(recaptcha.group(1)).content
            part = re.search("challenge \: \\'(.+?)\\'", html)
            captchaimg = 'http://www.google.com/recaptcha/api/image?c='+part.group(1)
            img = xbmcgui.ControlImage(450,15,400,130,captchaimg)
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
        
            time.sleep(3)
        
            kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            kb.doModal()
            capcode = kb.getText()
        
            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '':
                    solution = kb.getText()
                elif userInput == '':
                    raise Exception ('You must enter text in the image to access video')
            else:
                raise Exception ('Captcha Error')
            wdlg.close()
            dialog.update(66)
            data.update({'recaptcha_challenge_field':part.group(1),'recaptcha_response_field':solution})

        else:
            captcha = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(html)
            result = sorted(captcha, key=lambda ltr: int(ltr[0]))
            solution = ''.join(str(int(num[1])-48) for num in result)
            dialog.update(66)
            data.update({'code':solution})
        html = net().http_POST(url, data).content
        if dialog.iscanceled(): return False
        if 'reached the download-limit' in html:
            logerror('couchtuner: Resolve HugeFiles - Daily Limit Reached, Cannot Get The File\'s Url')
            xbmc.executebuiltin("XBMC.Notification(Daily Limit Reached,HugeFiles,2000)")
            return False
        r = re.findall("software_download_url : '(.+?)',", html, re.DOTALL + re.IGNORECASE)
        if r:
            dialog.update(100)
            return r[0]
        if not r:
            sPattern = '''<div id="player_code">.*?<script type='text/javascript'>(eval.+?)</script>'''
            jpack = re.findall(sPattern, html, re.DOTALL|re.I)
            if jpack:
                dialog.update(100)
                sUnpacked = jsunpack.unpack(jpack[0])
                sUnpacked = sUnpacked.replace("\\'","")
                r = re.findall('file,(.+?)\)\;s1',sUnpacked)
                if not r:
                  r = re.findall('"src"value="(.+?)"/><embed',sUnpacked)
                return r[0]
            else:
                logerror('***** HugeFiles - Cannot find final link')
                raise Exception('Unable to resolve HugeFiles Link')
    except Exception, e:
        logerror('couchtuner: Resolve HugeFiles Error - '+str(e))
        raise ResolverError(str(e),"HugeFiles")  
