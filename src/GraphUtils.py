# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def create_usonic_graph(usonic_log, fpath):
	# List x and y data
	x = [usonic.get_date() for usonic in usonic_log]
	print(x)
	y = [usonic.get_distance() if usonic.get_distance() < 100 else 0  for usonic in usonic_log] # omit data over 100
	# Construct figure
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(x, y)
	# Set graph format
	hours = mdates.HourLocator()
	hours_format = mdates.DateFormatter('%Y:%m:%d:%H:%M')
	ax.xaxis.set_major_locator(hours)
	ax.xaxis.set_major_formatter(hours_format)
	fig.autofmt_xdate()
	# Save figure
	plt.savefig(fpath)

