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
        logging.info('向%s:%s发起连接请求' % self.client_address)
        try:
            sock = self.connection
            sock.recv(262)
            sock.send("\x05\x00".encode())   #发送SOCK_VERSION = 5(\x05),认证方式为\x00
            testdata = self.rfile.read(1024)
            print("---------")
            print(testdata)
            print("---------")
			
            data = self.rfile.read(4) #读取响应数据VER CMD RSV ATYP (4 bytes)
            
            
            mode = ord(data[1])
            if mode != 1:
                logging.info('连接Sock服务器失败')
                logging.warn('CMD != 1')
                return
#地址类型（ipv4/domain）
            addr_type = ord(data[3])
            address_send = data[3]
            if addr_type == 1:
                addr_ip = self.rfile.read(4) #ipv4共4字节
                address = socket.inet_ntoa(addr_ip)
                address_send =address_send + addr_ip

            elif addr_type == 3:     #域名类型，\x03
                addr_len = self.rfile.read(1)
                address = self.rfile.read(ord(addr_len))
                address_send += addr_len + address

            else:
                logging.info('地址类型错误')
                return
#获取端口
            addr_port = self.rfile.read(2)
            address_send += addr_port
            port = struct.unpack('!H',addr_port)

#回复客户端
            try:
                reply = '\x05\x00\x00\x01' #VER REP RSV ATYP
                reply = reply + socket.inet_aton('0.0.0.0') + struct.pack("!H",1030) #监听本地上PORT端口的所有地址
                self.wfile.write(reply)
#连接远程服务器
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

    def send_all(self, data):
        bytes_sent = 0
        while True:
            r = self.connection.send(data[bytes_sent:])
            if r < 0:
                return r
            bytes_sent += r
            if bytes_sent == len(data):
                return bytes_sent
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
    with open('config.json', 'rb') as f:
        config = json.load(f)
    SERVER = config['server']
    REMOTE_PORT = config['server_port']
    PORT = config['local_port']
    KEY = config['password']

    optlist, args = getopt.getopt(sys.argv[1:], 's:p:k:l:')
    for key, value in optlist:
        if key == '-p':
            REMOTE_PORT = int(value)
        elif key == '-k':
            KEY = value
        elif key == '-l':
            PORT = int(value)
        elif key == '-s':
            SERVER = value

    with ThreadingTCPServer(('',PORT),LightSocks) as server:
        logging.info("starting server at port %d ..." % PORT)
        server.serve_forever()





