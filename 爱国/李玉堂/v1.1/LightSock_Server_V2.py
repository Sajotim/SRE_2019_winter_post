import sys
try:
    import gevent,gevent.monkey
    gevent.monkey.patch_all(dns=gevent.version_info[0]>=1)  #多线程
except ImportError:
    gevent = None
    print(sys.stderr,'警告，没找到gevent，将使用threading代替')

import logging
import struct
import select
import socket
import os
import json
import getopt
from socketserver import TCPServer,ThreadingMixIn,StreamRequestHandler

class ThreadingTCPServer(ThreadingMixIn,TCPServer):
    allow_reuse_address = True

logging.basicConfig(level=(logging.DEBUG))

def handle_tcp(sock,remote): # 数据交换函数
    fdset = [sock,remote]
    try:
        while True:
            r,w,e = select.select(fdset,[],[])
            if sock in r:
                if remote.send(sock.recv(4096)) <= 0:
                    break
            if remote in r:
                if sock.rend(sock.recv(4096)) <= 0:
                    break
    except:
        sock.close()
        remote.close()
        logging.info('数据交换失败！')

class LightSocks(StreamRequestHandler):
    def handle(self):
        logging.info('来自%s:%s的请求' % self.client_address)
        try:
            sock = self.connection
            address_type = ord(sock.recv(1))
            if address_type == 1: #IPV4
                address_ip = self.rfile.read(4) #IPV4刚好4字节
                address = socket.inet_ntoa(address_ip)
            elif address_type == 3: #Domain
                address_ip = ord((sock.recv(1)))
                address = self.rfile.read(address_ip)
            else:
                logging.info('非法的地址类型')
                return
            address_port = self.rfile.read(2)# 地址端口，根据协议，2字节
            port = struct.unpack('!H',address_port)
            reply = b"\x05\x00\x00\x01" #Command支持
            #建立TCP连接
            remote = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            remote.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) #关闭Nagling
            remote.connect((address,port))
            logging.info('TCP连接到',address,port)
            #数据交换
            handle_tcp(sock,remote)
        except socket.error:
            logging.info('Socket错误！')


if __name__ == '__main__':
    print('欢迎使用LightSocks V2')
    os.chdir(os.path.dirname(__file__) or '.')
    with open('config.json', 'rb') as f:
        config = json.load(f)
    SERVER = config['server']
    PORT = config['server_port']
    KEY = config['password']

    optlist, args = getopt.getopt(sys.argv[1:], 'p:k:')
    for key, value in optlist:
        if key == '-p':
            PORT = int(value)
        elif key == '-k':
            KEY = value
    with ThreadingTCPServer(('',PORT),LightSocks) as server:
        server.serve_forever()






