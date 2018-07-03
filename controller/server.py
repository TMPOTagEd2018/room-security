import socket
import _thread
import paho.mqtt.client as mqtt

HOST = '192.168.4.1'
PORT = 8000
SERVER = (HOST, PORT)


def handler(client, addr):
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
s.listen(64)

while True:
    conn, addr = s.accept()
    print(f"New client connected: {addr}")
    _thread.start_new_thread(handler, (conn, addr))
s.close()
