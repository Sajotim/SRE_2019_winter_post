import urllib.request

url='http://www.httpbin.org/ip'

headers=[]

proxy_handler = urllib.request.ProxyHandler({'http': 'http://localhost:8080/'})
opener = urllib.request.build_opener(proxy_handler)
r = opener.open('http://httpbin.org/ip')
print(r.read())