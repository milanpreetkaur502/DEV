#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import time


MQTT_BROKER = "" # AWS ARN
PORT = 8883
MQTT_KEEP_INTERVAL = 44
TOPIC = "testThings_DE/booted"

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Publish Client Connected\n")
		
	else:
		print("Bad connection: Publish Client")


def on_publish(client, userdata, message):

	print("Device Status set to Booted.")
	# print("File names published to topic.\n\nDisconnecting from publish client...\n")
	client.disconnect()

def update_boot_status(serialID):
	rootCA = f'certificates_{serialID}/AmazonRootCA1.pem'
	cert = f'certificates_{serialID}/{serialID}-certificate.pem.crt'
	privateKey = f'certificates_{serialID}/{serialID}-private.pem.key'

	payload = {
	"serialID":serialID,
	"bootStatus" : True
	}
	payload = json.dumps(payload)


	pubClient = mqtt.Client('digitalEntomologist')
	# Setting Certificates
	pubClient.tls_set(rootCA, cert, privateKey)

	# Callback functions
	pubClient.on_connect = on_connect
	pubClient.on_publish = on_publish
	
	# Connecting to broker and publishing payload.
	pubClient.connect(MQTT_BROKER, PORT, MQTT_KEEP_INTERVAL)
	pubClient.publish(TOPIC, payload, 1)

	pubClient.loop_forever()