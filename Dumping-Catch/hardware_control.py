#  하드웨어 제어 함수
import RPi.GPIO as GPIO
import time
from grovepi import *

# GPIO 모드와 모터 핀 번호를 설정합니다.
HORIZON_motor_pin = 18
VERTICAL_motor_pin = 17
GPIO.setmode(GPIO.BCM)

# 수평 모터 각도를 제어하는 함수입니다.
def HORIZON_motor_doAngle(angle):
    GPIO.setup(HORIZON_motor_pin, GPIO.OUT)
    HORIZON_motor_p = GPIO.PWM(HORIZON_motor_pin, 50)
    HORIZON_motor_p.start(0)
    #print("Angle: %d" % angle)
    HORIZON_motor_p.ChangeDutyCycle(angle)
    time.sleep(0.5)
    GPIO.setup(HORIZON_motor_pin, GPIO.IN)
    
# 수직 모터 각도를 제어하는 함수입니다.
def VERTICAL_motor_doAngle(angle):
    GPIO.setup(VERTICAL_motor_pin, GPIO.OUT)
    VERTICAL_motor_p = GPIO.PWM(VERTICAL_motor_pin, 50)
    VERTICAL_motor_p.start(0)
    #print("Angle: %d" % angle)
    VERTICAL_motor_p.ChangeDutyCycle(angle)
    time.sleep(0.5)
    GPIO.setup(VERTICAL_motor_pin, GPIO.IN)
