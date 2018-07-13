import keyex
import random

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
        self.addr = addr
        self.bus = SMBus(1)
        self.c = paho.Client("name")
        self.c.tls_set("ca.crt")
        self.c.connect("192.168.4.1", 8883)

    def exchange(self):
        dh = keyex.DiffieHellman()

        my_pk = dh.gen_public_key()
        they_pk = None

        def handler(client, data, flags, rc):
            global they_pk
            they_pk = data.decode()

        self.c.subscribe(f"{self.name}/key")
        self.c.on_message = handler
        self.c.publish(f"{self.name}/key", payload=my_pk, qos=1)

        while they_pk is None:
            time.sleep(0.25)

        self.c.on_message = None

        sk = dh.gen_shared_key(they_pk)
        random.seed(int(sk, 16))
        self.rng = random.getstate()

    def register(self, sensor, place, transform):
        self.sensors.append(Sensor(sensor, place, transform))

    def pipe(self, name, topic, pipeline):
        self.inputs.append(Input(name, topic, pipeline))

    def start(self):
        counter = 0

        self.exchange()

        while True:
            d = self.bus.read_i2c_block_data(self.addr, 48)
            for i in self.inputs:
                r = self.c.subscribe(i.name + "/" + i.topic, qos=1)
                i.function(r)
                print("Recieved: ", bytes(r.payload))
            for s in self.sensors:
                data = s.function(d[s.place])
                print((self.name + "/" + s.name), data)
                self.c.publish(self.name + "/" + s.name, data, qos=1)
            self.c.loop()
            time.sleep(.25)

            counter = counter + 1
            if counter == 20:
                random.setstate(self.rng)
                self.c.publish(f"{self.name}/heartbeat",
                               random.getrandbits(32), qos=2)
                self.rng = random.getstate()
                counter = 0
