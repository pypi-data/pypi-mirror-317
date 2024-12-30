import shutil

from bwk.characters import UnicodeChars as UTF
from bwk import Window
from bwk.screen import Screen

from ..utils import FILELIST_WIDTH, FILE_DETAILS_HEIGHT
from ..strings import gettext as _

#-==@class
class RenameMenu(Screen):
	#-== When "Rename" is selected from the action menu,
	# you can type in a new name for the file, and press
	# /Enter to confirm the change.
	#
	#-== *Available command keys:*
	# @table
	# Key(s)              |
	# ----------------------------------------------------------
	# /Enter              | Confirm the name typed as the new name of the file
	# /Esc                | Back out of the rename (back to /ActionMenu screen)

	#-==@method
	def __init__(self, filemanager, name, commands={}):
		#-== Creates the screen for the "Rename" action.
		# @params
		# filemanager: a /FileManager object
		# name: the name of the screen
		# commands: a dictonary where each key is a keyboard code,
		#						and the value is a function which should execute
		#						when that key is pressed
		# x: the X-coordinate of where the rename action should
		#				render in the terminal window
		# y: the Y-coordinate of where the rename action should
		#				render in the terminal window

		super().__init__(filemanager, name, commands)
		self.x = FILELIST_WIDTH
		self.y = FILE_DETAILS_HEIGHT+1
		self.newname = ''

	def pre_process_input(self, key):
		if not key.is_sequence:
			self.add_char(key)

	def add_char(self, key):
		if key not in """:';"/""":
			self.newname += key

	def delete_char(self):
		self.newname = self.newname[:-1]

	def set_commands(self):
		self.commands['KEY_ENTER'] = self.confirm_rename
		self.commands['KEY_BACKSPACE'] = self.delete_char
		self.commands['KEY_ESCAPE'] = self.back_to_main
		# Note: 'b' is not included here as a command key
		# because it is used in renaming the file.

	def back_to_main(self):
		self.newname = ''
		self.man.curr_screen = self.man.screens.main

	def confirm_rename(self):
		if not os.access(self.man.pwd, os.X_OK | os.W_OK):
			raise PermissionError(_('error.write.denied'))
		oldfile = self.man.current_file
		try:
			shutil.move(oldfile.filename, self.newname)
		except PermissionError:
			raise PermissionError(_('errors.general.permissions'))

		self.man.collect_dir()
		new_index = self.man.find_filelist_index_by_name(self.newname)
		self.man.set_current_file(new_index)
		self.back_to_main()

	def render(self):
		content = _('rename.prompt').format(self.newname, UTF.block.full)

		mywin = Window(self.man.term, self.x, self.y, border=' '*8)
		mywin.content = content
		mywin.render()