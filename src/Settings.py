# coding: utf-8

import json

CONSUMER_KEY = "CONSUMER_KEY"
CONSUMER_SECRET = "CONSUMER_SECRET"
ACCESS_TOKEN = "ACCESS_TOKEN"
ACCESS_SECRET = "ACCESS_SECRET"
PERMITTED_ACCOUNT = "PERMITTED_ACCOUNT"
PERMITTED_ID = "PERMITTED_ID"

class Settings:
	
	def __init__(self, fpath):
		f = open(fpath, 'r')
		json_data = json.load(f)
		
		# parse data
		self.consumer_key = json_data[CONSUMER_KEY]
		self.consumer_secret = json_data[CONSUMER_SECRET]
		self.access_token = json_data[ACCESS_TOKEN]
		self.access_secret = json_data[ACCESS_SECRET]
		# self.permitted_users = json_data[PERMITTED_ACCOUNT]
		self.permitted_users = json_data[PERMITTED_ID]

		f.close()

	def get_consumer_key(self):
		return self.consumer_key

	def get_consumer_secret(self):
		return self.consumer_secret

	def get_access_token(self):
		return self.access_token

	def get_access_secret(self):
		return self.access_secret

	def get_permitted_users(self):
		return self.permitted_users

