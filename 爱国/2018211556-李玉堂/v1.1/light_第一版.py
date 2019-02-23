from socketserver import TCPServer,ThreadingMixIn,StreamRequestHandler
import struct
import socket
import select
import logging

SOCK_VERSION = 5
logging.basicConfig(level=logging.DEBUG)

#创建TCPserver线程并监听端口

class ThreadingTCPServer(ThreadingMixIn,TCPServer):
    pass


class LightSocksProxy(StreamRequestHandler):
    #认证信息（可任意修改‘’里面的内容）
    username = 'username'
    password = 'password'

    def handle(self):
        logging.info('收到来自%s：%s的连接请求' % self.client_address)

        #创建header
        #解包并读取来自客户端2byets的数据（其中1byet是认证version，另1byet是nmethod）

        header = self.connection.recv(2)
        version,nmethods = struct.unpack("!BB",header)

        #设定Socks的版本为5，以及协商信息的nmethod必须大于零（因为我们采用的是第二种验证方式），需要对客户端发来的信息判断是否为nmethod确定的那样
        assert version == SOCK_VERSION
        assert nmethods > 0

        #得到客户端发来的有效认证方式
        methods = self.get_right_methods(nmethods)

        #只接受用户名/密码的认证方式（在此需要对客户端发来的认证方式进行判断）
        if 2 not in set(methods):
            #断开连接
            self.server.close_request(self.request)
            return
        #如果认证方式正确，则回复客户端
        self.connection.sendall(struct.pack("!BB",SOCK_VERSION,2))

        #进行用户名和密码认证
        if not self.verify_right():
            return

        #获取客户端发送的version，cmd，rsv，atyp，dst.addr，dst.port等信息
        version, cmd, _, add_type = struct.unpack("!BBBB",self.connection.recv(4))
        assert version == SOCK_VERSION

        #add_type总共有三种类型
        if add_type == 1: #ipv4
            address = socket.inet_ntoa(self.connection.recv(4))
        elif add_type == 3: #domain
            domain_len = ord(self.connection.recv(1)[0])
            address = self.connection.recv(domain_len)
        elif add_type == 4: #ipv6
            address = socket.inet_aton(self.connection.recv(16))

        port = struct.unpack('!H',self.connection.recv(2))[0]

        #服务器端对客户端发来了ip/域名，去尝试做连接，如果连接成功，则对客户端答复version,rep,rsv,atyp,bnd.addr,bnd.port信息
        try:
            if cmd == 1: #cmd ==1 是connect态，其中还有Bind 2 ，UDP 3
                re_connect = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #re_connect == remote_connect
                re_connect.connect((address,port))
                bind_address = re_connect.getsockname()
                logging.info('连接到 %s %s' % (address, port))
            else:
                self.server.close_request(self.request)
            addr = struct.unpack("!I",socket.inet_aton(bind_address[0]))[0]
            port = bind_address[1]
            reply_strs = struct.pack("!BBBBIH",SOCK_VERSION,0,0,add_type,
                                     addr,port)

        except Exception as error:
            reply_strs = self.re_connect_refused(add_type,5)

        self.connection.sendall(reply_strs)

        #如果远程服务器连接成功并且连接为connect，则与客户端进行数据交换
        if reply_strs[1] == 0 and cmd ==1:
            self.data_exchange(self.connection,re_connect)

        self.server.close_request(self.request)



#该函数读取从客户端收到的nmethods的数据并用ord()函数处理成对应的ASCII码，并添加给methods
    def get_right_methods(self,n):
        methods = []
        for i in range(n):
            methods.append(ord(self.connection.recv(1)))
        return methods


#用户名密码认证函数
    def verify_right(self):
        version = ord(self.connection.recv(1))
        assert version == 1

        username_len = ord(self.connection.recv(1)) #获取用户名长度
        username = self.connection.recv(username_len).decode('utf-8') #将收到的字符串解码

        password_len = ord(self.connection.recv(1))
        password = self.connection.recv(password_len).decode('utf-8')

        if username == self.username and password == self.password:
            #如果认证成功，就返回状态码0，status = 0
            response = struct.pack("!BB",version,0)
            self.connection.sendall(response)
            return True

        #如果认证失败，就返回状态码0xFF，status ！=0
        response = struct.pack("！BB",version,0xFF)
        self.connection.sendall(response)
        self.server.close_request(self.request)
        return False


#如果远程服务器拒绝连接
    def re_connect_refused(self, add_type, error_number):
        return struct.pack("!BBBBIH", SOCK_VERSION, error_number, 0, add_type, 0, 0)



#数据交换函数
    def data_exchange(self,client,re_connect):
        while True:

            r,w,e = select.select([client,re_connect],[],[])
            #当客户端处于可读状态时，发送远程服务器的数据给客户端
            if client in r:
                data = client.recv(4096)
                if re_connect.send(data) <= 0:
                    break
            #当远程服务器处于可读时，发送客户端的数据给远程服务器
            if re_connect in r:
                data = re_connect.recv(4096)
                if client.send(data) <= 0:
                    break



if __name__ == '__main__':
    with ThreadingTCPServer(('127.0.0.1',9012),LightSocksProxy) as server:
        server.serve_forever()
