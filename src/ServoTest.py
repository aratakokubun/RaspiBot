# coding: utf-8

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SERVO_GPIO = 23
GPIO.setup(SERVO_GPIO, GPIO.OUT)

def calc_duty(angle):
		return (1.0 + angle/180.0) / 20.0 *100.0

# Set servo pin and 20ms / 50Hz
servo = GPIO.PWM(SERVO_GPIO, 50)
servo.start(0.0)
"""
# 0 degree
angle = 0.0
new_duty = calc_duty(angle=angle)
# print(new_duty)
servo.start(new_duty)
print("angle = {0}".format(angle))
time.sleep(2)

# 180 degree
angle = 180
new_duty = calc_duty(angle=angle)
# print(new_duty)
servo.start(new_duty)
print("angle = {0}".format(angle))
time.sleep(5)

# test
servo.start(5)
time.sleep(2)
"""

for dc in range(2, 12, 1):
	servo.ChangeDutyCycle(dc)
	print("dc=%d" % dc)
	time.sleep(2)
