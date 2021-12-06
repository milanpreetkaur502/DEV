#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import ast
import time
import os
import multiprocessing
from sub import start_subscribe
from pub import start_publish
from imageUpload import image_upload_manager
from verification import start_verification

# AWS Setup

MQTT_BROKER = ""
PORT = 8883
MQTT_KEEP_INTERVAL = 44
rootCA = 'certificates/AmazonRootCA1.pem'
cert = 'certificates/certificate.pem.crt'
privateKey = 'certificates/private.pem.key'

BUCKET_NAME = "test-entomoligist"

# Publish Details

PUBLISH_CLIENT_NAME = 'digitalEntomologist'
PUBLISH_TOPIC = 'testThings_DE/generateURL'
PUBLISH_QoS = 1

# Subscribe Details

SUBSCRIBE_CLIENT_NAME = 'iot-data'
SUBSCRIBE_TOPIC = 'testThings_DE/getURL'
SUBSCRIBE_QoS = 0

# Verification Details

VERIFICATION_TOPIC = 'testThings_DE/fileUploaded'

# Buffer Storage Path
BUFFER_IMAGES_PATH = 'bufferStorage/'


def generate_payload(filesList):

	

	payload = {
		"bucket-name":BUCKET_NAME,
		"files": filesList
	}

	return json.dumps(payload)

def signed_url_file_exist():

	while "signedUrls.json" not in os.listdir():
		time.sleep(2)
	return True


def upload_manager(filesList):

	batchSize = len(filesList)
	
	publishPayload = generate_payload(filesList)
	

	# Create start_subscribe and start_publish as two processes by implementing mulitprocessess.
	p1 = multiprocessing.Process(target = start_subscribe, args = [
		MQTT_BROKER, 
		PORT,
		MQTT_KEEP_INTERVAL,
		SUBSCRIBE_CLIENT_NAME,
		SUBSCRIBE_TOPIC,
		SUBSCRIBE_QoS,
		rootCA,
		cert,
		privateKey])

	p2 = multiprocessing.Process(target = start_publish, args =[
		MQTT_BROKER, 
		PORT,
		MQTT_KEEP_INTERVAL,
		PUBLISH_CLIENT_NAME,
		PUBLISH_TOPIC,
		PUBLISH_QoS,
		publishPayload,
		rootCA,
		cert,
		privateKey])

	p1.start()
	p2.start()
	p1.join()
	p2.join()

	# Create a better implementation once the signedUrls.json file has been created.
	if signed_url_file_exist():
		
		p3 = multiprocessing.Process(target = start_verification, args = [
		MQTT_BROKER, 
		PORT,
		MQTT_KEEP_INTERVAL,
		SUBSCRIBE_CLIENT_NAME,
		VERIFICATION_TOPIC,
		SUBSCRIBE_QoS,
		batchSize,
		rootCA,
		cert,
		privateKey])

		p4 = multiprocessing.Process(target = image_upload_manager)

		p3.start()
		p4.start()
		p3.join()
		p4.join()


		os.remove('signedUrls.json')

def main():

	while len(os.listdir(BUFFER_IMAGES_PATH)):
		filesList = os.listdir(BUFFER_IMAGES_PATH)[:10]

		upload_manager(filesList)
			

if __name__ == '__main__':

	main()
	
