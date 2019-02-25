import socket
import  threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 8888))

s.listen(5)
while True:
    cs,address=s.accept()
    print('got connected from'+address)
    cs.send('I have got your socket')
    data = cs.recv(1024)
