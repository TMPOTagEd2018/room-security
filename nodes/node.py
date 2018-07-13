import keyex
import paho.mqtt.client as paho
from smbus import SMBus
import time

class Sensor:

    def __init__(self, n, p, f):
        self.name = n
        self.place = p
        self.function = f

class Input:

    def __init__(self, n, t, f):
        self.name = n
        self.topic = t
        self.function = f

class Node:
    inputs = []
    sensors = []

    def __init__(self, name, addr):
        self.name = name
        self.ADDR = addr
        self.bus = SMBus(1)
        self.c = paho.Client("name")
        self.c.tls_set("ca.crt")
        self.c.connect("192.168.4.1", 8883)

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

    def pipe(self, name, topic, pipeline):
        self.inputs.append(Input(name, topic, pipeline))

    def start(self):
        while True:
            d = self.bus.read_i2c_block_data(self.ADDR, 48)
            for i in self.inputs:
                r = self.c.subscribe(i.name + "/" + i.topic, qos=1)
                i.function(r)
                print("Recieved: ", bytes(r.payload))
            for s in self.sensors:
                data = s.function(d[s.place])
                print((self.name + "/" + s.name), data)
                self.c.publish(self.name + "/" + s.name, data, qos=1)
            time.sleep(.25)
 
