import socket
import _thread

HOST = '192.168.4.1'
PORT = 8000
SERVER = (HOST, PORT)


def connectionHandler(client, addr):
    while True:
        msg = client.recv(1024).decode()
        if not msg:
            break
        print(msg)
        client.send(msg.encode())
    client.close()


s = socket.socket()

print("Starting server...")
print("Waiting for clients")

s.bind(SERVER)
s.listen(1)

while True:
    c, addr = s.accept()
    _thread.start_new_thread(connectionHandler, (c, addr))
s.close()
