import socket

HOST = '192.168.4.1'
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

message = "Hello world"
s.sendto(message.encode(), (HOST, PORT))
data = s.recv(1024).decode()
s.close()
print('Received', repr(data))
