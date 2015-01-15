import urllib,urllib2,re,cookielib,urlresolver,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin, string
import main

#Videobull - by Kasik04a 2014

from t0mm0.common.addon import Addon
from resources.universal import playbackengine, watchhistory
addon_id = 'plugin.video.vdeobull'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.vdeobull', sys.argv)
art = main.art
MainUrl='http://videobull.to/'


def VIDBULLMAIN():
        main.addDir('Latest Tv Shows',MainUrl,860,art+'/latest.png')
        main.addDir('A-Z Tv Shows',MainUrl+'tv-shows/',861,art+'/az.png')
        main.addDir('Search for Tv Shows',MainUrl,866,art+'/search.png')
        main.VIEWSB()

def List(url):
        link=main.OPEN_URL(url)
        match=re.compile('class="cover"><a href="([^"]*?)" rel="bookmark" title=".+?"><img src="([^"]*?)".+?alt="([^"]*?)" /></a>.+?class="postmetadata">([^"]*?)</p>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url,thumb,name,date in match:
            #main.addPlayTE(name+' [COLOR red]'+date+'[/COLOR]',url,5,'','','','','','')
            main.addDirTE(name+'[COLOR red] '+date+'[/COLOR]',url,865,thumb,'','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait

        paginate=re.compile('="nextpostslink" rel="next" href="([^"]*)">&raquo;</a>').findall(link)
        if paginate:
          xurl=paginate[0]         
          main.addDir('[COLOR blue]Next Page'+'[/COLOR]',xurl,860,art+'/next2.png') 
                    

def VBAtoZ():
    main.addDir('1','http://videobull.to/tv-shows/#1',895,art+'/1.png')
    main.addDir('2','http://videobull.to/tv-shows/#2',896,art+'/2.png')
    main.addDir('3','http://videobull.to/tv-shows/#3',897,art+'/3.png')
    main.addDir('4','http://videobull.to/tv-shows/#4',898,art+'/4.png')
    main.addDir('5','http://videobull.to/tv-shows/#5',899,art+'/5.png')
    main.addDir('6','http://videobull.to/tv-shows/#6',900,art+'/6.png')
    main.addDir('7','http://videobull.to/tv-shows/#7',901,art+'/7.png')
    main.addDir('8','http://videobull.to/tv-shows/#8',902,art+'/8.png')
    main.addDir('9','http://videobull.to/tv-shows/#9',903,art+'/9.png')
    
    main.addDir('A','http://videobull.to/tv-shows/#A',869,art+'/a.png')
    main.addDir('B','http://videobull.to/tv-shows/#B',870,art+'/b.png')
    main.addDir('C','http://videobull.to/tv-shows/#C',871,art+'/c.png')
    main.addDir('D','http://videobull.to/tv-shows/#D',872,art+'/d.png')
    main.addDir('E','http://videobull.to/tv-shows/#E',873,art+'/e.png')
    main.addDir('F','http://videobull.to/tv-shows/#F',874,art+'/f.png')
    main.addDir('G','http://videobull.to/tv-shows/#G',875,art+'/g.png')
    main.addDir('H','http://videobull.to/tv-shows/#H',876,art+'/h.png')
    main.addDir('I','http://videobull.to/tv-shows/#I',877,art+'/i.png')
    main.addDir('J','http://videobull.to/tv-shows/#J',878,art+'/j.png')
    main.addDir('K','http://videobull.to/tv-shows/#K',879,art+'/k.png')
    main.addDir('L','http://videobull.to/tv-shows/#L',880,art+'/l.png')
    main.addDir('M','http://videobull.to/tv-shows/#M',881,art+'/m.png')
    main.addDir('N','http://videobull.to/tv-shows/#N',882,art+'/n.png')
    main.addDir('O','http://videobull.to/tv-shows/#O',883,art+'/o.png')
    main.addDir('P','http://videobull.to/tv-shows/#P',884,art+'/p.png')
    main.addDir('Q','http://videobull.to/tv-shows/#Q',885,art+'/q.png')
    main.addDir('R','http://videobull.to/tv-shows/#R',886,art+'/r.png')
    main.addDir('S','http://videobull.to/tv-shows/#S',887,art+'/s.png')
    main.addDir('T','http://videobull.to/tv-shows/#T',888,art+'/t.png')
    main.addDir('U','http://videobull.to/tv-shows/#U',889,art+'/u.png')
    main.addDir('V','http://videobull.to/tv-shows/#V',890,art+'/v.png')
    main.addDir('W','http://videobull.to/tv-shows/#W',891,art+'/w.png')
    main.addDir('X','http://videobull.to/tv-shows/#X',892,art+'/x.png')
    main.addDir('Y','http://videobull.to/tv-shows/#Y',893,art+'/y.png')
    main.addDir('Z','http://videobull.to/tv-shows/#Z',894,art+'/z.png')
    


def A(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    A=re.compile('id="A">(.+?)id="B">').findall(link)
    if A:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(A[0])            
     for url,name in match:
      main.addDir(name,url,864,'') 
def B(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    B=re.compile('id="B">(.+?)id="C">').findall(link)
    if B:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(B[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def C(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    C=re.compile('id="C">(.+?)id="D">').findall(link)
    if C:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(C[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def D(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    A=re.compile('id="D">(.+?)id="E">').findall(link)
    if D:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(D[0])            
     for url,name in match:
      main.addDir(name,url,864,'')      
def E(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    E=re.compile('id="E">(.+?)id="F">').findall(link)
    if E:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(E[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def F(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    F=re.compile('id="F">(.+?)id="G">').findall(link)
    if F:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(F[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def G(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    G=re.compile('id="G">(.+?)id="H">').findall(link)
    if G:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(G[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def H(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    H=re.compile('id="H">(.+?)id="I">').findall(link)
    if H:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(H[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def I(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    I=re.compile('id="I">(.+?)id="J">').findall(link)
    if I:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(I[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def J(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    J=re.compile('id="J">(.+?)id="K">').findall(link)
    if J:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(J[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def K(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    K=re.compile('id="K">(.+?)id="L">').findall(link)
    if K:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(K[0])            
     for url,name in match:
      main.addDir(name,url,864,'')      
def L(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    L=re.compile('id="L">(.+?)id="M">').findall(link)
    if L:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(L[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def M(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    M=re.compile('id="M">(.+?)id="N">').findall(link)
    if M:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(M[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def N(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    N=re.compile('id="N">(.+?)id="O">').findall(link)
    if N:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(N[0])            
     for url,name in match:
      main.addDir(name,url,864,'')      
def O(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    O=re.compile('id="O">(.+?)id="P">').findall(link)
    if O:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(O[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def P(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    P=re.compile('id="P">(.+?)id="Q">').findall(link)
    if P:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(P[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def Q(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    Q=re.compile('id="Q">(.+?)id="R">').findall(link)
    if Q:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(Q[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def R(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    R=re.compile('id="R">(.+?)id="S">').findall(link)
    if R:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(R[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def S(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    S=re.compile('id="S">(.+?)id="T">').findall(link)
    if S:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(S[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def T(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    T=re.compile('id="T">(.+?)id="U">').findall(link)
    if T:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(T[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def U(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    U=re.compile('id="U">(.+?)id="V">').findall(link)
    if U:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(U[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def V(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    V=re.compile('id="V">(.+?)id="W">').findall(link)
    if V:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(V[0])            
     for url,name in match:
      main.addDir(name,url,864,'')      
def W(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    W=re.compile('id="W">(.+?)id="X">').findall(link)
    if W:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(W[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def X(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    X=re.compile('id="X">(.+?)id="Y">').findall(link)
    if X:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(X[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def Y(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    Y=re.compile('id="D">(.+?)id="E">').findall(link)
    if Y:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(Y[0])            
     for url,name in match:
      main.addDir(name,url,864,'')      
def Z(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    Z=re.compile('id="Z">(.+?)</div></div>').findall(link)
    if Z:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(Z[0])            
     for url,name in match:
      main.addDir(name,url,864,'')


def ONE(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    ONE=re.compile('id="1">(.+?)id="2">').findall(link)
    if ONE:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(ONE[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def TWO(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    TWO=re.compile('id="2">(.+?)id="3">').findall(link)
    if TWO:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(TWO[0])            
     for url,name in match:
      main.addDir(name,url,864,'')      
def THREE(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    THREE=re.compile('id="3">(.+?)id="4">').findall(link)
    if THREE:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(THREE[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def FOUR(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    FOUR=re.compile('id="4">(.+?)id="5">').findall(link)
    if FOUR:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(FOUR[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def FIVE(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    FIVE=re.compile('id="5">(.+?)id="6">').findall(link)
    if FIVE:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(FIVE[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def SIX(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    SIX=re.compile('id="6">(.+?)id="7">').findall(link)
    if SIX:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(SIX[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def SEVEN(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    SEVEN=re.compile('id="7">(.+?)id="8">').findall(link)
    if SEVEN:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(SEVEN[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def EIGHT(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    EIGHT=re.compile('id="8">(.+?)id="9">').findall(link)
    if EIGHT:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(EIGHT[0])            
     for url,name in match:
      main.addDir(name,url,864,'')
def NINE(url):
    link = main.OPEN_URL(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','')
    NINE=re.compile('id="9">(.+?)id="A">').findall(link)
    if NINE:
     match=re.compile('<a href=\'([^"]*)\' title=\'.+?\' class=\'.+?\'>([^"]*)<span>').findall(NINE[0])            
     for url,name in match:
      main.addDir(name,url,864,'')      


def List2(url):
        link=main.OPEN_URL(url)
        match=re.compile('class="contentarchivetime">([^"]*)</div><div class="contentarchivetitle"><a href="([^"]*)" title=".+?">([^"]*)</a></div>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for date,url,name in match:
            name=name.replace('&#8211;',' - ').replace('&#039;',"'")    
            #main.addPlayTE(name+' [COLOR red]'+date+'[/COLOR]',url,5,'','','','','','')
            main.addDirTE(name+' [COLOR red]'+date+'[/COLOR]',url,865,'','','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait

        paginate=re.compile('="nextpostslink" rel="next" href="([^"]*)">&raquo;</a>').findall(link)
        if paginate:
          xurl=paginate[0]         
          main.addDir('[COLOR blue]Next Page'+'[/COLOR]',xurl,864,art+'/next2.png') 








            
        
def GRABFEED(name,url):      
        link = main.OPEN_URL(url)
        r = re.compile(r'Videobull &raquo;.+?Comments Feed" href="([^"]*?)" />',re.M|re.DOTALL).findall(link)
        for url in r:
          LINKS(name,url)
                           
             
def LINKS(name,url):      
        html = main.OPEN_URL(url)
        html = html.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('+++','<a href="').replace('---','"></a>')                   
        link = main.OPEN_URL(url)
        link = html.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\\','').replace('+++','<a href="').replace('---','"></a>')                   
        
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
        nowvideo = re.compile(r'<a href="http://www.nowvideo.sx/video/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in nowvideo:        
          url = 'http://www.nowvideo.sx/video/' + url       
          host = 'nowvideo'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        oneeighty = re.compile(r'<a href="http://180upload.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in oneeighty:       
           url = 'http://180upload.com/' + url
           host = '180upload'                   
           main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        vodlocker = re.compile(r'<a href="http://vodlocker.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in vodlocker:        
          url = 'http://vodlocker.com/' + url
          host = 'vodlocker'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        thevideo = re.compile(r'<a href="http://www.thevideo.me/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in thevideo:       
          url = 'http://www.thevideo.me/' + url       
          host = 'thevideo'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        exashare = re.compile(r'<a href="http://www.exashare.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in exashare:       
          url = 'http://www.exashare.com/' + url       
          host = 'exashare'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        allmyvideos = re.compile(r'<a href="http://allmyvideos.net/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in allmyvideos:       
          url = 'http://allmyvideos.net/' + url
          host = 'allmyvideos'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        primeshare = re.compile(r'<a href="http://primeshare.tv/download/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in primeshare:       
          url = 'http://primeshare.tv/download/' + url
          host = 'primeshare'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        oboom = re.compile(r'<a href="https://www.oboom.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in oboom:       
          url = 'https://www.oboom.com/' + url
          host = 'oboom'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        played = re.compile(r'<a href="http://played.to/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in played:       
          url = 'http://played.to/' + url
          host = 'played'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        vidzi = re.compile(r'<a href="http://vidzi.tv/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in vidzi:       
          url = 'http://vidzi.tv/' + url
          host = 'vidzi'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        sharerepo = re.compile(r'<a href="http://sharerepo.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in sharerepo:       
          url = 'http://sharerepo.com/' + url       
          host = 'sharerepo'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        mightyupload = re.compile(r'<a href="http://mightyupload.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in mightyupload:       
          url = 'http://mightyupload.com/' + url
          host = 'mightyupload'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        billionup = re.compile(r'<a href="http://billionuploads.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in billionup:       
          url = 'http://billionuploads.com/' + url
          host = 'billionuploads'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        flashx = re.compile(r'<a href="http://www.flashx.tv/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in flashx:       
          url = 'http://www.flashx.tv/' + url
          host = 'flashx'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        streamin = re.compile(r'<a href="http://streamin.to/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in streamin:       
          url = 'http://streamin.to/' + url
          host = 'streamin'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        moevideo = re.compile(r'<a href="http://moevideo.net/video/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in moevideo:       
          url = 'http://moevideo.net/video/' + url
          host = 'moevideo'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        uptobox = re.compile(r'<a href="http://uptobox.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in uptobox:       
          url = 'http://uptobox.com/' + url
          host = 'uptobox'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        vshare = re.compile(r'<a href="http://vshare.eu/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in vshare:       
          url = 'http://vshare.eu/' + url
          host = 'vshare'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        vidspot = re.compile(r'<a href="http://vidspot.net/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in vidspot:       
          url = 'http://vidspot.net/' + url
          host = 'vidspot'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        yourvideohost = re.compile(r'<a href="http://yourvideohost.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in yourvideohost:       
          url = 'http://yourvideohost.com/' + url
          host = 'yourvideohost'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        uploadable = re.compile(r'<a href="http://www.uploadable.ch/file/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in uploadable:       
          url = 'http://www.uploadable.ch/file/' + url
          host = 'uploadable'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        junkyvideo = re.compile(r'<a href="http://junkyvideo.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in junkyvideo:       
          url = 'http://junkyvideo.com/' + url
          host = 'junkyvideo'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        sharesix = re.compile(r'<a href="http://sharesix.com/f/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in sharesix:       
          url = 'http://sharesix.com/f/' + url
          host = 'sharesix'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        bestreams = re.compile(r'<a href="http://bestreams.net/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in bestreams:       
          url = 'http://bestreams.net/' + url
          host = 'bestreams'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        hugefiles = re.compile(r'<a href="http://hugefiles.net/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in hugefiles:       
          url = 'http://hugefiles.net/' + url
          host = 'hugefiles'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        vidto = re.compile(r'<a href="http://vidto.me/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in vidto:       
          url = 'http://vidto.me/' + url
          host = 'vidto'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        videott = re.compile(r'<a href="http://www.video.tt/video/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in videott:       
          url = 'http://www.video.tt/video/' + url
          host = 'videott'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        vidbull = re.compile(r'<a href="http://vidbull.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in vidbull:       
          url = 'http://vidbull.com/' + url
          host = 'vidbull'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        youwatch = re.compile(r'<a href="http://youwatch.org/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in youwatch:       
          url = 'http://youwatch.org/' + url
          host = 'youwatch'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        vidbux = re.compile(r'<a href="http://www.vidbux.to/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in vidbux:       
          url = 'http://www.vidbux.to/' + url
          host = 'vidbux'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        vidxden = re.compile(r'<a href="http://www.vidxden.to/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in vidxden:       
          url = 'http://www.vidxden.to/' + url
          host = 'vidxden'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        uploadc = re.compile(r'<a href="http://www.uploadc.com/([^"]*)"></a>',re.M|re.DOTALL).findall(html)
        for url in uploadc:       
          url = 'http://www.uploadc.com/' + url
          host = 'uploadc'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        cloudyvideos = re.compile(r'<a href="http://cloudyvideos.com/([^"]*)"></a>',re.M|re.DOTALL).findall(link)
        for url in cloudyvideos:       
          host = 'cloudyvideos'
          url = 'http://cloudyvideos.com/' + url
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')
        movreel = re.compile('<a href="http://movreel.com/([^"]*)"></a>').findall(link)
        for url in movreel:       
          url = 'http://movreel.com/' + url
          host = 'movreel'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')                
        movshare = re.compile('<a href="http://www.movshare.net/video/([^"]*)"></a>').findall(link)
        for url in movshare:       
          url = 'http://www.movshare.net/video/' + url
          host = 'movshare'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')        

        oboom = re.compile('<a href="https://www.oboom.com/([^"]*)"></a>').findall(link)
        for url in oboom:       
          url = 'https://www.oboom.com/' + url
          host = 'oboom'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')        

        nosupload = re.compile('http://nosupload.com/[?]d=([^"]*)').findall(link)
        for url in nosupload:       
          url = 'http://nosupload.com/' + url
          host = 'nosupload'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')        
        filefactory = re.compile('http://www.filefactory.com/([^"]*)').findall(link)
        for url in filefactory:       
          url = 'http://www.filefactory.com/' + url
          host = 'filefactory'                   
          main.addDown2(name.strip()+" [COLOR blue]"+host.upper()+"[/COLOR]",url,868,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')        
                                                                      
        
        
#################################################
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
        stream_url = urlresolver.resolve(url)

        infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok

#################################################          











def PLAYDIS(name,murl):
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
        stream_url = urlresolver(murl)

        infoL={'Title': infoLabels['metaName'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok




def Searchhistory():
    seapath=os.path.join(main.datapath,'Search')
    SeaFile=os.path.join(seapath,'SearchHistoryTV')
    if not os.path.exists(SeaFile):
        SEARCH()
    else:
        main.addDir('Search Shows','###',867,art+'/search.png')
        main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
        for seahis in reversed(searchis):
            url=seahis
            seahis=seahis.replace('%20',' ')
            main.addDir(seahis,url,867,thumb)

            

def SEARCH(url = ''):
        encode = main.updateSearchFile(url,'TV')
        if not encode: return False
        surl='http://videobull.to/?s=' + encode + '&x=0&y=0'
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('class="cover"><a href="([^"]*)" rel="bookmark" title="([^"]*)"><img src="([^"]*)"').findall(link)
        if len(match) > 0:
          for url,name,thumb in match:
           main.addDir(name,url,864,thumb)
        else:   
          match=re.compile('class="contentarchivetime">([^"]*)</div><div class="contentarchivetitle"><a href="([^"]*)" title=".+?">([^"]*)</a></div>').findall(link)
          for date,url,name in match:
           main.addDir(name,url,864,'')
          paginate=re.compile('="nextpostslink" rel="next" href="([^"]*)">&raquo;</a>').findall(link)
          if paginate:
           xurl=paginate[0]         
           main.addDir('[COLOR blue]Next Page'+'[/COLOR]',xurl,867,art+'/next2.png') 
         
          
          






