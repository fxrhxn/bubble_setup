import os
import subprocess

def node_check():
	reading = os.popen('node -v').read()

	# If the array count is 0, gem does not exist.
	if(len(reading.split()) == 0):
		return False
	else:
		return True


print node_check()
