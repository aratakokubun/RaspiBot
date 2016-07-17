# condign: utf-8

from subprocess import call

# linux command
CMD = "sudo irsend"

# count
ONCE = "SEND_ONCE"

# device name
DEV_NAME = "aircon"
# option
OFF = "off"
COOLER_ON = "cooler_on"

def send_cmd(count=ONCE, device=DEV_NAME, option=OFF):
	fqcmd = " ".join([CMD, count, device, option])
	call(fqcmd.strip().split(" "))

def send_off():
	send_cmd(option=OFF)

def send_cooler_on(trial=1):
	for _ in range(trial):
		send_cmd(option=COOLER_ON)

def send_ac_cmd(option):
	if option == COOLER_ON:
		send_cooler_on(trial=2)
	else:
		send_off()
