# coding: utf-8

import RPi.GPIO as GPIO
import time
import atexit

from Operations import OperatorBase

# GP Pin number of servo input
SERVO_GPIO = 23

# Servo drive Hz
HZ = 50

# Controllable range of DC
DC_MIN = 2
DC_MAX = 12

class Servo(OperatorBase):

	def __init__(self):
		super(Servo, self).__init__("servo", 1)
		# Specify pin number as General Purpose Pin number
		GPIO.setmode(GPIO.BCM)
		# Set servo pin
		GPIO.setup(SERVO_GPIO, GPIO.OUT)
		# Initialize servo
		self.init_servo()
		# Register cleanup handler at exit
		atexit.register(self.cleanup)

	# Clean up GPIO on exit
	def cleanup(self):
		self.servo.ChangeDutyCycle(DC_MIN)
		time.sleep(0.5)
		self.servo.stop()
		GPIO.cleanup(SERVO_GPIO)

	"""
	Initialize GPIO servo.
	"""
	def init_servo(self):
		self.servo = GPIO.PWM(SERVO_GPIO, HZ)
		self.servo.start(0.0)

	# Concete methods of super class
	def operate(self, args, tweet_id):
		angle = float(args[0])
		self.rotate_servo(angle=angle)
	
	def check_args(self, args):
		try:
			angle = float(args[0])
			if self.check_angle(angle):
				return True
			else:
				return False
		except:
			return False

	"""
	Convert angle to duty cycle.
	@param angle : angle to convert
	"""
	def angle2dc(self, angle):
		return DC_MIN + (DC_MAX - DC_MIN) * angle / 180.0

	"""
	Check angle arguments.
	@param angle : angle to check
	"""
	def check_angle(self, angle):
		return 0.0 <= angle < 180.0

	"""
	Rotate servo with specified angle.
	@param angle : target angle
	"""
	def rotate_servo(self, angle=90.0):
		if self.check_angle(angle):
			self.angle = angle
			dc = self.angle2dc(angle)
			print("dc = {0}".format(dc))
			# Start servo
			# self.servo.start(0.0)
			self.servo.ChangeDutyCycle(dc)
			time.sleep(0.5)
			# Stop servo to prevent vibration
			# self.servo.stop()

