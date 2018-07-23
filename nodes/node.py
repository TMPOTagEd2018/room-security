import keyex
import random
import time

import paho.mqtt.client as paho
import serial


class MQTT_Input:
    name: str = ""
    topic: str = ""

    def __init__(self, n, t):
        self.name = n
        self.topic = t


class Node:
    inputs = []

    def __init__(self, name, addr, dummy=False):
        self.name = name
        self.addr = addr
        self.ser = serial.Serial(115200)
        self.c = paho.Client(str(name))
        self.c.tls_set("ca.crt")
        self.c.connect("10.90.12.213", 8883)

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

        print("Sent my public key: " + str(public_key))
        print("Waiting for their public key...")

        start_time = time.time()

        while server_public_key is None:
            self.c.loop()

            if time.time() - start_time >= 30:
                print("Key exchange timed out.")
                return False

        server_public_key = int(server_public_key)

        print("Received server public key: " + str(server_public_key))

        self.c.on_message = None
        self.c.unsubscribe("server/key")

        sk = dh.gen_shared_key(server_public_key)

        print("Key exchange completed with server, shared key " + sk)

        random.seed(int(sk, 16))

        self.rng = random.getstate()

        return True

    def input(self, name, topic):
        self.inputs.append(MQTT_Input(name, topic))

    def start(self):
        counter = 0

        while not self.exchange():
            pass

        print("Beginning sensor loop.")

        while True:
            rec = self.ser.readline()
            for i in self.inputs:
                mes = self.c.subscribe(f"{i.name}/{i.topic}", qos=1)
                self.ser.write(f"{i.topic}: {mes}")

            name, data = rec.split(":")
            print(f"{self.name}/{name}", int(data))
            self.c.publish(f"{self.name}/{name}", int(data), qos=1)

            counter = counter + 1
            if counter == 10:
                print("Sending heartbeat.")
                random.setstate(self.rng)
                self.c.publish(f"{self.name}/heartbeat",
                               random.getrandbits(32), qos=2)
                self.rng = random.getstate()
                counter = 0

            self.c.loop()
