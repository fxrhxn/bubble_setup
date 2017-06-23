import os
import subprocess


try:
    os.remove('efs')
except OSError as error:
    print error
