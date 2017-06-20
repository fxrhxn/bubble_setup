'''

What does this do?

This simple script replaces localhost on the employees computer and changes it to local.bubble.is

'''

import fileinput
import os
import subprocess



# Change etc/hosts to local.bubble.is from localhost
for i, line in enumerate(fileinput.input('/private/etc/hosts', inplace=1)):
	sys.stdout.write(line.replace('localhost', 'local.bubble.is'))  # replace 'sit' and write
	if i == 4: sys.stdout.write('\n')  # write a blank line after the 5th line

print('Changed localhost to local.bubble.is')
