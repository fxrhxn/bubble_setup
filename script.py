import os
import subprocess
import sys
import fileinput



## Find a way to check if the version exists.


#returns the output, ignores return code (unless ignore_fail is false)
def get_output(cmd, ignore_fail=True, no_verbose=False):
	try:
		if not no_verbose:
			print 'Checking ' + cmd
		return subprocess.check_output(cmd, shell=True)
	except subprocess.CalledProcessError, e:
		if ignore_fail:
			return e.output
		else:
			raise e

## Dependency class that does most of the heavy lifting. Currently we are only using the ensure function to make sure that we have the dependencies that are necessary.
class Dependency:
	def name(self):
		return self._name

	## MAIN FUNCTION USED - Checks if package is installed or not.
	def ensure(self):
		if self.check() == False:
			return { 'installed' : False, 'message' : self.name() + ' is not installed'}
		else:
			return { 'installed' : True, 'message' : self.name() + ' is already installed'}

	def check(self):
		return self.check_prod()

	def check_debug(self):
		raise Exception('No check routine defined for ' + self.name())

	def check_prod(self):
		return self.check_debug()

	def upgrade(self):
		return self.upgrade_debug()

	def upgrade_debug(self):
		print('')
		# fail('Installing dependency: ' + self.name())
		#print(self.name() + 'hahahaahhaha')


	def upgrade_prod(self): raise Exception('No upgrade routine defined')


## Make this None.
cached_pip_output = None

# Use this class to check for pip dependencies.
class PipDependency(Dependency):
	def __init__(self, package, version=None):
		self.package = package
		if version is not None:
			self.package += '==' + version
		self._name = 'pip install ' + self.package

	def check_debug(self):
		global cached_pip_output
		if cached_pip_output is None:
			cached_pip_output = get_output('pip freeze')

		return cached_pip_output.find(self.package) != -1

	def upgrade_prod(self): run(self._name)

## Class to check if a command exists.
class CmdExists(Dependency):
	def __init__(self, cmd, install, in_output = None):
		self._name = install
		self.cmd = cmd
		self.install = install
		self.in_output = in_output

	def check_debug(self):


		if self.in_output is not None:
			return get_output(self.cmd).find(self.in_output) != -1
		else:
			return no_error(self.cmd)

	def upgrade_prod(self):
		run(self.install)


## Use this class to check for NPM packages.
class GlobalNPM(CmdExists):
	def __init__(self, package, version):
		CmdExists.__init__(self, 'npm list -g --depth 1 ' + package, 'npm install -g ' + package + '@' + version, version)



# The main class that installs all of the Gems.
class GemDependency(Dependency):
	def __init__(self, gem):
		self.gem = gem
		self._name = 'ruby gem ' + self.gem

	def check_debug(self):
		cached_gem_output = get_output('gem list --local')
		return cached_gem_output.find(self.gem) != -1

	def upgrade_prod(self): run('gem install ' + self.gem)





## NPM commands we have to call.
npm_commands = [
	{'cmd' : 'coffee-script', 'v' : '1.6.3'},
	{'cmd' : 'node-inspector', 'v' : '0.12.1'},
	{'cmd' : 'shrinkpack', 'v' : '0.13.1'},
]

## Pip commands to install.
pip_commands = [
	{'package' : 'selenium', 'v' : '2.35'},
	{'package' : 'iso8601', 'v' : None}
]


# Gem commands to install.
gem_commands = [
	'listen',
	'sass',
	'rb-fsevent',
]

# Function that installs the packages.
def install_package(cmd, type):

	#Install the command w/ os packacge.
	os.system(cmd)


## This function checks if ruby  / brew / pip / node is installed.
def check_basics(cmd):

	## Get the current version of Ruby.
	reading = os.popen(cmd).read()

	# If the array count is 0, ruby does not exist.
	if(len(reading.split()) == 0):
		return False
	else:
		return True

'''
 Next 5 functions are installing functions.
'''

## Ruby is usually installed, here is the function anyways if it needs to be installed.
def install_ruby():
	## Install Ruby using homebrew.
	os.system('brew install ruby')

## Install pip.
def install_pip():
	## Link GBDM to use python with homebrew.
	os.system('brew link gbdm')
	## Install python using homebrew.
	os.system('brew install python')

## Gem is usually installed, but here is the function to install that shit.
def install_gem():
	print('Gem should be installed on all Macs.')

## Command to install homebrew, the legendary package manager.
def install_brew():
	os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')

## Command to install Node.
def install_node():

	# Install node.
	os.system('brew install node')

	# "n" is a library that allows you to change node versions.
	os.system('npm install -g n')

	# Get the version of node specified here.
	os.system('sudo n 0.12.15')

# Get the current line of directories.
cwd = os.getcwd()

# Split the directories up.
directories_split = cwd.split('/');

# Get the name of the current directory.
current_directory = directories_split[len(directories_split) - 1]


## Repo urls to clone.
repo_urls = ['https://github.com/bubblegroup/bubble', 'https://github.com/jphaas/bubble_private']


## Function to download repos
def download_repo(repo):

	## Split the repo because subprocess requires the repos to be broken into a list. --> ['git', 'clone', 'repo']
	repo_split = ('git clone ' + repo).split()


	## Clone "bubble_private" INSIDE of "bubble"
	if(repo == repo_urls[1]):


		## This is the repo path. It is supposed to download "bubble_private" inside of the bubble repository.
		#repo_path = os.path.dirname(os.path.abspath(__file__)) + '/bubble'

		repo_path = os.getcwd() + '/bubble'

		try:
			# Call the command that is split in the command line.
			subprocess.Popen(repo_split, cwd=repo_path).communicate()
			print('Finished Cloning: ' + repo)
		except OSError as Err:
			print(Err)
			## Incase there's some error, catch that fucker.
			print('ERORR - Error while cloning ' + repo)

	else:

		try:
			# Call the command that is split in the command line.
			subprocess.call(repo_split)

			print('Finished Cloning: ' + repo)
		except OSError as Err:
			print(Err)
			## Incase there's some error, catch that fucker.
			print('ERORR - Error while cloning ' + repo)


# Function that sends confirmation questions.
def confirm_question(question):
	question = raw_input(question + '(y / n)')

	if (question == 'y' or question == 'yes' or question == 'Y'):
		return True
	elif (question == 'n' or question == 'N' or question == 'no'):
		return False
	else:
		return False

# Function that creates files for us in other paths.
def file_creator(path, data, filename):

	print('Creating a file named ' +  '"' + filename + '"' + ' inside of ' + path)

	# Create a file with the open function.
	f = open(path + filename ,"w+")

	# Write the new data inside of the file.
	f.write(data)

	# Print closing message.
	print('Created ' + '"' + filename + '"'   + '')

	# Close the fie stream.
	f.close()


## Questions to confirm
confirmed_1 = True 	# 'Did you open bubble-app.slack.com?'
confirmed_2 = True	# 'Please go to bubble-bot and type in "new_developer"'
confirmed_3 = True	# 'Did you open bubble-app.slack.com?'



#------------------------------
print('Setup Script STARTED')
#---------------------------------
################################################################################
'''

	First Step - Check for prerequisites(Gem / Ruby / Brew / Pip ) + See if user is in desktop.

'''

print(current_directory)
if(current_directory != 'Desktop'):
	print('ERROR - Please make sure you are in the "Desktop" directory.')
else:

	# Check ruby and see correct version.
	if(check_basics('ruby -v') == False):
		install_ruby()
	else:
		print('ruby already installed.')

	## Check brew and find the correct version.
	if(check_basics('brew -v') == False):
		install_brew()
	else:
		print('brew already installed.')

	## Check pip and install the same version.
	if(check_basics('pip -V') == False):
		install_pip()
	else:
		print('pip already installed.')

	## Check gem and install the correct version.
	if(check_basics('gem -v') == False):
		install_gem()
	else:
		print('gem already installed.')

	# Check node and install it if it does not exist.
	if(check_basics('node -v') == False):
		install_node()
	else:
		print('node and npm already installed.')

################################################################################
	'''

		Second Step - Install Node, then NPM packages.

	'''
	# Loop through all of the commands and check them.
	for cmd in npm_commands:

		## Full command to install, and version.
		full_command = cmd['cmd'] + '@' + cmd['v']
		command = cmd['cmd']
		version = cmd['v']

		if(GlobalNPM(command, version).ensure()['installed']):
			print(command + ' already installed.')
		else:
			print('INSTALLING ' + command)
			install_package('sudo npm install -g ' + full_command, 'npm')



################################################################################
	'''

		Third Step - Install Pip Commands

	'''

	## Loop through all of the pip commands.
	for cmd in pip_commands:

		# No version specified.
		if(cmd['v'] == None):

			#Check to see if dependency is installed.
			if(PipDependency(cmd['package']).ensure()['installed']):
				print(cmd['package'] + ' already installed.')
			else:
				install_package('pip install ' + cmd['package'], 'pip')

		# Version is given.
		else:

			#Check to see if dependency is installed.
			if(PipDependency(cmd['package'], cmd['v']).ensure()['installed']):
				print(cmd['package'] + ' already installed.')
			else:
				install_package('pip install ' + cmd['package'] + '==' + cmd['v'], 'pip')


################################################################################
	'''

		Fourth Step - Install Gem Packages

	'''

	# Loop through all of the gem commands in the array.
	for cmd in gem_commands:

		# Check if GemDependency is installed.
		if(GemDependency(cmd).ensure()['installed']):
			print('Already installed ' + cmd)
		else:
			print('Installing ' + cmd)

			# Command to install the gem dependency.
			command = 'sudo gem install ' + cmd

			# Function that actually does the installing.
			install_package(command, 'gem')


#------------------------------
	print('DEPENDENCIES INSTALLED - Now Downloading Bubble / Bubble Private')
#---------------------------------
################################################################################
	'''

		Fifth Step  - Download Bubble, and Bubble Private.

	'''
	# Loop all of the repo urls and clone them.
	for url in repo_urls:
		download_repo(url)


################################################################################
	'''

		Sixth Step  - Bubble Site SETUP

	'''
	# Make the first confirmed question False to start the process..
	confirmed_1 = False

	# Repeating question to be answered.
	while confirmed_1 == False:

		if confirm_question('Did you open bubble-app.slack.com?  ') == False:

			print("We can't proceed unless you verify that you have opened bubble-app.slack.com.")
		else:

			# Set confirmed_1 to True( AKA closing it. )
			confirmed_1 = True

			# Set confirmed_2 to False( AKA activating it. )
			confirmed_2 = False

	# Repeating question to be answered.
	while confirmed_2 == False:

		if confirm_question('Please send a direct message to bubblebot and type in "new_developer"') == False:

			print("We can't move on unless this is done.")
		else:

			# Set confirmed_2 to True( AKA closing it. )
			confirmed_2 = True

			# Set confirmed_3 to False( AKA activating it. )
			confirmed_3 = False


	# Repeating question to be answered.
	while confirmed_3 == False:


		if confirm_question('Did the credentials to print out? It may take a while. [20 - 30 minutes]') == False:

			print("We can't move on unless this is done.")
		else:
			confirmed_3 = True

			# Path for the credentials file.
			credential_path = os.getcwd() + '/bubble/lib/'

			# Pass data to file creator, and create the file with the data.
			file_creator(credential_path, '##INSIDE OF VIM press escape to finish, and ":wq" to save. Press I to insert.', 'credentials.coffee')

			# Notify user of VIM transition.
			confirm_question('We are going to move towards a VIM screen to enter your credentials, press any key to continue.')

			os.system('vim bubble/lib/credentials.coffee')

			# Change etc/hosts to local.bubble.is from localhost
			confirm_question('Please change localhost to local.bubble.is, in the NEXT vim screen.')
			os.system('sudo vim /private/etc/hosts')


#------------------------------
	print('Setup Script ENDED')
#---------------------------------











# Fin
