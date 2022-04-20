import os
import re
import cv2
import numpy as np
from datetime import datetime
import time
import random
DEVICE_INDEX =  "DEFAULT_CAMERA_NAME= '/dev/v4l/by-id/usb-e-con_systems_See3CAM_130_3B128E0B-video-index0'
                device_num = 0
                if os.path.exists(DEFAULT_CAMERA_NAME):
                    device_path = os.aoth.realpath(DEFAULT_CAMERA_NAME)
                    device_re = re.compile("\dev/\video(\d+)")
                    info = device_re.match(device_path)
                    if info:
                        device_num = int(info.group(1))
                        print("Using default video capture device on /dev/video" + str(device_num))
                cap=cv2.VideoCapture(device_num)"
                 


cap=cv2. VideoCapture(f"v4l2src device={DEVICE_INDEX} ! video/x-raw, width=640, height=480, format=(string)UYVY, framerate=60/1 ! decodebin ! videoconvert ! appsink",cv2.CAP_GSTREAMER)
    


        


def rescale_frame(frame, percent=71): #Setting parameters
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

while (True):
    ret1, frame11 = cap.read()
    ret1, frame12 = cap.read()

    diff1 = cv2.absdiff(frame11, frame12)#Absoulte difference between the pixels of the  1st and 2nd image frame or By using this we will be able to extract just the pixels of the objects that are moving

    gray1 = cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY)# converting this difference into gray scale mode and  grayscale images are single-dimensional, Reduces model complexity

    blur1 = cv2.GaussianBlur(gray1, (5, 5), 0)#Gaussian filter is a low-pass filter that removes the high-frequency components.

    _, tresh1 = cv2.threshold(blur1, 40, 255, cv2.THRESH_BINARY)# way to extract useful information encoded into pixels while minimizing background noise or upto which we want motion to be detected

    dilated1 = cv2.dilate(tresh1, None, iterations=3)#iterations means how accurate our smoothening will be if we inc background noise aajegi.

    contours1, _ = cv2.findContours(dilated1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # points at which motion is happening.

    for contour in contours1:
        (x, y, w, h) = cv2.boundingRect(contour)# making of rectangular frame.
        if cv2.contourArea(contour) < 2000: # if area of contour is less than 2000, then we are going to do nothing.But if its greater than 2000, a rectangle will be drawn.
            continue
        cv2.rectangle(frame11, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame11, "Status: {}".format('Insect captured'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        t = time.localtime()
        path = 'E:/capture/' # path were images will be stored
        num = random.random()
        filename = path + str(t[0]) + str(t[1]) + str(t[2]) + "_" + str(t[3]) + str(t[4]) + str(t[5]) + str(num) + ".jpg"
        cv2.imwrite(filename, frame11, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        print('Image being capture...', filename)

    # cv2.line(frame, (0, 300), (200, 200), (0, 255, 0), 5)
    resizedframe11 = rescale_frame(frame11, percent=75)
    cv2.imshow('Ready to capture', resizedframe11)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
