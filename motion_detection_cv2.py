import cv2
import numpy as np
from datetime import datetime
import time

cap=cv2.VideoCapture(-1)

def rescale_frame(frame, percent=75):
    width= int(frame.shape[1] * percent/100)
    height= int(frame.shape[0] * percent/100)
    dim =(width,height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    
while (True):
    ret1, frame11 = cap.read()
    ret1, frame12 = cap.read()
    
    
    diff1 = cv2.absdiff(frame11, frame12)
    gray1 = cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(gray1, (5 ,5),0)
    _, tresh1 = cv2.threshold(blur1, 40, 255, cv2.THRESH_BINARY)
    dilated1 = cv2.dilate(tresh1, None, iterations=3)
    contours1, _ = cv2.findContours(dilated1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours1:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) <2000:
            continue
        cv2.rectangle(frame11, (x, y), (x + w, y + h), (0,255,0), 2)
        cv2.putText(frame11, "Status: {}".format("movement"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1 ,(0, 0, 255), 3)
        t= time.localtime()
        filename = str(t[0]) + str(t[2]) + "_" + str(t[3]) + str(t[4]) + str(t[5]) + ".jpg"
        cv2.imwrite(filename, frame11)
        
    resizedframe11 = rescale_frame(frame11, percent=75)
    cv2.imshow("ready to capture", resizedframe11)
        
       
        
    if cv2.waitKey(1) & 0xFF == ord("w"):
        break
         
            
cap.release()
cv2.destroyAllWindows()
