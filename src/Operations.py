# coding: utf-8

import Servo
import Capture

SERVO = "servo"
PHOTO = "photo"

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
			try:
				angle = float(args[OPERATION_INDEX + 1])
				Servo.rotate_servo(angle=angle)
				print(angle)
			except TypeError:
				print("Invalid Operation")
			except:
				print("Invalid arguments")
		elif operation == PHOTO:
			Capture.capture_image(TEMP_FILE_PATH)
			self.tweet.tweet_with_media(TEMP_FILE_PATH, "Take picture.")

