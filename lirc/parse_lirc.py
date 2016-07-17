# coding: utf-8

import sys

argvs = sys.argv
argc = len(argvs)

if (argc < 2):
	print ("Argument error")
	quit()

f = open(argvs[1])
# Omit first line
line = f.readline()
# Read lines after second
line = f.readline()

count = 0

while line:
	print (line.split(' ')[1].strip()), 
	line = f.readline()
	count += 1
	# Insert return to prevent long lines
	if (count > 20):
		count = 0
		print

f.close()
