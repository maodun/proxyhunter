#coding=utf-8

import socket

def encode(pa):
    pa = pa.replace(' ','%20')
    pa = pa.replace('#','%23')
    return pa


def sendsocket(host, port):
    pass
##    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##    s.connect((host, port))
##    s.settimeout(30)
##    #postdata = "id=456&id=789&id=\\'"
##    
##    reqdata = "GET /php/gp.php?i%64=s%6"
##    reqdata += "5lect%%22&ie[1=1&id=\\' HTTP/1.1234"+str(i)+"\r\n"
##    reqdata += "Host:www.baidu.com\r\n"
##    reqdata += "content-type:application/x-www-form-urlencoded\r\n"
##    reqdata += "content-length:%d\r\n" % len(postdata)
##    reqdata += "\r\n"
##    reqdata += postdata
##              
##    print reqdata
##
##    s.sendall(reqdata)
####    import time
####    time.sleep(1)
####    s.sendall(reqdata2)
##    data = s.recv(1024)
##    s.close()
##    print data
##    #print repr(data.split('\r\n')[0])
##    print '-'*20
##    




import urllib2
import random

def randip():
    return str(random.randint(1,255))+str(random.randint(1,255))+str(random.randint(1,255))+str(random.randint(1,255))#'1.2.2.4'

##proxylist = [{'http':'http://180.168.208.15:1981/'},
##             {'http':'http://218.29.74.134:8080/'},
##             {'http':'http://221.2.228.202:9000/'},]
proxylist = []

fproxy = open('hide_output.txt','r')
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
    def __init__(self, url, referer, xip, cookie, proxy, timeout=30):
        proxy_handler = urllib2.ProxyHandler(proxy)
        
        opener = urllib2.build_opener(proxy_handler)
        
        req = urllib2.Request(url)
        req.add_header('Referer', referer)
        req.add_header('X-Forwarded-For', xip)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1838.2 Safari/537.36')
        req.add_header('Cookie', cookie )
        r = opener.open(req, timeout=timeout)
        self.head = r.info()
        self.body = r.read()

    def gethead(self):
        return str(self.head)
    
    def getbody(self):
        return self.body
        

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
            #res = str(proxy) + '#,' + str(m.group(0)) + ','+ str(chinaz[posLeft + posLocLeft + 8:posLeft + posLocLeft + posLocRight].decode('utf-8').encode('gbk'))+ ','
            #res = res + "%.2fs" % (endtime - statime)
            #print res
            #logging.log(1,res+'\n')
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

    
    

