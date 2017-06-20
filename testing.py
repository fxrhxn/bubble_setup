import os
import subprocess



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
def file_creator(path,filename):

	print('Creating a file named ' +  '"' + filename + '"' + ' inside of ' + path)

	# Create a file with the open function.
	f = open(path + filename ,"w+")

	print('Created ' + '"' + filename + '"'   + '')


	# Close the fie stream.
	f.close()


## Questions to confirm
confirmed_1 = True 	# 'Did you open bubble-app.slack.com?'
confirmed_2 = True	# 'Please go to bubble-bot and type in "new_developer"'
confirmed_3 = True	# 'Did you open bubble-app.slack.com?'

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

		file_creator(credential_path, 'credentials.coffee')

		## Open the credentials.coffee VIM file
		os.system('vim ' + credential_path)












##
