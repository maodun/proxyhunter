#coding=utf-8

import socket

def encode(pa):
    pa = pa.replace(' ','%20')
    pa = pa.replace('#','%23')
    return pa


def sendsocket(host, port):
    pass

import logging
logging.basicConfig(filename = 'proxy.log',\
                    level = logging.INFO,\
                    filemode = 'w',\
                    format = '%(message)s')


import httplib
import random

def randip():
    return str(random.randint(1,255))+str(random.randint(1,255))+str(random.randint(1,255))+str(random.randint(1,255))#'1.2.2.4'

##proxylist = [{'http':'http://180.168.208.15:1981/'},
##             {'http':'http://218.29.74.134:8080/'},
##             {'http':'http://221.2.228.202:9000/'},]
proxylist = []

fproxy = open('plinput.txt','r')
fplist = fproxy.readlines()
fplist = list(set(fplist)) #remove dup
for proxy in fplist:
    #global proxylist
    if(not proxy):
        continue
    proxy_pair = proxy.strip().lower().split(',')
    if 'http' in proxy_pair[0]:
        proxylist.append({proxy_pair[0]:proxy_pair[1]})
fproxy.close()


#print proxylist
def getproxylist():
    return

proxyindex = 0
proxylen = len(proxylist)

class SendReq:
    head = ''
    body = ''
    def __init__(self, url, referer, xip, cookie, proxyitem, timeout=30):
        proxy = proxyitem['http'][7:-1]
        hc = httplib.HTTPConnection(proxy, timeout=timeout)
        
        headers = {}
        if(referer):
            headers['Referer'] = referer
        else:
            headers['Referer'] = url
        headers['X-Forwarded-For'] = xip
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1838.2 Safari/537.36'
        if(cookie):
            headers['Cookie'] = cookie
        self.head = {}
        self.body = ''
        self.code = None
        self.url = url
        
        hc.request('GET',url, headers = headers)
        resp = hc.getresponse()
        
        self.setheads(resp.getheaders())
        self.body = resp.read()
        hc.close()
        

        
##        proxy_handler = urllib2.ProxyHandler(proxy)
##        
##        opener = urllib2.build_opener(proxy_handler)
##        
##        req = urllib2.Request(url)
##        req.add_header('Referer', referer)
##        req.add_header('X-Forwarded-For', xip)
##        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1838.2 Safari/537.36')
##        req.add_header('Cookie', cookie )
##        r = opener.open(req, timeout=timeout)
##        self.head = r.info()
##        self.body = r.read()
    def setheads(self, headlist):        
        for headline in headlist:
            self.head[headline[0].strip().lower()] = headline[1].strip()
            
    def gethead(self):
        return str(self.head)
    
    def getbody(self):
        return str(self.body)
        

import re, time
import threading
lock = threading.RLock()

#fresult = open('result.txt','a')

#import logging, datetime
#import logging.handlers
#logger = logging.getLogger()
#logger.setLevel(logging.INFO)

def chinaz_ip(proxy):
    try:
        statime = time.time()
        chinaz = SendReq('http://ip.chinaz.com/', 'http://ip.chinaz.com/', randip(), '', proxy, timeout = 100).getbody()
        endtime = time.time()
        #chinaz = urllib2.urlopen("http://ip.chinaz.com/").read()
        m = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",chinaz)
        if m:
            posLeft = chinaz.index(m.group(0))
    ##        print posLeft
            posLocLeft = chinaz[posLeft:].index("<strong>")
    ##        print posLocLeft
            posLocRight = chinaz[posLeft + posLocLeft:].index("</strong>")
    ##        print posLocRight
            lock.acquire()
            print proxy, '#,', m.group(0),  ',', chinaz[posLeft + posLocLeft + 8:posLeft + posLocLeft + posLocRight].decode('utf-8').encode('gbk'), ',', "%.2fs" % (endtime - statime)
            res = str(proxy) + '#,' + str(m.group(0)) + ','+ str(chinaz[posLeft + posLocLeft + 8:posLeft + posLocLeft + posLocRight].decode('utf-8').encode('gbk')).replace('\n','')+ ','
            res = res + "%.2fs" % (endtime - statime)
            #print res
            logging.info(res)
            #print pro
            #fresult.write(pro+'\n')
            lock.release()
    except:
        pass

def main():
    import WorkManager
    wm = WorkManager.WorkerManager(30)
    for proxy in proxylist:
        wm.add_job(chinaz_ip, proxy)
    
    wm.wait_for_complete()

if __name__=='__main__':
    main()

    
    

