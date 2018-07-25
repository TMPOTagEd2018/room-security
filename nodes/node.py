import keyex
import random
import time

import paho.mqtt.client as paho
import serial
import queue
import threading


class Node:
    inputs = []

    def __init__(self, name, addr):
        self.name = name

        self.serial = serial.Serial(addr, 115200)
        self.client = paho.Client(str(name))
        self.client.tls_set("ca.crt")
        self.client.connect("192.168.4.1", 8883)
        self.client.subscribe("server/init")
        self.client.on_message = self.handler
        self.started = False
        self.server_key = None

        print(f"Node {name} initialized. Listening on {addr}")

    def handler(self, client: paho.Client, rc, message: paho.MQTTMessage):
        if message.topic == "server/init" and self.started:
            # server just restarted, exchange keys again so it doesn't ignore us
            print("Server/init received.")

            self.server_key = None
            self.exchange()

        elif message.topic == "server/key":
            self.server_key = int(message.payload.decode())

        elif self.started:
            self.serial.writeline(
                f"{message.topic}:{message.payload.decode()}")

    def exchange(self):
        print("Initiating key exchange.")

        dh = keyex.DiffieHellman()

        public_key = dh.gen_public_key()

        self.client.subscribe("server/key")
        self.client.publish(f"{self.name}/key", payload=public_key, qos=1)

        print("Sent my public key: " + str(public_key))
        print("Waiting for their public key...")

        start_time = time.time()

        while self.server_key is None:
            self.client.loop()

            if time.time() - start_time >= 30:
                print("Key exchange timed out.")
                return False

        print("Received server public key: " + str(self.server_key))

        self.client.on_message = None
        self.client.unsubscribe("server/key")

        sk = dh.gen_shared_key(self.server_key)

        print("Key exchange completed with server, shared key " + sk)

        random.seed(int(sk, 16))

        self.rng = random.getstate()

        return True

    def input(self, name, topic):
        self.inputs.append(f"{name}/{topic}")

    def start(self):
        counter = 0
        self.started = True

        while not self.exchange():
            pass

        print("Beginning sensor loop.")

        for input in self.inputs:
            self.client.subscribe(input, qos=1)

        lines = queue.Queue()

        def loop(serial: serial.Serial, queue: queue.Queue):
            rec = self.serial.readline().decode().strip()
            if ":" in rec and not rec.startswith("-"):
                name, data = rec.split(":")
                lines.put((name, data))

        loop_thread = threading.Thread(target=loop, args=(self.serial, lines))
        loop_thread.daemon = True
        loop_thread.start()

        while True:
            try:
                name, data = lines.get_nowait()
                print(f"{self.name}/{name}", data)
                self.client.publish(f"{self.name}/{name}", int(data), qos=1)
            except queue.Empty:
                time.sleep(0.1)
                pass

            counter = counter + 1
            if counter == 10:
                print("Sending heartbeat.")
                random.setstate(self.rng)
                self.client.publish(
                    f"{self.name}/heartbeat", random.getrandbits(32), qos=2)
                self.rng = random.getstate()
                counter = 0

            self.client.loop()
