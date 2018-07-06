from smbus import SMBus
import paho.mqtt.publish as p_mqtt
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

while True:
    ac = recv()
    print(ac)
    p_mqtt.single("door/gyro", str(ac), qos=1, hostname=HOST, port=PORT)
    time.sleep(1)
