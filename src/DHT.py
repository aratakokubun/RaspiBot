# coding: utf-8

import time
import atexit
import Adafruit_DHT
from Operations import OperatorBase
import GraphUtils as Gu
import sqlite3 as sqlite
import datetime

# GPIO Pin number
DHT_GPIO = 18

# Options
NOW = "now"
HOUR = "hour"
DAY = "day"
WEEK = "week"
OPERATIONS = [NOW, HOUR, DAY, WEEK]

# Command line parameters
SENSOR_ARGS = { '11': Adafruit_DHT.DHT11,
								'22': Adafruit_DHT.DHT22,
								'2302': Adafruit_DHT.AM2302 }

# Messages
DHT_NOW_FMT = "Current temperature: {0}, humidity: {1}"
DHT_FAIL_FMT = "Could not measure current state dht."
DHT_LOG_FMT = "Temperature and humidity in {0}."

# Files
DHT_GRAPH_TEMP = "./image/dht_temp.png"

class DHT(OperatorBase):

	def __init__(self, tweet, dht_ver=SENSOR_ARGS['11']):
		super(DHT, self).__init__("dht", 1)
		self.tweet = tweet
		self.dht_ver = dht_ver
		# Register cleanup handler at exit
		atexit.register(self.__cleanup)

	def __cleanup(self):
		pass

	# Number of trials
	MAX_TRIAL = 3
	# Concrete methods of super class
	def operate(self, args, tweet_id):
		option = args[0]
		if option == NOW:
			self.__dht_now(tweet_id)
		else:
			self.__dht_log(tweet_id, span=option)

	def check_args(self, args):
		try:
			return args[0] in OPERATIONS
		except:
			return False

	def __dht_now(self, tweet_id, trial=3):
		for _ in range(self.MAX_TRIAL):
			data = self.measure_dht()
			if data[0] is None and data[1] is None:
				continue
			message = DHT_NOW_FMT.format(data[0], data[1])
			self.tweet.update(message, tweet_id)
			return
		self.tweet.update(DHT_FAIL_FMT, tweet_id)

	def __dht_log(self, tweet_id, span=DAY):
		now = datetime.datetime.now()
		if span == DAY:
			from_time = now - datetime.timedelta(days=1)
			axis_span = 120
		elif span == WEEK:
			from_time = now - datetime.timedelta(days=7)
			axis_span = 1000
		else:
			from_time = now - datetime.timedelta(hours=1)
			axis_span = 10
		db = DHTDB()
		log = db.select_between(from_time, now)
		Gu.create_dht_graph(log, DHT_GRAPH_TEMP, axis_span=axis_span)
		message = DHT_LOG_FMT.format(span)
		self.tweet.update_with_media(DHT_GRAPH_TEMP, message, tweet_id)

	def measure_dht(self):
		humidity, temperature = Adafruit_DHT.read_retry(self.dht_ver, DHT_GPIO)
		return [humidity, temperature]


# Files
DB_FILE = "dht/dht.db"

# SQL
CREATE_TABLE_SQL = u"""
	CREATE TABLE IF NOT EXISTS DHT (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		temperature REAL,
		humidity REAL
	);
"""
INSERT_SQL = u"""
	INSERT INTO DHT (temperature, humidity) values (?, ?);
"""
SELECT_BETWEEN_SQL = u"""
	SELECT * FROM DHT
	WHERE date BETWEEN ? AND ?;
"""

class DHTDB:
	
	def __init__(self, db_file=DB_FILE):
		self.db_file = db_file
		try:
			self.conn = sqlite.connect(db_file)
			print("Connection established.")
			self.__create_table()
		except sqlite.Error, e:
			print("Sqlite connect error.")
		# Register cleanup handler at exit
		atexit.register(self.__cleanup)

	def __cleanup(self):
		try:
			self.conn.close()
			print("Connection closed.")
		except sqlite.Error, e:
			print("Sqlite connect error.")

	def __create_table(self):
		try:
			self.conn.execute(CREATE_TABLE_SQL)
			self.conn.commit()
		except sqlite.Error, e:
			print("Create table failed.")
			print(e)
	
	def insert_log(self, temperature, humidity):
		try:
			self.conn.execute(INSERT_SQL, (temperature, humidity, ))
			self.conn.commit()
		except:
			print("Insert error.")

	def select_between(self, start, end):
		try:
			cursor = self.conn.cursor()
			cursor.execute(SELECT_BETWEEN_SQL, (start, end, ))
			return [DHTData(row[0], datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"), row[2], row[3]) for row in cursor]
		except sqlite.Error, e:
			print("Select error.")
			return []


class DHTData:
	
	def __init__(self, id, date, temperature, humidity):
		self.id = id
		self.date = date
		self.temperature = temperature
		self.humidity = humidity

	def get_id(self):
		return self.id

	def get_date(self):
		return self.date

	def get_temperature(self):
		return self.temperature

	def get_humidity(self):
		return self.humidity


"""
On launching this python on main, get distance data and insert log.
"""
if __name__ == "__main__":
	db = DHTDB()
	dht = DHT(None) # pass None object as tweet
	for _ in range(3):
		data = dht.measure_dht()
		if data[0] is None and data[1] is None:
			continue
		break
	db.insert_log(temperature=float(data[1]), humidity=float(data[0]))
