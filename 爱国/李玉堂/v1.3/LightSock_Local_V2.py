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
import json
import os
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
        try:
            sock = self.connection
            # 1.版本协商
            sock.sendall(struct.pack("!BB",5,1))
            # 2.请求
            version, cmd, _, address_type = struct.unpack("!BBBB", sock.recv(4)) #读取服务端的响应包，内含SOCK命令码，地址类型，地址，端口
            if cmd != 1:
                logging.info('Command not supported!')
                return
            if address_type == 1: #IPV4
                address_ip = sock.recv(4) #IPV4刚好4字节
                address = socket.inet_ntoa(address_ip)
            elif address_type == 3: #Domain
                domain_len = ord((sock.recv(1)[0]))
                address = sock.recv(domain_len)
            else:
                logging.info('非法的地址类型')
                return
            address_port = sock.recv(2)# 地址端口，根据协议，2字节
            port = struct.unpack('!H',address_port)[0]
            reply = b"\x05\x00\x00\x01" #Command支持
            reply += socket.inet_aton('0.0.0.0') + struct.pack('!H',2222)
            self.wfile.write(reply)

            #建立TCP连接
            remote = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            remote.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) #关闭Nagling
            remote.connect((SERVER,REMOTE_PORT))
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
        server.serve_forever()
