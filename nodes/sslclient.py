import paho.mqtt.client as paho
import paho.mqtt.publish as pub
import paho.mqtt.subscribe as sub
#not really using these two here but i jsut put them
import socket
import time

broker = "Taged"
#broker is the mothernode




HOST = '192.168.4.1'
PORT = 8883

node1 = paho.Client("node1")
node1.tls_set('')  #<< Put CA certificate from raspi's here
def on_connect:
    global flag
    flag = True
node1.on_connect = on_connect
node1.connect(broker, PORT)
while not flag: 
    node1.loop
    time.sleep(1)
node.pub("")