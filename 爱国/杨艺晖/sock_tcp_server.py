import  socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8888))
data=s.recv(1024)
s.send('this is a connection from client')
print('The data received is '+data)
s.close()