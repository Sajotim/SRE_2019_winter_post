# 该版本在之前的简易sock代理基础上，参考0.9版的shadowsocks源代码且剔除加密解密后写的

import logging
import socket
import select
import struct
import json
import os
import sys
import getopt
from socketserver import TCPServer,ThreadingMixIn,StreamRequestHandler

try:
    import gevent, gevent.monkey
    gevent.monkey.patch_all(dns=gevent.version_info[0]>=1)
except ImportError:
    gevent = None

logging.basicConfig(level=(logging.DEBUG))

class ThreadingTCPServer(ThreadingMixIn,TCPServer):
    pass


class LightSocks(StreamRequestHandler):

    def handle(self):
        logging.info('客户端%s:%s发起连接请求' % self.client_address)
        try:
            sock = self.connection
            addr_type = ord(sock.recv(1)) #接收地址类型

            if addr_type == 1:
                address = socket.inet_ntoa(self.rfile.read(4))  #获取dst信息

            elif addr_type == 3:     #域名类型，\x03
                address = self.rfile.read(ord(sock.recv(1)))    #先读取域名的长度（sock.recv（1））里面，然后在读取完整的域名

            else:
                logging.info('地址类型错误')
                return
#获取端口
            port = struct.unpack('!H',self.rfile.read(2))

#连接
            try:
                remote = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                remote.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                remote.connect((address,port))
                logging.info('连接到 %s %s' % (address, port))
            except socket.error as e:
                logging.info('远程服务器连接失败')
                return

#数据交换
            self.data_exchange(sock,remote)

        except socket.error as e:
            logging.info('严重错误')
#发送验证
    def send_all(self, data):
        bytes_sent = 0
        while True:
            r = self.connection.send(data[bytes_sent:])
            if r < 0:
                return r
            bytes_sent += r
            if bytes_sent == len(data):
                return bytes_sent
#数据交换函数
    def data_exchange(self,sock,remote):
        try:
            while True:

                r,w,e = select.select([sock,remote],[],[])
                #当客户端处于可读状态时，发送远程服务器的数据给客户端
                if sock in r:
                    data = sock.recv(4096)
                    if remote.send(data) <= 0:
                        break
                #当远程服务器处于可读时，发送客户端的数据给远程服务器
                if remote in r:
                    data = remote.recv(4096)
                    if sock.send(data) <= 0:
                        break
        finally:
            sock.close()
            remote.close()


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__) or '.')

    print('LightSocks')
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

    with ThreadingTCPServer(('127.0.0.1',9011),LightSocks) as server:
        logging.info("starting server at port %d ..." % PORT)
        server.serve_forever()





