import os
import subprocess

import sys




def create_files(data):


	credential_path = os.getcwd() + '/bubble/' + 'test4.coffee'

	# w+ means write. # r means to read. # a means to append.
	f = open(credential_path,"w+")
	f.write(data)
	f.close()


print('Enter Credentials. Press Ctrl D to Save.')
userInput = sys.stdin.read()

create_files(userInput)


'''
1) Create environment.coffee file.

2) Paste credentials in there.

3) Change etc/hosts 127.0.0.1 to local.bubble.is


'''
