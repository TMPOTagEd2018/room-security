from smbus import SMBus
import paho.mqtt.client as mqtt
import socket
import time

bus = SMBus(1)
ADDR = 0x06

HOST = '192.168.4.1'
PORT = 1883

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

def recv():
    return bus.read_byte(ADDR)

client = mqtt.Client()
client.connect(HOST, PORT, 60)

while True:
    ac = recv()
    print(ac)
    client.publish("door/gyro", str(ac))
    time.sleep(1)
