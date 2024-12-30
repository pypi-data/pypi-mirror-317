import os
import shutil

from bwk import Window, echo, flush
from bwk.screen import Screen

from ..utils import FileType, FILELIST_WIDTH, FILE_DETAILS_HEIGHT
from ..strings import gettext as _

#-==@class
class ActionMenu(Screen):
	#-== The "action menu" is a menu which opens
	# below the file info panel on the right side of the terminal
	# which allows you to select actions you can perform
	# on the current file or a set of selected files.
	#
	#-== If you have selected one or more files
	# (via the /Space bar or /A key),
	# the action menu is acting upon those files.
	#-== If you do not have any files selected,
	# the action menu is acting upon the file
	# the cursor is currently pointing to.
	#
	#-== *Available command keys:*
	# @table
	# Key(s)              |
	# ----------------------------------------------------------
	# /Up \/ /Down arrows | Navigate up and down the list of actions available
	# /Enter              | Select the item the cursor is currently pointing to
	# /Esc \/ /B          | Back out of the action menu (back to /FileListMode screen)
	# /H                  | Show the help text
	# /Q                  | Quit

	#-==@method
	def __init__(self, filemanager, name, commands={}):
		#-== Creates the screen for the action menu.
		# @params
		# filemanager: a /FileManager object
		# name: the name of the screen
		# commands: a dictonary where each key is a keyboard code,
		#						and the value is a function which should execute
		#						when that key is pressed
		# x: the X-coordinate of where the action menu should
		#				render in the terminal window
		# y: the Y-coordinate of where the action menu should
		#				render in the terminal window

		super().__init__(filemanager, name, commands)
		self.current_index = 0
		self.x = FILELIST_WIDTH
		self.y = FILE_DETAILS_HEIGHT+1
		self.menu_items = []
		self.set_menu_items()
	
	def pre_process_input(self, key):
		self.set_menu_items()

	def post_process_input(self, key):
		# there's no menu items, then after pressing anything,
		# it should go back
		if len(self.menu_items) == 0:
			self.back_to_main()

	def set_menu_items(self):
		self.menu_items = []
		if self.check_copy_action():
			self.menu_items.append({'label': _('actions.labels.copy.here'), 'exec': self.copy_items})
		if self.check_move_action():
			self.menu_items.append({'label': _('actions.labels.move.here'), 'exec': self.move_items})
		if self.check_rename_action():
			self.menu_items.append({'label': _('actions.labels.rename'), 'exec': self.rename_item})
		if self.check_permissions_action():
			self.menu_items.append({'label': _('actions.labels.permissions'), 'exec': self.change_permissions})
		if self.check_delete_action():
			self.menu_items.append({'label': _('actions.labels.delete'), 'exec': self.delete_items})

	def set_commands(self):
		self.commands['KEY_UP'] = self.cursor_up
		self.commands['KEY_DOWN'] = self.cursor_down
		self.commands['KEY_ENTER'] = self.select_item
		self.commands['KEY_ESCAPE'] = self.back_to_main
		self.commands['b'] = self.back_to_main
		self.commands['h'] = self.show_help
		self.commands['q'] = self.man.quit

	def cursor_up(self):
		if self.current_index > 0:
			self.current_index -= 1

	def cursor_down(self):
		if self.current_index < len(self.menu_items)-1:
			self.current_index += 1

	def select_item(self):
		menu_function = self.menu_items[self.current_index]['exec']
		menu_function()

	def copy_items(self):
		if not os.access(self.man.pwd, os.X_OK | os.W_OK):
			raise PermissionError(_('error.write.denied'))
		for file in self.man.selected_files:
			try:
				shutil.copy2(file.path, '.', follow_symlinks=False)
			except PermissionError:
				raise PermissionError(_('error.copy.denied').format(file.filename))
		self.man.collect_dir()
		new_index = self.man.find_filelist_index_by_name(getattr(self.man.current_file, 'filename', ''))
		self.man.set_current_file(new_index)
		self.man.selected_files.clear()
		self.back_to_main()

	def move_items(self):
		if not os.access(self.man.pwd, os.X_OK | os.W_OK):
			raise PermissionError(_('error.write.denied'))
		for file in self.man.selected_files:
			try:
				shutil.move(file.path, '.')
			except PermissionError:
				raise PermissionError(_('error.move.denied').format(file.filename))
		self.man.collect_dir()
		new_index = self.man.find_filelist_index_by_name(getattr(self.man.current_file, 'filename', ''))
		self.man.set_current_file(new_index)
		self.man.selected_files.clear()
		self.back_to_main()

	def rename_item(self):
		self.man.curr_screen = self.man.screens.rename

	def change_permissions(self):
		# TODO: Add permissions stuff
		pass

	def delete_items(self):
		term = self.man.term

		vcenter = int(term.height / 2)
		echo(term.move_xy(0, vcenter - 4))

		echo(term.black_on_bright_red)
		alertwin = Window(term, 0, vcenter - 4, 
							height=7, title=_('actions.delete.window.title'))
		alertwin.content = '\n' + term.center(_('actions.delete.confirm.message')) + \
							'\n \n' + term.center(_('actions.delete.key.prompt'))
		alertwin.render()
		echo(term.normal)
		flush()

		waiting_for_valid_input = True
		confirm_delete = False
		while waiting_for_valid_input:
			c = term.inkey()
			if c == 'y':
				waiting_for_valid_input = False
				confirm_delete = True
			elif c == 'n':
				waiting_for_valid_input = False

		if confirm_delete:
			filelist = [self.man.current_file]
			if len(self.man.selected_files) > 0:
				filelist = self.man.selected_files
			for file in filelist:
				if file.filetype == FileType.DIR:
					shutil.rmtree(file.path)
				else:
					os.remove(file.path)
			self.man.collect_dir()
			self.man.set_current_file(self.man.current_index-1)
			self.man.selected_files.clear()
		self.back_to_main()


	def back_to_main(self):
		self.clear_menu()
		self.man.curr_screen = self.man.screens.main

	def show_help(self):
		self.man.curr_screen = self.man.screens.help

	def check_copy_action(self):
		if len(self.man.selected_files) < 1:
			return False
		return True

	def check_move_action(self):
		if len(self.man.selected_files) < 1:
			return False
		return True

	def check_rename_action(self):
		if len(self.man.selected_files) > 0:
			return False
		if self.man.current_file is None:
			return False
		return True

	def check_permissions_action(self):
		return False

	def check_delete_action(self):
		if len(self.man.selected_files) == 0 \
					and self.man.current_file is None:
			return False
		return True

	def render_menu(self, width, height):
		term = self.man.term
		rendered_menu = ['']
		i = 0
		for item in self.menu_items:
			item_str = '  '+item['label']
			if i == self.current_index:
				item_str = '  '+term.reverse+item['label']+term.normal
			rendered_menu.append(item_str)
			i += 1
		if len(self.menu_items) == 0:
			rendered_menu = [
				_('actions.empty.menu.message'),
				_('actions.empty.menu.key.prompt'),
			]
		return rendered_menu

	def render(self):
		term = self.man.term
		self.set_menu_items()
		menu_title = ''
		num_files = len(self.man.selected_files)
		if num_files > 0:
			menu_title = _('actions.menu.title.single')
			if num_files > 1:
				menu_title = _('actions.menu.title.multi')
			menu_title = _('actions.menu.title.single').format(num_files)

		actions = Window(term, self.x, self.y, border=' '*8,
							title=menu_title, title_align='left')
		actions.render_content = self.render_menu
		actions.render()

	def clear_menu(self):
		self.current_index = 0
