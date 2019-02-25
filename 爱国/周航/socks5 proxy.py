
import logging  #记录
import selectors  #高级复用
import socket  
import sys
import threading #多线程
import time
import traceback
import random

logger = logging.getLogger("Socks5")


class Socks5Error(Exception):
    pass


class AuthenticationError(Socks5Error):#授权错误
    pass


# Empty byte #这块是定义了回复请求的状态
EMPTY = b''
# Response Type
SUCCEEDED = 0  #成功代理
GENERAL_SOCKS_SERVER_FAILURE = 1 #SOCKS服务器出现了错误
CONNECTION_NOT_ALLOWED_BY_RULESET = 2 #不允许的连接
NETWORK_UNREACHABLE = 3 # 找不到网络
HOST_UNREACHABLE = 4 # 找不到主机
CONNECTION_REFUSED = 5 # 连接被拒
TTL_EXPIRED = 6 # TTL超时
COMMAND_NOT_SUPPORTED = 7# 不支持的CMD
ADDRESS_TYPE_NOT_SUPPORTED = 8  #不支持的ATYP  



def judge(ip: str) -> int: #功能注释:有效地描述该函数返回一个类型的对象int
    try:
        socket.inet_aton(ip) #  转换IPV4地址成为32位打包的二进制格式
        return 4
    except OSError:# 内置异常
        pass
    try:
        socket.inet_pton(socket.AF_INET6, ip)#转换IP地址字符串为打包二进制格式
        return 6
    except OSError:
        return 0


class BaseSessoin:
    """
    Client session
    Subclass must set handler
    """

    def __init__(self, sock: socket.socket, address: tuple):#定义init()使创建的每个实例都有自己的属性并方便直接调用类中的函数
        self.socket = sock
        self.address = address #定义为元组使其不能修改
        self.auth = BaseAuthentication(self)

    def recv(self, num: int) -> bytes: #revc的返回对象为bytes
        data = self.socket.recv(num) #开始接收请求
        logger.debug("<<< %s" % data)
        if data == EMPTY:
            raise ConnectionError("Recv a empty bytes that may FIN or RST") #提出连接错误 
        return data #再次接收请求

    def send(self, data: bytes) -> int:#send()返回对象为int
        self.socket.sendall(data) #发送数据
        logger.debug(">>> %s" % data)
        return len(data) #返回数据长度（为什么。。

    def start(self):# 开始这个线程的工作
        try:
            self.negotiate()
        except Socks5Error as e:
            logger.error(e)
            self.socket.close()
        except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError) as e:
            logger.error(e)

    def negotiate(self):#客户端与服务端确定验证方式的一次交互。
        data = self.recv(2)
        VER, NMETHODS = data  #版本，支持的方法数
        if VER != 5:
            self.send(b"\x05\xff")
            raise Socks5Error("Unsupported version!")#版本验证 限制服务器只支持 socks5
        METHODS = set(self.recv(NMETHODS))#删掉接收到的重复数据
        METHOD = self.auth.getMethod(METHODS)#得到所有的 METHODS
        reply = b'\x05' + METHOD.to_bytes(1, 'big')
        self.send(reply)#服务器应该检查是否支持相应的版本和方法，如果支持则返回支持的版本和方法。不支持则发送 255。
        if METHOD == 255:
            raise Socks5Error("No methods available") 
        self.auth.authenticate() #确认是否正确
        del self.auth #将浏览器上 socks 5 代理的账号密码删除，再次访问
        data = self.recv(4)
        VER, CMD, RSV, ATYP = data #CMD: 指定代理方式 ；RSV: 预留位置，标准Socks5应为X'00'；ATYP: 指定DST.ADDR的类型
        if VER != 5:
            self.reply(GENERAL_SOCKS_SERVER_FAILURE)
            raise Socks5Error("Unsupported version!") #限制服务器只支持 socks5

        # Parse target address 
        if ATYP == 1:  # IPV4
            ipv4 = self.recv(4)
            DST_ADDR = socket.inet_ntoa(ipv4)  #从 bytes 转成点号分隔的十进制 ipv4 字符串 DST.ADDR 远程服务器地址
        elif ATYP == 3:  # Domain （ATYP 地址类型基本都是 \x03，即域名。）
            addr_len = int.from_bytes(self.recv(1), byteorder='big')
            DST_ADDR = self.recv(addr_len).decode() #这里应该可以调用一个request库
        elif ATYP == 4:  # IPV6
            ipv6 = self.recv(16)
            DST_ADDR = socket.inet_ntop(socket.AF_INET6, ipv6)#转换32位打包的IPV6地址为IP地址
        else:
            self.reply(ADDRESS_TYPE_NOT_SUPPORTED)
            raise Socks5Error("Unsupported ATYP value: %s" % ATYP)
        DST_PORT = int.from_bytes(self.recv(2), 'big')
        logger.info("Client reuqest %s:%s" % (DST_ADDR, DST_PORT))
        if CMD == 1:
            self.socks5_connect(ATYP, DST_ADDR, DST_PORT) #CONNECT X'01'
        elif CMD == 2:
            self.socks5_bind(ATYP, DST_ADDR, DST_PORT) #BIND X'02'
        elif CMD == 3:
            self.socks5_udp_associate(ATYP, DST_ADDR, DST_PORT) #UDP ASSOCIATE X'03'
        else:
            self.reply(COMMAND_NOT_SUPPORTED)
            raise Socks5Error("Unsupported CMD value: %s" % CMD)
     
      # 服务器响应
    def reply(self, REP: int, ATYP: int = 1, IP: str = "127.0.0.1", port: int = 1080):
        VER, RSV = b'\x05', b'\x00'
        if ATYP == 1:
            BND_ADDR = socket.inet_aton(IP) 
        elif ATYP == 4:
            BND_ADDR = socket.inet_pton(socket.AF_INET6, IP)
        elif ATYP == 3:
            BND_ADDR = len(IP).to_bytes(2, 'big') + IP.encode("UTF-8") 
        else:
            raise Socks5Error("Unsupported ATYP value: %s" % ATYP)

        #建立连接
        REP = REP.to_bytes(1, 'big')
        ATYP = ATYP.to_bytes(1, 'big')
        BND_PORT = int(port).to_bytes(2, 'big')
        reply = VER + REP + RSV + ATYP + BND_ADDR + BND_PORT
        self.send(reply)

    def socks5_connect(self, ATYP: int, address: str, port: int):
        """ must be overwrited """
        self.reply(GENERAL_SOCKS_SERVER_FAILURE)
        self.socket.close()  # CONNECT代理方式

    def socks5_bind(self, ATYP: int, address: str, port: int):
        """ must be overwrited """
        self.reply(GENERAL_SOCKS_SERVER_FAILURE)
        self.socket.close() #BIND代理方式

    def socks5_udp_associate(self, ATYP: int, address: str, port: int):
        """ must be overwrited """
        self.reply(GENERAL_SOCKS_SERVER_FAILURE)
        self.socket.close() #udp代理方式


class BaseAuthentication: #（下面应该是用户验证阶段）

    def __init__(self, session):#初始化
        self.session = session

    def getMethod(self, methods: set) -> int:
        """
        Return a allowed authentication method or 255
        Must be overwrited.
        """
        return 255

    def authenticate(self):
        """
        Authenticate user
        Must be overwrited.
        """
        raise AuthenticationError()


class NoAuthentication(BaseAuthentication):#（未验证的请求）
    """ NO AUTHENTICATION REQUIRED """

    def getMethod(self, methods: set) -> int:
        if 0 in methods:
            return 0
        return 255

    def authenticate(self):
        pass


class PasswordAuthentication(BaseAuthentication):#若服务器选择密码认证
    """ USERNAME/PASSWORD """

    def _getUser(self) -> dict:#（设置用户名和密码并返回为字典）
        return {"Username": "password"} 

    def getMethod(self, methods: set) -> int:
        if 2 in methods:
            return 2
        return 255

    def authenticate(self):
        VER = self.session.recv(1)
        if VER != 5:
            self.session.send(b"\x05\x01")
            raise Socks5Error("Unsupported version!")#again,版本验证
        ULEN = int.from_bytes(self.session.recv(1), 'big')
        UNAME = self.session.recv(ULEN).decode("ASCII")
        PLEN = int.from_bytes(self.session.recv(1), 'big')
        PASSWD = self.session.recv(PLEN).decode("ASCII")
        if self._getUser().get(UNAME) and self._getUser().get(UNAME) == PASSWD:
            self.session.send(b"\x05\x00")
        else:
            self.session.send(b"\x05\x01")
            raise AuthenticationError("USERNAME or PASSWORD ERROR")


class DefaultSession(BaseSessoin):
    """ NO AUTHENTICATION REQUIRED Session"""

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.auth = NoAuthentication(self)
        # TCP Connect
        self.sel = None
        # UDP
        self.alive = None

    def _forward(self, sender: socket.socket, receiver: socket.socket):
        data = sender.recv(4096)
        if data == EMPTY:
            self._disconnect(sender, receiver)
            raise ConnectionAbortedError("The client or destination has interrupted the connection.")
        receiver.sendall(data)
        logger.debug(f">=< {data}")#bug 记录

    def _connect(self, local: socket.socket, remote: socket.socket):
        self.sel.register(local, selectors.EVENT_READ, self._forward)
        self.sel.register(remote, selectors.EVENT_READ, self._forward)
        while True:
            events = self.sel.select(timeout=5)
            for key, mask in events:
                callback = key.data
                if key.fileobj == local:
                    callback(key.fileobj, remote)
                elif key.fileobj == remote:
                    callback(key.fileobj, local)

    def _disconnect(self, local: socket.socket, remote: socket.socket):
        self.sel.unregister(local)
        self.sel.unregister(remote)
        local.close()
        remote.close()

    def socks5_connect(self, ATYP: int, address: str, port: int):
        try:
            remote = socket.create_connection((address, port), timeout=5)
            self.reply(SUCCEEDED)
        except socket.timeout:
            self.reply(CONNECTION_REFUSED)
            logger.warning("Connection refused from %s:%s" % (address, port))
            return
        try:
            self.sel = selectors.DefaultSelector()
            self._connect(self.socket, remote)
        except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            return

    def _heartbeat(self):
        try:
            self.alive = True
            while True:
                self.send(b"heartbeat")
                time.sleep(5)
        except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            self.alive = False    #这里有个等待机制，长时间未响应就关闭

    def parse_udp_header(self, data: bytes) -> ((str, int), bytes):# 解析SOCKS5 UDP 请求
        _data = bytearray(data)

        def recv(num: int) -> bytes:
            if num == -1:
                return bytes(_data)
            r = _data[:num]
            del _data[:num]
            return bytes(r)
        RSV = recv(2)
        FRAG = recv(1)
        if int.from_bytes(FRAG, 'big') != 0:
            return None
        ATYP = int.from_bytes(recv(1), 'big')
        # Parse target address
        if ATYP == 1:  # IPV4
            ipv4 = recv(4)
            DST_ADDR = socket.inet_ntoa(ipv4)
        elif ATYP == 3:  # Domain
            addr_len = int.from_bytes(recv(1), 'big')
            DST_ADDR = recv(addr_len).decode()
        elif ATYP == 4:  # IPV6
            ipv6 = recv(16)
            DST_ADDR = socket.inet_ntop(socket.AF_INET6, ipv6)
        else:
            return None
        DST_PORT = int.from_bytes(recv(2), 'big')
        return ((DST_ADDR, DST_PORT), recv(-1))

    def add_udp_header(self, data: bytes, address: (str, int)) -> bytes: #添加UDP的请求头
        RSV, FRAG = b'\x00\x00', b'\x00'
        t = judge(address[0])
        if t == 4:
            ATYP = 1
            DST_ADDR = socket.inet_aton(address[0])
        elif t == 6:
            ATYP = 4
            DST_ADDR = socket.inet_pton(socket.AF_INET6, address[0])
        else:
            DST_ADDR = int(address[0]).to_bytes(2, 'big') + address[0].encode("UTF-8")
            ATYP = 3
        ATYP = ATYP.to_bytes(1, 'big')
        DST_PORT = address[1].to_bytes(2, 'big')
        reply = RSV + FRAG + ATYP + DST_ADDR + DST_PORT + data
        return reply

    def socks5_udp_associate(self, ATYP: int, address: str, port: int):#UDP转发，为了支持UDP转发，建立一个UDP server
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for _ in range(3):
            try:
                udp_port = random.randint(1024, 65535)
                udp_server.bind(("0.0.0.0", udp_port))
                break
            except OSError:
                continue
        self.reply(SUCCEEDED, IP=self.socket.getsockname()[0], port=udp_port)
        threading.Thread(target=self._heartbeat, daemon=True).start() #UDP的数据处理
        while self.alive:
            try:
                msg, addr = udp_server.recvfrom(8192)
                logger.debug(">>> %s" % msg)
                if address == "0.0.0.0":
                    address = addr   #对来源进行筛选
                if address == addr:
                    try:
                        target, data = self.parse_udp_header(msg)
                    except TypeError:
                        continue
                    udp_server.sendto(data, target)
                else:
                    udp_server.sendto(self.add_udp_header(msg, addr), address)
            except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
                continue


class Socks5:
    """
    A socks5 server
    """

    def __init__(self, ip: str = "0.0.0.0", port: int = 1080, session: BaseSessoin = DefaultSession):
        self.session = session
        self.server = socket.socket(socket.AF_INET)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))
        self.server.listen(13)
        logger.info("Socks5 Server running on %s:%s" % (ip, port))

    def __del__(self):
        self.server.close()
        logger.info("Socks5 Server closed")

    def _link(self, sock: socket.socket, address: (str, int)):
        logger.info("Connection from %s:%s" % address)
        session = self.session(sock, address)
        session.start()
        del session

    def master_worker(self):
        while True:
            try:
                sock, address = self.server.accept()
                client = threading.Thread(
                    target=self._link,
                    args=(sock, address),
                    daemon=True
                )
                client.start()
            except socket.error:
                logger.error("A error in connection from %s:%s" % address)
                traceback.print_exc()

    def run(self):
        worker = threading.Thread(target=self.master_worker, daemon=True)
        worker.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logger.setLevel(logging.DEBUG)
    Socks5().run()