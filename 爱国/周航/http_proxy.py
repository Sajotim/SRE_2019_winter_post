#coding:utf-8
from socket import *

SerPort = 8888
SerSock = socket(AF_INET, SOCK_STREAM)# 创建监听套接字
SerSock.bind(('', SerPort))
SerSock.listen(5)
print ('Serving at %s'% SerPort) 

while True: 
    CliSock, addr = SerSock.accept()#建立连接，监听接入的连接
    print('Received a connection from: ', addr)
    message = CliSock.recv(4096).decode()#从socket读取信息
    filename = message.split()[1].partition("//")[2].replace('/', '_')
    fileExist = "false"
    
    try:
        f = open(filename, "r") # 检查缓存中是否存在该文件
        outputdata = f.readlines()
        
        fileExist = "true"#存在：
        print('File Exists!')
        CliSock.send("HTTP/1.0 200 OK\r\n".encode())
        CliSock.send("Content-Type:text/html\r\n".encode())
        for i in range(0, len(outputdata)):
            CliSock.send(outputdata[i].encode())#用http响应报文返回对象
        print('Read from cache:')
        
    except IOError:#不存在：
        print('File Exist: ', fileExist)
        if fileExist == "false":
            print('Creating proxyserver socket：')
            c = socket(AF_INET, SOCK_STREAM)#打开一个该对象的初始服务器连接
            hostn = message.split()[1].partition("//")[2].partition("/")[0]
            print('Host Name: ', hostn)
            try:
                c.connect((hostn, 80))
                print('Socket connected to port 80 of the host')
                c.sendall(message.encode())               
                buff = c.recv(4096) 
                CliSock.sendall(buff)#接收到该请求后初始服务器向该proxy发送对应的http报文
               
                tmpFile = open("./" + filename, "w")
                tmpFile.writelines(buff.decode().replace('\r\n', '\n'))#proxy储存副本转发给客户端
                tmpFile.close()

            except:
                print("Illegal request")

        else:            
            print('File Not Found')
    
    tcpCliSock.close()
tcpSerSock.close()
