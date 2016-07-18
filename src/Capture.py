# coding: utf-8

import cv2
from subprocess import call
import atexit
from Operations import OperatorBase

# Image file path
TEMP_FILE_PATH = "/home/pi/python/sandbox/twitterRobot/image/temp.jpg"
# Stop cmd shell
STOP_CMD = "sudo bash /home/pi/python/sandbox/twitterRobot/src/stopCamera.sh"

class Capture(OperatorBase):

	def __init__(self, tweet):
		super(Capture, self).__init__("capture", 0)
		self.tweet = tweet
		# Call reset servo shell
		call(STOP_CMD.strip().split(" "))
		# Get camera capture instance
		self.cap = cv2.VideoCapture(0)
		# Register cleanup handler at exit
		atexit.register(self.cleanup)

	# Clean up GPIO on exit
	def cleanup(self):
		call(STOP_CMD.strip().split(" "))

	# Concrete methods of super class
	def operate(self, args, tweet_id):
		self.capture_image(TEMP_FILE_PATH)
		self.tweet.update_with_media(TEMP_FILE_PATH, "I took capture!", tweet_id)
	
	def check_args(self, args):
		return True

	def capture_image(self, save_file_path):
		ret, frame = self.cap.read()
		cv2.imwrite(save_file_path, frame)

