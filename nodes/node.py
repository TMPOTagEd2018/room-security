#import keyex
import paho.mqtt.publish as pub
import paho.mqtt.subscribe as sub
from smbus import SMBus
import time

bus = SMBus(1)

HOST = '192.168.4.1'
PORT = 1883

class Sensor:

    def __init__(self, n, p, f):
        self.name = n
        self.place = p
        self.function = f

class Node:
    sensors = []

    def __init__(self, name, addr):
        self.name = name
        self.ADDR = addr

    '''
    def exchange(self):
        dh = keyex.DiffieHellman()

        my_pk = dh.gen_public_key()
        pub.single(f"{self.name}/key", payload=my_pk, qos=1, hostname=HOST, port=PORT)
        they_pk = sub.simple(f"{self.name}/key", hostname=HOST, port=PORT)

        sk = dh.gen_shared_key(they_pk)
        self.seed = int(sk, 16)
    '''

    def register(self, sensor, place, transform):
        self.sensors.append(Sensor(sensor, place, transform))

    def send(self):
        while True:
            d = bus.read_i2c_block_data(self.ADDR, 2)
            for s in self.sensors:
                data = s.function(d[s.place])
                print(s.name, data)
                pub.single(self.name + "/" + s.name, data, qos=1, hostname=HOST, port=PORT)
                time.sleep(.25)
 
