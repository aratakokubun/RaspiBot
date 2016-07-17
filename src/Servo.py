# coding: utf-8

import RPi.GPIO as GPIO
import time

# Specify pin number as General Purpose Pin number
GPIO.setmode(GPIO.BCM)
# GP Pin number of servo input
SERVO_GPIO = 23
# Set servo pin
GPIO.setup(SERVO_GPIO, GPIO.OUT)

# Initialize servo
HZ = 50
servo = GPIO.PWM(SERVO_GPIO, HZ)
servo.start(0.0)

# Controllable range of DC
DC_MIN = 2
DC_MAX = 12

def angle2dc(angle):
	return DC_MIN + (DC_MAX - DC_MIN) * angle / 180.0

def check_angle(angle):
	return 0.0 <= angle < 180.0

def rotate_servo(angle=90.0):
	if check_angle(angle):
		dc = angle2dc(angle)
		print("dc = {0}".format(dc))
		servo.ChangeDutyCycle(dc)
		time.sleep(0.5)
		servo.start(0.0)
