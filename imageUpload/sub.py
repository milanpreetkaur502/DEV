#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import ast
import time


def on_message(client, userdata, message):

	recievedPayload = message.payload.decode('utf-8')

	# Writing recieved payload in file.

	# Write proper json writing code
	# payload = {'files': list of dicts with filename as key and urls as value.}
	with open("signedUrls.json","w") as f:
		f.write(recievedPayload)

	print("Signed URLs recieved.\n\nDisconnecting with Subscriber's client....\n")
	client.disconnect()


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Subscribe Client Connected")
		
	else:
		print("Bad connection: Subscribe Client")
	

def start_subscribe(broker, port, interval, clientName, topic, qos, rootCA, cert, privateKey):

	# AWS Subscription Client
	subClient = mqtt.Client(clientName)

	# Setting Cerificates
	subClient.tls_set(rootCA, cert, privateKey)

	# Callback function
	subClient.on_connect = on_connect
	subClient.on_message = on_message

	# Connecting and Subcribing to topic.
	subClient.connect(broker, port, interval)

	subClient.subscribe(topic, qos)

	subClient.loop_forever()
