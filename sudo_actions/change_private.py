'''

What does this do?

This simple script replaces localhost on the employees computer and changes it to local.bubble.is

'''

import fileinput
import os
import sys
import subprocess



# Change etc/hosts to local.bubble.is from localhost
for i, line in enumerate(fileinput.input('/private/etc/hosts', inplace=1)):

	# replace 'localhost' with local.bubble.is
	sys.stdout.write(line.replace('localhost', 'local.bubble.is'))
	
	print('Changed localhost to local.bubble.is')
