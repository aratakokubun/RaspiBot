# coding: utf-8

from abc import ABCMeta, abstractmethod

# from Servo import Servo as Sv
# from Capture import Capture as Cp
# from AirConditioner import AirConditioner as Ac

# Length and index
OPERATION_INDEX = 2

class Operator:
	
	def __init__(self, tweet):
		from Servo import Servo as Sv
		from Capture import Capture as Cp
		from AirConditioner import AirConditioner as Ac
		from USonic import USonic as Us
		from DHT import DHT
		servo = Sv()
		capture = Cp(tweet)
		aircon = Ac()
		usonic = Us(tweet)
		dht = DHT(tweet)
		self.operations = [servo, capture, aircon, usonic, dht]

	"""
	Parse operation set from arguments.
	"""
	def parse_operations(self, args):
		index = 0
		operation_set = list()
		while index < len(args):
			name = args[index]
			index += 1
			# Fetch matched operation
			operation = self.fetch_operation(name)
			# Skip if operation empty
			if operation is None:
				continue
			# Fetch arguments
			arg_len = operation.get_length()
			# Check argument
			if index+arg_len > len(args):
				print("Number of arguments invalid. expected:{0}, actual:{1}".format(arg_len, len(args)-index))
				# Finish parse loop
				break
			operation_args = args[index:index+arg_len]
			index += arg_len
			if not operation.check_args(operation_args):
				# Skip operation
				continue
			# Add to operation_set
			operation_set.append([operation, operation_args])
			print("Selected operation: {0}, args: {1}".format(operation.get_name(), operation_args))
	
		return operation_set

	"""
	Fetch operation from listed operations.
	@param name : operation name
	"""
	def fetch_operation(self, name):
		for operation in self.operations:
			if operation.get_name() == name:
				return operation
		return None

	def exec_operations(self, operation_set, tweet_id):
		for operation, args in operation_set:
			operation.operate(args, tweet_id)

	"""
	Operation mention is constructed as below.
	@RaspiBotTwi [^\s]+ OPERATION ARG1 ARG2 ...
	"""
	def operate(self, text, tweet_id):
		args = text.split(" ")[OPERATION_INDEX:]
		# Parse operations
		operation_set = self.parse_operations(args)
		# Execute operations
		self.exec_operations(operation_set, tweet_id)

"""
Base class to be extended by each operator class
"""
class OperatorBase(object):
	__metaclass__ = ABCMeta

	def __init__(self, name, length):
		self.name = name
		self.length = length

	def get_name(self):
		return self.name

	def get_length(self):
		return self.length

	@abstractmethod
	def operate(self, args, tweet_id):
		pass

	@abstractmethod
	def check_args(self, args):
		pass
