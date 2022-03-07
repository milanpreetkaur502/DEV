import cv2
cap=cv2.VideoCapture(0)
while True:
    sucess,img=cap.read()
    cv2.imshow('webcam',img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break