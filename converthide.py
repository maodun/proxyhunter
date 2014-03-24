#coding=utf-8


fproxy = open('hide.txt','r')
proxies = fproxy.read().replace(':\n',':').split('\n')
fout = open('hide_output.txt','w')
for proxy in proxies:
    #proxy = proxy.replace(':\n',':')
    if(not proxy):
        continue
    proxy_pair = proxy.lower().split(',')
    res =''
    if('http' in proxy_pair[1]):
        res = res + 'http,' + 'http://'+proxy_pair[0]+'/'+'\n'
    else:
        pass
        #res = res + 'sockets,' + 'sockets://'+proxy_pair[0]+'/'+'\n'
    fout.write(res)
    print proxy
fproxy.close()
fout.close()
