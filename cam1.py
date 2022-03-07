from PIL import Image
import cv2
import numpy as np
import os
import threading
from datetime import datetime

class MotionRecorder(object):

    hist_threshold = 500    # motion sensitivity => higher the value lesser the sensitivity
    path = 0
    DEFAULT_CAMERA_NAME = '/dev/v4l/by-id/usb-e-con_systems_See3CAM_130_3B128E0B-video-index0'
    device_num = 0
    if os.path.exists(DEFAULT_CAMERA_NAME):
        device_path = os.path.realpath(DEFAULT_CAMERA_NAME)
        device_re = re.compile("\/dev\/video(\d+)")
        info = device_re.match(device_path)
        if info:
            device_num = int(info.group(1))
            print("Using default video capture device on /dev/video" + str(device_num))
    cap=cv2.VideoCapture(device_num)
    
   
    #cap = cv2.VideoCapture("videotestsrc ! video/x-raw, format=I420, width=640, height=480 ! vpuenc_h264 ! appsink",cv2.CAP_GSTREAMER)
    subtractor = cv2.createBackgroundSubtractorMOG2()
    # FourCC is a 4-byte code used to specify the video codec. The list of available codes can be found in fourcc.org.
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')     # for windows
    fps = 12
    img_counter = 0
    skip_counter = 0
    temp_img_for_video = []
    skip_first_few_frames = 0

    def _init_(self):
        pass

    def start_storing_img(self, img):
        blur = cv2.GaussianBlur(img, (19,19), 0)
        mask = self.subtractor.apply(blur)
        img_temp = np.ones(img.shape, dtype="uint8") * 255
        img_temp_and = cv2.bitwise_and(img_temp, img_temp, mask=mask)
        img_temp_and_bgr = cv2.cvtColor(img_temp_and, cv2.COLOR_BGR2GRAY)

        hist, bins = np.histogram(img_temp_and_bgr.ravel(), 256, [0,256])
        print(hist[255])

        if(self.skip_first_few_frames < 5) : 
            self.skip_first_few_frames += 1
        else : 
            if hist[255] > self.hist_threshold :
                self.skip_counter = 0
                self.img_counter += 1 
                self.temp_img_for_video.append(img)
            else : 
                self.skip_counter += 1
                if self.skip_counter >= 5 :
                    self.save_recording()

    def save_recording(self):
        if self.img_counter >= 1:   
            now = datetime.now()
            video_name = str(now.year) + str(format(now.month,'02d')) + str(format(now.day,'02d')) + str(format(now.hour,'02d')) + str(format(now.minute,'02d')) + str(format(now.second,'02d')) + ".avi"  
            out = cv2.VideoWriter("./"+video_name, self.fourcc, self.fps, (640,480))
            print(video_name)

            for image in self.temp_img_for_video : 
                out.write(image)

            self.temp_img_for_video.clear()
            self.img_counter = 0


    def start(self):
        while True :
            available, frame = self.cap.read()
            if available :
                self.start_storing_img(frame)
                #cv2.imshow("Motion Recorder",frame)
                if cv2.waitKey(1) & 0xFF == ord('x'):
                    break

    def end(self):
        self.save_recording()
        self.cap.release()
        cv2.destroyAllWindows()

MR = MotionRecorder()
MR.start()
MR.end()