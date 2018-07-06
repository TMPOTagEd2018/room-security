#!/usr/bin/python3

import paho.mqtt.client as mqtt

import monitor
import monitor.gyro
import monitor.heartbeat

import keyex

from processor import ThreatProcessor

from rx import Observable

from typing import Dict

monitors: Dict[str, monitor.Monitor]  = {
    "door/gyro": monitor.gyro.GyroMonitor(1),
    "box/gyro": monitor.gyro.GyroMonitor(2),
    "door/heartbeat": monitor.heartbeat.HeartbeatMonitor(1),
    "room/heartbeat": monitor.heartbeat.HeartbeatMonitor(2),
    "box/heartbeat": monitor.heartbeat.HeartbeatMonitor(3)
}

threats = Observable.merge(*map(lambda m: m.threats, monitors.values()))

processor = ThreatProcessor(threats, 5)

monitors["door/heartbeat"].input(0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("door/gyro")
    client.subscribe("door/imu")
    client.subscribe("door/contact")
    client.subscribe("door/heartbeat")
    client.subscribe("door/key")

    client.subscribe("room/lux")
    client.subscribe("room/pir")
    client.subscribe("room/range")
    client.subscribe("room/heartbeat")
    client.subscribe("room/key")

    client.subscribe("box/gyro")
    client.subscribe("box/contact")
    client.subscribe("box/range")
    client.subscribe("box/heartbeat")
    client.subscribe("box/key")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg: mqtt.MQTTMessage):
    if msg.topic.endswith("/key"):
        they_pk = msg.payload.decode()

    else:
        monitors[msg.topic].input(msg.payload.decode())
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.90.12.213", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()