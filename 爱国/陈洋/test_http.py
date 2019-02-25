import socket
import urllib

#创建一个服务端
serverport = 8888
serverip = '192.168.1.3'
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('',serverport))
serversocket.listen(5)
while 1:
    connectsocket, addr = serversocket.accept()
    connectdate = connectsocket.recv(1024).decode()
    # 设置HTTP代理
    proxy_handler = urllib.request.ProxyHandler({'http': 'http://serverip:serverport/'})
    opener = urllib.request.build_opener(proxy_handler)
    r = opener.open('http://httpbin.org/ip')
    print(r.read())
    #发送HTTP请求
    send_date = "GET {r} {HTTP/1.0}\r\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(r,80)
    sock.sendall(send_data.encode())
    serverdate = connectsocket.recv(1024).decode()
    serversocket.sendall(serverdate.encode())
    connectsocket.close()
    s.close()

if __name__ == '__main__':
    main()
