from smbus import SMBus
import socket
import time

bus = SMBus(1)
ADDR = 0x06

HOST = '192.168.4.1'
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def recv():
    return bus.read_byte(ADDR)


while True:
    ac = recv()
    print(ac)
    s.sendto(str(ac).encode(), (HOST, PORT))
    time.sleep(1)
