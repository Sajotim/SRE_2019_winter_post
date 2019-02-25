#-*- coding:utf-8 -*-
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

class Proxy(BaseHTTPRequestHandler):

    def recv(self, sock):
        data=b''
        #因为使用非长连接，所以会关闭连接，recv会退出
        while True:
            recv_data = sock.recv(4096)
            if not recv_data:
                break
            data += recv_data
        sock.close()
        return data

    def do_GET(self):
        #解析GET请求
        uri = urlparse(self.path)     #解析url，urlparse会将url解析为六个部分
        scheme, host, path = uri.scheme, uri.hostname, uri.path
        host_ip = socket.gethostbyname(host)  #返回主机名的IPv4地址
        port = 80

        #为了简单起见，Connection都为close，也就不需要Proxy_Connection的判断了
        del self.headers['Proxy-Connection']
        self.headers['Connection'] = 'close'
        #构造新的http请求
        send_data = "GET {path} {protocol_version}\r\n".format(path=path, protocol_version=self.protocol_version)
        headers= ''
        for key, value in self.headers.items():
            headers += "{key}:{value}\r\n".format(key=key, value=value)
        headers += '\r\n'
        send_data += headers
        print(send_data)


        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((host_ip, port))
        sock.sendall(send_data.encode())
        data=self.recv(sock)
        self.wfile.write(data) #将响应写回客户端的输出流

def main():
    try:
        server = HTTPServer(('', 8888), Proxy)
        server.serve_forever()#处理请求直到明确shutdown()请求
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()





