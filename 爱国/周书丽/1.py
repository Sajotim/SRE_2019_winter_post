import urllib.request
proxy_url=urllib.request.ProxyHandler({'http':'https://tieba.baidu.com/index.html'})
opener=urllib.request.build_opener(proxy_url)
result=opener.open('https://mail.163.com/',timeout=1)
print(result.read().decode('utf-8'))