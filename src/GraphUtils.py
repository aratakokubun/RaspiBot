# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def create_usonic_graph(usonic_log, fpath, axis_span=10):
	# List x and y data
	x = [usonic.get_date() for usonic in usonic_log]
	y = [usonic.get_distance() if usonic.get_distance() < 100 else 0  for usonic in usonic_log] # omit data over 100
	# Construct figure
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(x, y)
	# Set graph format

	locator = mdates.MinuteLocator(interval=axis_span)
	date_format = mdates.DateFormatter('%Y:%m:%d:%H:%M')
	ax.xaxis.set_major_locator(locator)
	ax.xaxis.set_major_formatter(date_format)
	fig.autofmt_xdate()
	# Save figure
	plt.savefig(fpath)

def create_dht_graph(dht_log, fpath, axis_span=10):
	x = [dht.get_date() for dht in dht_log]
	y_temp = [dht.get_temperature() for dht in dht_log]
	y_humid = [dht.get_humidity() for dht in dht_log]

	fig, (axL, axR) = plt.subplots(ncols=2, sharex=True)
	
	axL.plot(x, y_temp, color="r", linewidth=2)
	axL.set_ylabel('temperature[C]')
	axL.grid(True)

	axR.plot(x, y_humid, color="b", linewidth=2)
	axR.set_ylabel('humidify[%]')
	axR.grid(True)

	locator = mdates.MinuteLocator(interval=axis_span)
	date_format = mdates.DateFormatter('%Y:%m:%d:%H:%M')
	axL.xaxis.set_major_locator(locator)
	axL.xaxis.set_major_formatter(date_format)
	axR.xaxis.set_major_locator(locator)
	axR.xaxis.set_major_formatter(date_format)
	fig.autofmt_xdate()
	# Save figure$
	plt.savefig(fpath)

