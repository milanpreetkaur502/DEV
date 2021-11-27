#! /usr/bin/env python
import os
import re
import cv2
import numpy as np
from datetime import datetime
import time
import random

DEFAULT_CAMERA_NAME = '/dev/v4l/by-id/usb-046d_0825_6DCDEF50-video-index0'

device_num = 0
if os.path.exists(DEFAULT_CAMERA_NAME):
    device_path = os.path.realpath(DEFAULT_CAMERA_NAME)
    device_re = re.compile("\/dev\/video(\d+)")
    info = device_re.match(device_path)
    if info:
        device_num = int(info.group(1))
        print("Using default video capture device on /dev/video" + str(device_num))
cap = cv2.VideoCapture(device_num)
while True:
    success, img = cap.read()
    cv2.imshow("cam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
