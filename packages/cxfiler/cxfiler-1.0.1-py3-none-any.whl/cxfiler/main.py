import os
from .base import FileManager

#-==@h1 Script Entrypoint

#-==@method
def main():
	#-== The main entrypoint when executing this module as an application.
	# This starts the Blessed /Terminal object and then passes it to a
	# /FilemManager object which will run the application.
	# When the application exits, the directory it was within will be printed
	# as terminal output as well as to a file ( /.cxfilerexit ) within
	# the user's /HOME directory.
	# This file can be used to recall where FILER was when it exited.
	# The shell command below will change directory to where
	# FILER was pointed when it exited.
	#@codeblock
	# cd $(cat ~/.cxfilerexit)
	#@codeblockend

	home = os.environ['HOME']
	pwd = os.getcwd()
	fileman = FileManager(pwd)
	fileman.run()
	exit_dir = fileman.pwd
	with open(os.path.join(home, '.cxfilerexit'), 'w') as filerout:
		filerout.write(exit_dir)
	print(exit_dir)

if __name__ == '__main__':
	main()