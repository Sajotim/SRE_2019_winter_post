import socket
import threading
import re
import time
def get_host(recvData):
     host = re.search(r"Host:\s(.*)\r\n", recvData)
     if host:
         host = host.group(1)
         hosts = host.split(":")
         if len(hosts) == 1:
              return (hosts[0], 80)
         else:
              return (hosts[0], hosts[1])
            
def handler(conn, addr):
    while True:
        try:
            request = conn.recv(1024*1024)

            socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = get_host(request.decode('utf-8'))
            print("目的服务器：", host)
            
            socket_conn.connect(host)
            socket_conn.sendall(request)
            print('客户端请求数据：', request)
            
            data = socket_conn.recv(1024*1024*3)
            socket_conn.close()
            print('接收目的服务器数据字符数:', len(data))
            
            conn.sendall(data)
            
        except Exception as e:
            data = '请求异常：{}, 错误信息：:{}'.format(addr, e)
            conn.sendall(data)

        conn.close()
        break
        time.sleep(1)
        
def run_serve():
    Ip, port = "127.0.0.1", 9999
    #云主机ip，端口
    serve = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serve.bind((Ip, port))
    serve.listen(10)
    print('http代理服务器已启动...')
    while True:
        conn, addr = serve.accept()
        print('客户端请求信息:', conn)
        print("客户端:", addr)
        proxy_thread = threading.Thread(target=handler, args=(conn, addr))
        proxy_thread.start()
        time.sleep(1)

def main():
    try:
        run_serve()
    except Exception as e:
        print('服务器异常：', e)
main()
