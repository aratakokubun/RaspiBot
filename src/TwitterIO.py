# coding: utf-8

import sys
import codecs
# import dateutil.parser
import datetime
import time
from peewee import *
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
from datetime import timedelta

from Settings import Settings as sts
from Operations import Operator

def get_oauth(consumer_key, consumer_secret, access_key, access_secret):
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	return auth

class Tweet():
	
	def __init__(self, auth):
		self.auth = auth
		self.api = API(auth)

	def tweet_with_media(self, fn, status):
		self.api.update_with_media(fn, status=status)

class Listener(StreamListener):

	permitted_users = []

	def set_permitted_users(self, permitted_users):
		self.permitted_users = permitted_users
	
	def init_operator(self, tweet):
		self.operator = Operator(tweet) 

	def filter_users(self, user):
		return user in self.permitted_users

	def on_status(self, status):
		if self.filter_users(status.author.name):
			text = status.text
			print(text)
			print(status.author)
			self.operator.operate(text)
		return True

	def on_error(self, status):
		print ("Stream error")
		return True

	def on_timeout(self):
		raise Exception

if __name__ == "__main__":
	settings = sts("json/settings.json") 
	auth = get_oauth(settings.get_consumer_key(), settings.get_consumer_secret(), settings.get_access_token(), settings.get_access_secret())
	listener = Listener()
	listener.set_permitted_users(settings.get_permitted_users())
	listener.init_operator(Tweet(auth))
	stream = Stream(auth, listener, secure=True)
	stream.filter(track=['@RaspiBotTwi'])
	stream.userstream()
