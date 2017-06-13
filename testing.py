import os
import subprocess

def node_check():
	reading = os.popen('node -v').read()

	# If the array count is 0, gem does not exist.
	if(len(reading.split()) == 0):
		return False
	else:
		return True



repo_split = ('git clone ' + 'https://github.com/joshyhargreaves/cmparch').split()


repo_path = os.path.dirname(os.path.abspath(__file__)) + '/cmparch'


subprocess.Popen(repo_split, cwd=repo_path).communicate()
