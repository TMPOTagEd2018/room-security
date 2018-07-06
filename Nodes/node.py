import keyex
import paho.mqtt.publish as pub
import paho.mqtt.subscribe as sub
from smbus import SMBus

bus = SMBus(1)

HOST = '192.168.4.1'
PORT = 1883

def run(self, name, address, sensor):
    dh = keyex.DiffieHellman()
    
    my_pk = dh.gen_public_key()
    pub.single(f"{name}/key", payload=my_pk, qos=1, hostname=HOST, port=PORT)
    they_pk = sub.simple(f"{name}/key", hostname=HOST, port=PORT)
    
    sk = dh.gen_shared_key(they_pk)
    seed = int(sk, 16)

    def recv():
        return bus.read_byte(address)

    while True:
        result = recv()
        pub.single(f"{name}/{sensor}", payload=result, qos=1)
