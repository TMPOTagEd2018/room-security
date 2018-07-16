import keyex
import random
import time

import paho.mqtt.client as paho
from smbus2 import SMBus


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
        print("Initiating key exchange.")

        dh = keyex.DiffieHellman()

        public_key = dh.gen_public_key()
        server_public_key = None

        def handler(client, data, message: paho.MQTTMessage):
            nonlocal server_public_key
            server_public_key = message.payload.decode()

        self.c.on_message = handler
        self.c.subscribe("server/key")
        self.c.publish(f"{self.name}/key", payload=public_key, qos=1)

        print(f"Sent my public key: {public_key}")
        print("Waiting for their public key...")

        start_time = time.time()

        while server_public_key is None:
            self.c.loop()

            if time.time() - start_time >= 30:
                print("Key exchange timed out.")
                return False

        server_public_key = int(server_public_key)

        print(f"Received server public key: {server_public_key}")

        self.c.on_message = None
        self.c.unsubscribe("server/key")

        sk = dh.gen_shared_key(server_public_key)

        print(f"Key exchange completed with server, shared key {sk}")

        random.seed(int(sk, 16))

        self.rng = random.getstate()

        return True

    def register(self, sensor, place, transform):
        self.sensors.append(Sensor(sensor, place, transform))

    def pipe(self, name, topic, pipeline):
        self.inputs.append(Input(name, topic, pipeline))

    def start(self):
        counter = 0

        while not self.exchange():
            pass

        print("Beginning sensor loop.")

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
            time.sleep(.25)

            counter = counter + 1
            if counter == 4:
                print("Sending heartbeat.")
                random.setstate(self.rng)
                self.c.publish(f"{self.name}/heartbeat",
                               random.getrandbits(32), qos=2)
                self.rng = random.getstate()
                counter = 0

            self.c.loop()
