# coding: utf-8

import Servo
import Capture
import AirConditioner as Ac

SERVO = "servo"
PHOTO = "photo"
AIRCON = "aircon"

OPERATION_INDEX = 2

TEMP_FILE_PATH = "/home/pi/python/sandbox/twitterRobot/image/temp.jpg"

class Operator:

	def __init__(self, tweet):
		self.tweet = tweet

	"""
	Operation mention is constructed as below.
	@RaspiBotTwi [^\s]+ OPERATION ARG1 ARG2 ...
	"""
	def operate(self, text):
		args = text.split(" ")

		operation = args[OPERATION_INDEX]
		# select operation
		if operation == SERVO:
			if len(args) < 4:
				print("Number of argument is insufficient.")
				return
			try:
				angle = float(args[OPERATION_INDEX + 1])
				Servo.rotate_servo(angle=angle)
			except:
				print("Invalid arguments")
		elif operation == PHOTO:
			Capture.capture_image(TEMP_FILE_PATH)
			self.tweet.tweet_with_media(TEMP_FILE_PATH, "Take picture.")
		elif operation == AIRCON:
			if len(args) < 4:
				print("Number of argument is insufficient.")
				return
			option = args[OPERATION_INDEX + 1]
			Ac.send_ac_cmd(option)
