import logging
import socket
import struct
import select
from socketserver import TCPServer,ThreadingMixIn,StreamRequestHandler

def send_data(sock,data):
    bytes_sent = 0
    while True:
        r = sock.send(data[bytes_sent:])
        if r < 0:
            return r
        bytes_sent += r
        if bytes_sent == len(data):
            return bytes_sent
def handle_tcp(sock,remote):
    #处理客户端socket和远程端socket的数据流
    try:
        fdset = [sock,remote]
        while True: #利用select i/o多路复用来监听套接字
            r,w,e = select.select(fdset,[],[])
            if sock in r:
                data = sock.recv(4096)
                if len(data) <= 0:
                    break
                result = send_data(remote,data)

            if remote in r:
                data = remote.recv(4096)
                if len(data) <= 0:
                    break
                result = send_data(sock,data)
    except:
        logging.info('TCP Error!')
    finally:
        sock.close()
        remote.close()

class ThreadingTCPServer(ThreadingMixIn,TCPServer):
    pass

class LightSocks(StreamRequestHandler):
    def handle(self):
        logging.info('来自%s:%s的请求' % self.client_address)
        sock = self.connection
        # 接受客户端来的请求，socks5 的 认证和连接过程
        sock.recv(256)
        #无需进一步认证
        sock.send(b"\x05\x00")
        data = sock.recv(4)
        #CMD 为0x01 即为CONNect
        mode = data[1]
        if mode != 1:
            logging.info('CMD ERROR！')
            return
        # DST.ADDR 有三种形式，排除ipv6，国内用得少
        address_type = data[3]
        if address_type == 1: #ipv4
            address_ip = sock.recv(4)
            re_address = socket.inet_ntoa(address_ip)
        elif address_type == 3:
            domain_len = ord(sock.recv(1))
            re_address = sock.recv(domain_len)
        else:
            logging.info('ADDRESS TYPE ERROR!')
            return
        # DST.PORT

        port = struct.unpack('>H',sock.recv(2))

        # 返回客户端 success
        reply = b"\x05\x00\x00\x01"
        reply += socket.inet_aton('0.0.0.0') + struct.pack('>H',2222)
        sock.send(reply)

        #开始和re_address 建立连接
        try:
            remote = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            remote.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) #关闭Nagling
            remote.connect((re_address,port[0]))
            logging.info('TCP连接到',re_address,port[0])
        except socket.error as e:
            logging.error(e)
            return
        #TCP处理
        handle_tcp(sock,remote)

if __name__ == '__main__':
    print('欢迎使用LightSocks')

    LOCAL = ''
    PORT = 9011

    with ThreadingTCPServer(('',PORT),LightSocks) as server:
        server.serve_forever()



