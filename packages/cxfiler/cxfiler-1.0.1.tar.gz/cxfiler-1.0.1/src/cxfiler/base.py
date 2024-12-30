import os

from cerrax import DotDict
from bwk import echo, flush
from bwk.screen import BwkScreenManager

from .strings import gettext as _
from .utils import FileType, ScanDirHelper
from .screens import FileList, ActionMenu, RenameMenu, HelpText

#-==@class
class FileManager(BwkScreenManager):
	#-== The main class which runs the application loop (see the /run() method below).
	# @attributes
	# term:           the Blessed /Terminal object to control input/output
	# running:        a boolean which is set to /True if teh application loop is running
	# screens:        a /DotDict of /Screen objects, each keyed with a name
	# pwd:            the current absolute path of the running application
	# prev_pwd:       the previous /pwd of the running application
	# show_hidden_files: a boolean indicating if hidden files should be displayed
	# show_files:     a boolean indicating if non-directory files should be displayed
	# show_directories: a boolean indicating if directories should be displayed
	# filelist:       a list of /ScanDirHelper objects, each describing a file in the directory
	# selected_files: the list of selected files; each is a /ScanDirHelper object
	# total_files:    total count of all files within the current directory
	# displayed_files: count of files actually displayed in the window
	# current_dir:    the name of the current directory
	# current_index:  the index of the file the cursor is currently on
	# current_file:   the /ScanDirHelper object referencing the file the cursor is on
	# curr_screen:    the /Screen currently executing in the application loop

	# currently unused, potentially add ability
	# to see/use navigation history?
	MAX_PATH_HISTORY = 20

	#-==@method
	def __init__(self, pwd):
		#-== Creates an instance of the FILER application.
		# @params
		# term: a Blessed /Terminal object to control input and output
		# pwd:  the absolute path to start the application within

		super().__init__(auto_flush=True)

		self.show_hidden_files = False
		self.show_files = True
		self.show_directories = True

		self.pwd = pwd
		self.prev_pwd = pwd
		self.filelist = []
		self.selected_files = []
		self.total_files = 0
		self.displayed_files = 0
		self.current_dir = None
		self.current_index = None
		self.current_file = None

		self.goto_dir(pwd)
		self.running = False
		self.screens = DotDict(
			main = FileList(self, 'main'),
			actions = ActionMenu(self, 'actions'),
			help= HelpText(self, 'help'),
			rename= RenameMenu(self, 'rename'),
		)
		self.curr_screen = self.screens.main

	#-==@method
	def find_filelist_index_by_name(self, name):
		#-== @params
		# name: the filename of the file
		# @returns
		# The integer index of the file within /self.filelist .
		# Returns -1 if the /name was not found.

		i = 0
		for file in self.filelist:
			if file.filename == name:
				return i
			i += 1
		return -1

	#-==@method
	def is_selected(self, checkfile):
		#-== @params
		# checkfile: a /ScanDirHelper object
		# @returns
		# A boolean indicating if the file is in /self.selected_files

		for file in self.selected_files:
			if file.inode == checkfile.inode:
				return True
		return False

	#-==@method
	def goto_dir(self, path, set_current_by_name=None, record_history=True):
		#-== Changes the current directory and adjusts
		# all relevant information within /FileManager .
		# @params
		# path: the path to change to
		# set_current_by_name: a name to use when setting the current index
		# record_history: not currently used

		try:
			os.chdir(path)
			self.collect_dir()
			self.pwd = os.getcwd()
			self.current_dir = os.path.basename(self.pwd)
			current_index = self.calculate_file_index(set_current_by_name)
			self.set_current_file(current_index)
		except PermissionError:
			self.goto_dir(self.prev_pwd, set_current_by_name=os.path.basename(path))
			raise PermissionError(_('errors.general.permissions'))

	#-==@method
	def calculate_file_index(self, filename):
		#-== Attempts to determine a file's index in the filelist
		# by its name. If no such name is found,
		# it defaults to the first file in the filelist (index zero).

		set_current_index = 0
		if filename is not None:
			set_current_index = self.find_filelist_index_by_name(filename)
		if set_current_index < 0:
			set_current_index = 0
		return set_current_index

	#-==@method
	def set_current_file(self, index):
		#-== Changes the current file the cursor is on and adjusts
		# all relevant information within /FileManager .

		if index < 0:
			index = 0
		if len(self.filelist) > index:
			self.current_index = index
			self.current_file = self.filelist[index]
		else:
			self.current_index = None
			self.current_file = None

	#-==@method
	def pre_render(self):
		#-== Sets the previous working directory to the current one.
		# This ensures that the "up one level" command works as expected.

		self.prev_pwd = self.pwd


	#-==@method
	def handle_crash(self, exc):
		#-== Catches /PermissionError exceptions and renders an error message.
		# All other errors will cause a crash.
		# Probably need to find a more graceful way to handle this.

		if isinstance(exc, PermissionError):
			self.render_error(str(exc))
		else:
			raise

	#-==@method
	def collect_dir(self):
		#-== Compiles the list of files in the current directory
		# as a list of /ScanDirHelper objects and stores it in /self.filelist ,
		# then adjusts all relevant information.

		self.total_files = 0
		self.displayed_files = 0
		self.filelist = []
		with os.scandir() as dirlist:
			for file in dirlist:
				self.total_files += 1
				entry = ScanDirHelper(file)
				if self.is_displayable(entry):
					self.displayed_files += 1
					self.filelist.append(entry)
		self.filelist.sort(key=lambda x: x.filename.lower())

	#-==@method
	def is_displayable(self, entry):
		#-== Checks if the /entry will be displayed based on options
		# set in attributes of the object.
		# @params
		# entry: the file entry to check if displayable
		# @returns
		# /True if the file should be displayed, /False if not


		if entry.is_hidden_file() and not self.show_hidden_files:
			return False
		elif entry.filetype in [FileType.DIR] and not self.show_directories:
			return False
		elif entry.filetype not in [FileType.DIR] and not self.show_files:
			return False
		return True

	#-==@method
	def select_current(self):
		#-== Adds the file the cursor is pointing to
		# (as indicated by /self.current_file ) to /self.selected_files .

		if self.current_file is not None:
			self.selected_files.append(self.current_file)

	#-==@method
	def deselect_current(self):
		#-== Removes the file the cursor is pointing to
		# (as indicated by /self.current_file ) from /self.selected_files .

		if self.current_file is not None:
			self.selected_files.remove(self.current_file)

	#-==@method
	def render_error(self, msg):
		#-== Renders an error message in the middle of the terminal.
		# You can press any key to dismiss the error message.

		vcenter = int(self.term.height / 2)
		echo(self.term.move_xy(0, vcenter))
		echo(self.term.black_on_bright_red)
		echo(self.term.center(_('errors.user.display').format(msg)))
		echo(self.term.normal)
		flush()
		c = self.term.inkey()
