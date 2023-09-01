import time
import io
import threading
import picamera
import grovepi
import RPi.GPIO as GPIO
import os
from grovepi import *

class Camera(object):
    thread = None
    frame = None
    last_access = 0

    def initialize(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        ultrasonic_ranger = 4
        sheets=0
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            camera.start_preview(alpha=100)
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                distant = ultrasonicRead(ultrasonic_ranger)
                #print(distant)
                time.sleep(1.5)
                if(distant < 30):
                    sheets +=1
                    current_directory = os.getcwd()
                    relative_path = 'static/capture_test' + str(sheets) + '.jpg'
                    absolute_path = os.path.join(current_directory, relative_path)
                    camera.capture(absolute_path)
                stream.seek(0)
                cls.frame = stream.read()
                stream.seek(0)
                stream.truncate()

                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
