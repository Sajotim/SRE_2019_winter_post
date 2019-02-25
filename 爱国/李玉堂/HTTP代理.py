##两种方法，一是requests，另一种是urllib。详细文档，见https://itanger.cn
"""
import requests
url = 'http://httpbin.org/ip'
s = requests.session()
s.proxies = {'https': 'www.cloudflare.com'}
print(s.get(url).json())
"""
import urllib.request
url = "https://www.name.com/zh-cn/domain/search/0001.gs"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'}
proxy_handler = urllib.request.ProxyHandler({
    'https':'cn.aliyun.com'
})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)
request = urllib.request.Request(url=url,headers=headers)
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
