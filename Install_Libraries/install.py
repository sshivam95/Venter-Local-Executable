'''
Author : Meet Shah

Date   : 10/07/2018

Purpose: I am writing this script so that ICMC users don't have to install all the python libraries manually.
		 This script will automatically install all the necessary dependencies. 'requirements.txt' file contains
		 list of all the librarires that user need on his system.

Source : Convert PY to EXE => https://www.youtube.com/watch?v=lOIJIk_maO4
		 Check py version during runtime => https://stackoverflow.com/questions/9079036/detect-python-version-at-runtime

Note   : Type in following command in cmd to make exe.
			pyinstaller -i "D:\Project\Venter\Install_Libraries\install_icon.ico" -F "D:\Project\Venter\Install_Libraries\install.py"
		 Please note that the this is just sample command, change the name of directory according to your need.
'''
import os
import sys
Manually = []
print("Don't close terminal while this script is running")

if sys.version_info[0] >= 3:

	try:
		with open('requirements.txt', 'r') as f:
			for line in f:
				line = line.replace('\n','')
				print("Currently installing: ", line)
				command = 'pip install ' + line
				try:
					os.system(command)
				except Exception as e:
					Manually.append(line)
					print('Following exception occured: \n', e)
	except:
		print("Please make sure 'requirements.txt' file and 'install.exe' are in same folder")

	if len(Manually) > 0:
		print("Please note that following libraries have been not installed in your system. Please contact support team they will guide you. \n \
			 Or else you can manually install it by yourself by typing following command. pip install 'library-name'. \n \
			 Following is the list of library you need to install: \n")

		for i in Manually:
			print(i)
else:
	print('Please install python 3 or higher version. Contact Venter team for more info.')

a = input('Press Enter to exit')

