import socket
import requests
import socks


#常用信息修改处
server_ip = "127.0.0.1"
server_port = "9012"
username = "username"
password = "password"

#下面是采用socks对服务器发出验证报文
socks.set_default_proxy(socks.SOCKS5,server_ip,server_port,username='username',password='password')

#验证通过后，后续流量将通过该服务器以及端口传输
socket.socket=socks.socksocket

print(requests.get('https://www.google.com/').text)
#用浏览器抓包可知，google是GET型，content-type是text/html
