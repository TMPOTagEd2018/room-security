#!/usr/bin/python3

import paho.mqtt.client as mqtt

import monitor
import monitor.gyro

from processor import ThreatProcessor

from rx import Observable

from typing import Dict

monitors: Dict[str, monitor.Monitor]  = {
    "door/gyro": monitor.gyro.GyroMonitor()
}

threats = Observable.merge(*map(lambda m: m.threats, monitors.values()))

processor = ThreatProcessor(threats, 5)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("door/gyro")
    client.subscribe("door/imu")
    client.subscribe("door/contact")

    client.subscribe("room/lux")
    client.subscribe("room/pir")
    client.subscribe("room/range")

    client.subscribe("box/accel")
    client.subscribe("box/contact")
    client.subscribe("box/range")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    e = msg.payload.decode()
    monitors[msg.topic].input(e)
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.90.12.213", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()