import os
import subprocess


def create_files():

	filename = os.getcwd() + '/bubble/' + 'environment.coffee'

	# w+ means write. # r means to read. # a means to append.
	f = open(filename,"w+")
	f.write('HAHAHAHAHA')
	f.close()

create_files()


'''
1) Create environment.coffee file.

2) Paste credentials in there.

3) Change etc/hosts 127.0.0.1 to local.bubble.is


'''
