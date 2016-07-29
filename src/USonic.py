# codint: utf-8

import RPi.GPIO as GPIO
import time
import atexit
from Operations import OperatorBase
import sqlite3 as sqlite
import datetime
import GraphUtils as Gu

# GPIO PIN number
TRIG_GPIO = 17
ECHO_GPIO = 27

# Options
NOW = "now"
HOUR = "hour"
DAY = "day"
OPTIONS = [NOW, HOUR, DAY]

# Message
USONIC_NOW_FMT = "Current distance is {0}[cm]."
USONIC_LOG_FMT = "Distance log in {0}."

# Files
USONIC_GRAPH_TEMP = "./image/usonic_temp.png"
	
class USonic(OperatorBase):

	def __init__(self, tweet):
		super(USonic, self).__init__("usonic", 1)
		self.tweet = tweet
		# Specify pin number as General Puroise Pin number
		GPIO.setmode(GPIO.BCM)
		# Set usonic pin
		GPIO.setup(TRIG_GPIO, GPIO.OUT)
		GPIO.setup(ECHO_GPIO, GPIO.IN)
		# Initialize pin
		self.__init_usonic()
		# Register cleanup handler at exit
		atexit.register(self.__cleanup)

	def __cleanup(self):
		GPIO.cleanup(TRIG_GPIO)
		GPIO.cleanup(ECHO_GPIO)

	def __init_usonic(self):
		GPIO.output(TRIG_GPIO, GPIO.LOW)
		time.sleep(0.3)

	# Concrete methods of super class
	def operate(self, args, tweet_id):
		option = args[0]
		if option == NOW:
			self.__usonic_now(tweet_id)
		else:
			self.__usonic_log(tweet_id, span=option)

	def check_args(self, args):
		return args[0] in OPTIONS

	"""
	Usonic current data.
	@param tweet_id : operate tweet id
	"""
	def __usonic_now(self, tweet_id):
		distance = self.measure_distance()
		message = USONIC_NOW_FMT.format(str(distance))
		self.tweet.update(message, tweet_id)

	def __usonic_log(self, tweet_id, span=HOUR):
		now = datetime.datetime.now()
		if span == DAY:
			from_time = now - datetime.timedelta(days=1)
			axis_span = 120
		else:
			from_time = now - datetime.timedelta(hours=1)
			axis_span = 10
		db = USonicDB()
		log = db.select_between(from_time, now)
		Gu.create_usonic_graph(log, USONIC_GRAPH_TEMP, axis_span=axis_span)
		message = USONIC_LOG_FMT.format(span)
		self.tweet.update_with_media(USONIC_GRAPH_TEMP, message, tweet_id)

	def __fetch_log(self, tweet_id, from_time, to_time):
		# Read log from db file
		return self.db.select_between(from_time, to_time)

		
	"""
	Measure distance with usonic sensor
	"""
	def measure_distance(self):
		# Send pulse
		GPIO.output(TRIG_GPIO, True)
		time.sleep(0.00001)
		GPIO.output(TRIG_GPIO, False)
		# Wait while ECHO pin input
		while GPIO.input(ECHO_GPIO) == 0:
				signaloff = time.time()
		while GPIO.input(ECHO_GPIO) == 1:
				signalon = time.time()
		return USonic.__time_to_centm(signalon - signaloff)

	"""
	Convert usonic time to sentimetres.
	@param sec : usonic response time
	"""
	@classmethod
	def __time_to_centm(cls, sec):
		return sec * 17000


# Files
DB_FILE = "usonic/usonic.db"

# SQL
CREATE_TABLE_SQL = u"""
	CREATE TABLE IF NOT EXISTS USONIC_LOG (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		distance REAL
	);
	"""
INSERT_SQL = u"""
	INSERT INTO USONIC_LOG (distance) values (?);
"""
SELECT_BETWEEN_SQL = u"""
	SELECT * FROM USONIC_LOG 
	WHERE date BETWEEN ? AND ?;
"""
SELECT_SQL = u"""
	SELECT * FROM USONIC_LOG;
"""

class USonicDB:
	
	def __init__(self, db_file=DB_FILE):
		self.db_file = db_file
		try:
			self.conn = sqlite.connect(db_file)
			print("Connection established")
			self.__create_table()
		except sqlite.Error, e:
			print ("Sqlite connect error.")
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

	def insert_log(self, distance):
		try:
			self.conn.execute(INSERT_SQL, [distance])
			self.conn.commit()
		except sqlite.Error, e:
			print("Insert error.")

	def select_between(self, start, end):
		try:
			cursor = self.conn.cursor()
			cursor.execute(SELECT_BETWEEN_SQL, [start, end])
			return [USonicData(row[0], datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"), row[2]) for row in cursor]
		except sqlite.Error, e:
			print("Select error.")
			print(e)
			return []

	def select(self):
		try:
			cursor = self.conn.cursor()
			cursor.execute(SELECT_SQL)
			return [USonicData(row[0], datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S"), row[2]) for row in cursor]
		except sqlite.Error, e:
			print("Select error.")
			print(e)
			print []

class USonicData:
	
	def __init__(self, id, date, distance):
		self.id = id
		self.date = date
		self.distance = distance

	def get_id(self):
		return self.id

	def get_date(self):
		return self.date

	def get_distance(self):
		return self.distance


"""
On launching this python on main, get distance data and insert log.
"""
if __name__ == "__main__":
	db = USonicDB()
	usonic = USonic(None) # pass None object as tweet
	distance = usonic.measure_distance()
	db.insert_log(distance)

