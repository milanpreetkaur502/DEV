#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import ast
import time
from sub import start_subscribe

def on_publish(client, userdata, message):

	print("File names published to topic.\n\nDisconnecting from publish client...\n")
	client.disconnect()

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Publish Client Connected")
		
	else:
		print("Bad connection: Publish Client")


def start_publish(broker, port, interval, clientName, topic, qos, payload, rootCA, cert, privateKey):

	time.sleep(3)
	# AWS Publishing Cient
	pubClient = mqtt.Client(clientName)

	# Setting Certificates
	pubClient.tls_set(rootCA, cert, privateKey)

	# Callback functions
	pubClient.on_connect = on_connect
	pubClient.on_publish = on_publish
	
	# Connecting to broker and publishing payload.
	pubClient.connect(broker, port, interval)
	pubClient.publish(topic, payload, qos)

	pubClient.loop_forever()