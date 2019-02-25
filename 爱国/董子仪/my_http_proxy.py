from socket import *
import threading




def Proxy_start(serSocket):

    connSocket, addr = serSocket.accept()
    print("[{},{}]用户连接上了".format(addr[0], addr[1]))
    datas = connSocket.recv(1024)     #接收客户端发来的数据
    data = datas.decode()
    print("这是发过来的数据:\n" + data)
    if not data:                                #发过来的数据为空，就重新发送上一次数据
        print('无')
        data = last_data[-1]
        if not data:
            exit("错误请求")
    last_data.append(data)
    print('******************************')
    requestline = data.split('\r\n',1)[0]             #将数据解码后分割为第一行和其余行
    remainline = data.split('\r\n',1)[1]
    method , url , protocol = requestline.split()
    if '://' in url:                                                      #排除掉http://这种情况
         clean_url = url.split(':')[1]
    else:
        clean_url = url
    print('已分割出url')
    #print("这个是url：\n" + clean_url)              #再次将第一行的内容分割
    hosts = remainline.split('Host: ')[1]           #由于Host不一定会在首部字段的第一行所以将host分出来
    host = hosts.split('\r\n',1)[0]                 #分出host
    #print("这个是hosts：\n" + hosts)

    #print("这个是host:\n" + host)
    print('已分割出host')
    send_data = data
    #print("这个是send_data:\n" + send_data)
    print('生成转发数据')
    try:
        r_host = gethostbyname(host)                                 #将主机名解释为一个IP地址，失败后将引发一个异常
        if ':' in clean_url:                                        #有些网站的端口是包含在相对路径里的（比如内网外入）所以要提取出来
             port = clean_url.split(':')[1]
        else:
            port = '80'
    except:
        if ':' in host:                                             #如果有‘：’则给端口赋值否则默认端口为80
            r_host,port = host.split(':')
            if r_host.isalpha():
                r_host = gethostbyname(r_host)
        elif ':' in clean_url:
            port = url.split(':')[1]
        else:
            port = '80'
    #print("这个是port：\n" + port)
    #print("这个是r_host:\n" + r_host)
    print("获取目标主机名成功")
    send_socket = socket()                                            #创建一个新的套接字来向服务器转发数据
    send_socket.connect((r_host,int(port)))

    send_socket.send(send_data.encode())
    d = send_socket.recv(1024)
    #print("这个是服务器发来的数据：\n" + d.decode())
                                                                        #接收服务器发来的数据
    connSocket.send(d)                                                  #将它转发给客户端
    print("转发成功")
    print("#####################################################")
    send_socket.close




if __name__ == '__main__':
    last_data = ['']
    serPort = 2333         #瞎jb整的端口
    serSocket = socket(AF_INET,SOCK_STREAM)
    serSocket.bind(('',serPort))
    serSocket.listen(100)

    while True:
        t1 = threading.Thread(target=Proxy_start(serSocket))
        # 开始多线程
        t1.start()
