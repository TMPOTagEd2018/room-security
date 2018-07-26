import keyex
import random
import time

import paho.mqtt.client as paho
import serial
import queue
import threading


def abbrev(key: int):
    return hex(key)[:16] + hex(key)[-16:]


class Node:
    inputs = {}

    def __init__(self, name, addr):
        self.name = name

        print(f"node {name} initialized. Listening on {addr}.")

        self.serial = serial.Serial(addr, 115200)

        print(f"{addr} opened.")

        self.client = paho.Client(str(name))
        self.client.tls_set("ca.crt")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("192.168.4.1", 8883)
        self.client.loop_start()

        print(f"connected to server at 192.168.4.1.")

        self.started = False
        self.server_key = None

    def on_connect(self, client: paho.Client, data, rc, flags):
        self.client.subscribe("server/init", qos=2)
        print("subscribed to server/init")
        self.client.subscribe("server/key", qos=2)
        print("subscribed to server/key")
        for i in self.inputs.keys():
            self.client.subscribe(i, qos=1)
            print("subscribed to server/key", i)

    def on_message(self, client: paho.Client, rc, message: paho.MQTTMessage):
        if message.topic == "server/init" and self.started:
            # server just restarted, exchange keys again so it doesn't ignore us
            print("server/init received.")

            self.server_key = None

        elif message.topic == "server/key":
            try:
                self.server_key = int(message.payload.decode())
                print(f"server/key recieved: {abbrev(self.server_key)}")
            except:
                pass

        elif self.started and message.topic in self.inputs.keys():
            code = self.inputs[message.topic]
            if message.payload.decode() == "1":
                self.serial.write(bytes([code]))
            else:
                self.serial.write(bytes([~code & 0xFF]))

    def exchange(self):
        print("initiating key exchange.")

        dh = keyex.DiffieHellman()

        public_key = dh.gen_public_key()

        self.client.publish(f"{self.name}/key", payload=public_key, qos=1)

        print("sent my public key: " + str(public_key))
        print("waiting for their public key...")

        start_time = time.time()

        while self.server_key is None:
            time.sleep(0.1)

            if time.time() - start_time >= 30:
                print("key exchange timed out.")
                return False

        print("received server public key: " + abbrev(self.server_key))

        sk = dh.gen_shared_key(self.server_key)

        print("key exchange completed with server, shared key " + sk)

        random.seed(int(sk, 16))

        self.rng = random.getstate()

        return True

    def input(self, name: str, topic: str, code: int):
        self.inputs[f"{name}/{topic}"] = code

    def start(self):
        i, j = 0, 0
        self.started = True

        while not self.exchange():
            pass

        print("beginning sensor loop.")

        lines = queue.Queue()

        def serial_read(serial: serial.Serial, queue: queue.Queue):
            while True:
                rec = self.serial.readline().decode().strip()
                if ":" in rec and not rec.startswith("-"):
                    line = rec.split(":")
                    if len(line) != 2:
                        print(f"[warn] irregular line: {line}")
                    else:
                        lines.put(tuple(line))

        serial_thread = threading.Thread(target=serial_read, args=(self.serial, lines))
        serial_thread.daemon = True
        serial_thread.start()

        while True:
            try:
                name, data = lines.get_nowait()
                self.client.publish(f"{self.name}/{name}", data, qos=1)
            except queue.Empty:
                time.sleep(0.1)
                pass

            if self.server_key is None:
                while not self.exchange():
                    pass

            i = i + 1
            if i == 10:
                # print("sending heartbeat.")
                random.setstate(self.rng)
                self.client.publish(f"{self.name}/heartbeat", random.getrandbits(32), qos=2)
                self.rng = random.getstate()
                i = 0

                j = j + 1
                if j == 10:
                    print("[heartbeat] 10th heartbeat")
                    j = 0
