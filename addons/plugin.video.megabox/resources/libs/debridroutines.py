import urllib, urllib2
import re, os, cookielib
import time as time_

class RealDebrid:

    def __init__(self, cookie_file, username, password):
        self.cookie_file = cookie_file
        self.username = username
        self.password = password
        


    def GetURL(self, url):

        print 'DebridRoutines - Requesting URL: %s' % url
        if self.cookie_file is not None and os.path.exists(self.cookie_file):
            cj = cookielib.LWPCookieJar()
            cj.load(self.cookie_file)
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')   
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
            response = opener.open(req)
            
            #check if we might have been redirected (megapremium Direct Downloads...)
            finalurl = response.geturl()
            
            #if we weren't redirected, return the page source
            if finalurl is url:
                link=response.read()
                response.close()
                return link

            #if we have been redirected, return the redirect url
            elif finalurl is not url:               
                return finalurl    


    def Resolve(self, url):
        print 'DebridRoutines - Resolving url: %s' % url
        timer=int(round(time_.time() * 1000))
        url = 'http://real-debrid.com/ajax/unrestrict.php?link='+url+'&password=&remote=0&time='+str(timer)
        source = self.GetURL(url)
        source=source.replace('\/','/')
        print 'DebridRoutines - Returned Source: %s' % source
        download_details = {}
        download_details['download_link'] = ''
        download_details['message'] = ''
        if re.search('"error":5', source):
            download_details['message'] = 'Upgrade your account to generate a link.'
            return download_details
        if re.search('"error":10',source):
            download_details['message'] = 'No server is available for this hoster.'
            return download_details
        if re.search('"error":11',source):
            download_details['message'] = 'Your file is unavailable on the hoster.'
            return download_details
        if re.search('"error":0',source):
            link =re.compile('generated_links":.+?,.+?,"(.+?)".+?"main_link"').findall(source)[0]
            print 'DebridRoutines - Resolved Link: %s' % link
            download_details['download_link'] = link
            return download_details





    def  checkLogin(self):
        url = 'http://real-debrid.com/lib/api/account.php'
        source = self.GetURL(url)
        if source is not None and re.search('expiration', source):
            return False
        else:
            return True


    def Login(self):    
        if self.checkLogin():
            cj = cookielib.LWPCookieJar()
            login_data = urllib.urlencode({'user' : self.username, 'pass' : self.password})
            url = 'https://real-debrid.com/ajax/login.php?' + login_data
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

            #do the login and get the response
            response = opener.open(req)
            source = response.read()
            response.close()
            cj.save(self.cookie_file)
            print source
            if re.search('OK', source):
                return True
            else:
                return False
        else:
            return True
