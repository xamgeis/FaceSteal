import numpy as np
import cv2
import sys

import RPi.GPIO as GPIO 
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#setup Y motor
GPIO.setup(18,GPIO.OUT)
while True:
	GPIO.output(18, GPIO.HIGH)
	time.sleep(0.0015)
	GPIO.output(18, GPIO.LOW)
	time.sleep(0.0015)

#setup X motor

