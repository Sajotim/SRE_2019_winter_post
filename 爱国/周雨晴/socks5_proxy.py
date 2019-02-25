#-*- coding:utf-8 -*-

import socket
import select
import logging
import threading
logging.basicConfig(level = logging.INFO,format = '%(name)s - %(levelname)s - %(message)s')
#logging记录器默认warning以上级别打印出来，所以要设置一下
def send_all(sock, data):
    #辅助函数，发送所有数据到client中
    bytes_sent = 0
    while True:
        r = sock.send(data[bytes_sent:])
        if r < 0:
            return r
        bytes_sent += r
        if bytes_sent == len(data):
            return bytes_sent



def exchange(client, remote):
    #处理client socket和remote socket的数据流
    try:
        fdset = [client, remote]
        while True:
            #用IO多路复用select监听套接字是否有数据流
            r, w, e = select.select(fdset, [], [])
            if client in r:
                #client可读则读出来pipe到remote中
                data=client.recv(4096)
                print(data)
                if len(data) <= 0:
                    break
                result = send_all(remote, data)
                if result < len(data):
                    raise Exception('failed to send all data')
            if remote in r:
                #remote可读则读出来pipe到client中
                data=remote.recv(4096)
                if len(data) <= 0:
                    break
                result = send_all(client, data)
                if result < len(data):
                    raise Exception('failed to send all data')
    except Exception as e:
        raise(e)
    finally:
        client.close()
        remote.close()
    print("piping data done.")

def client_connect(client, addr):
    #接受客户端的请求，sock5的认证和连接过程
    client.recv(257)
    #响应客户端，x00表示不需要验证
    client.send(b"\x05\x00")  #\xhh,值为16进制数hh的字符
    ver=client.recv(1)
    cmd=client.recv(1)
    rsv=client.recv(1)
    atype=client.recv(1)

    #判断是否支持cmd，目前只支持0x01（connect）
    if int.from_bytes(cmd,byteorder="big") != 1:     #返回对应的十进制整数，因为收到的数据是bytes类型不能拿来直接用
        return                                       #并且使用大端排序，在通讯协议中，一般使用大端排序

    #判断是否支持atype，目前不支持IPv6
    if int.from_bytes(atype,byteorder="big") == 1:
        #IPv4
        remote_addr=socket.inet_ntoa(client.recv(4)) #转换32位打包的二进制地址为IPv4地址的标准点号分隔字符串表示
        remote_port =int.from_bytes(client.recv(2),byteorder="big")
    elif int.from_bytes(atype,byteorder="big") == 3:
       #域名
        addr_len=int.from_bytes(client.recv(1),byteorder="big")
        remote_addr=client.recv(addr_len)
        remote_port=int.from_bytes(client.recv(2),byteorder="big")
    else:
        #不支持的地址类型
        reply=b"\x05\x08\x00\x01\x00\x00\x00\x00"+(1080).to_bytes(2,byteorder="big")
        client.send(reply)
        client.close()
        return

    #回复客户端连接建立
    reply=b"\x05\x00\x00\x01\x00\x00\x00\x00"+(1080).to_bytes(2,byteorder="big")
    client.send(reply)
    #拿到remote address 的信息后，建立连接
    try:
        remote=socket.create_connection((remote_addr,remote_port))
        #这个函数比socket.connect()更高级，如果addr（host, port）中的host是一个非数值的值，那么该函数会
        #同时尝试AF_INET和AF_INET6来解析它，然后尝试所有获得的可能地址，该方法可以用来编写同时支持IPv4和IPv6的客户端
        logging.info('connecting %s:%d' % (remote_addr,remote_port)) #证明事情按预期进行
    except socket.error as e:   #socket.error是IOError的一个子类
        logging.error(e)  #由于一些问题，软件已不能执行一些功能了。
        return
    #转接双方数据
    exchange(client,remote)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 1080))
    server.listen(5)
    print("server listening on port:1080")

    try:
        while True:
            sock, addr = server.accept()
            t = threading.Thread(target=client_connect, args=(sock,addr)) #创建线程
            t.start() #启动线程
    except socket.error as e:
        logging.error(e)
    except KeyboardInterrupt:
        server.close()

if __name__ == '__main__':
    main()