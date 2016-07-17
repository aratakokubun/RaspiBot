# coding: utf-8

import cv2
from subprocess import call

# Call reset servo shell
cmd = "sudo bash /home/pi/python/sandbox/twitterRobot/src"
call(cmd.strip().split(" "))

# Get camera capture instance
cap = cv2.VideoCapture(0)

def capture_image(save_file_path):
		ret, frame = cap.read()
		cv2.imwrite(save_file_path, frame)
