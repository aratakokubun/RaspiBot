# condign: utf-8

from subprocess import call
from Operations import OperatorBase
import atexit

# lirc commands
INIT_CMD = "sudo bash /home/pi/python/sandbox/twitterRobot/src/initLirc.sh"
STOP_CMD = "sudo bash /home/pi/python/sandbox/twitterRobot/src/stopLirc.sh"

# linux command
CMD = "sudo irsend"
# count
ONCE = "SEND_ONCE"
# device name
DEV_NAME = "aircon"
# option
OFF = "off"
COOLER_ON = "cooler_on"
OPTIONS = [OFF, COOLER_ON]

class AirConditioner(OperatorBase):
	
	def __init__(self):
		super(AirConditioner, self).__init__("aircon", 1)
		# Initialize camera
		call(INIT_CMD.strip().split(" "))
		# Register cleanup handler
		atexit.register(self.cleanup)

	def cleanup(self):
		call(STOP_CMD.strip().split(" "))

	# Concrete methods of super class
	def operate(self, args, tweet_id):
		self.send_ac_cmd(args[0])

	def check_args(self, args):
		return args[0] in OPTIONS

	# Send remote controll commands
	def send_cmd(self, count=ONCE, device=DEV_NAME, option=OFF):
		fqcmd = " ".join([CMD, count, device, option])
		call(fqcmd.strip().split(" "))

	def send_off(self):
		print("Cooler Off")
		self.send_cmd(option=OFF)

	def send_cooler_on(self, trial=1):
		print("Cooler On")
		for _ in range(trial):
			self.send_cmd(option=COOLER_ON)

	def send_ac_cmd(self, option):
		if option == COOLER_ON:
			self.send_cooler_on(trial=2)
		else:
			self.send_off()

