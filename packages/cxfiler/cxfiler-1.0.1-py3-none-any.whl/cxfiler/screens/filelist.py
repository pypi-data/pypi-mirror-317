from bwk.characters import UnicodeChars as UTF
from bwk import Window, Border, echo
from bwk.screen import Screen

from ..utils import FileType, PATH_WINDOW_HEIGHT, FILELIST_WIDTH, \
				FILE_DETAILS_HEIGHT, SCREEN_JUMP, FILETYPE_SYMBOL
from ..strings import gettext as _

#-==@class
class FileList(Screen):
	#-== The "main" screen of FILER.
	# This screen displays a list of files within
	# the directory on the left side, and displays
	# information about the file the cursor is pointing to
	# on the right side of the screen.
	# The left side is a fixed width, whereas
	# the right side stretches to fill the entire terminal.
	#
	#-== *Available command keys:*
	# @table
	# Key(s)              |
	# ----------------------------------------------------------
	# /Up \/ /Down arrows | Navigate up and down the list of files
	# /" \/ /?            | Navigate a full screenful up or down
	# /Left arrow         | Move up one to the parent directory
	# /Right arrow        | Move into the directory (if current file is a directory)
	# /Enter              | Open the action menu (switch to /ActionMenu screen)
	# /.                  | Show/hide hidden files
	# /D                  | Show/hide directories
	# /F                  | Show/hide nondirectory files
	# /Space              | Select/deselect current file
	# /A                  | Select/deselect all files
	# /H                  | Show the help text
	# /Esc \/ /B          | Quit
	# /Q                  | Quit

	def set_commands(self):
		self.commands['KEY_UP'] = self.cursor_up
		self.commands['KEY_DOWN'] = self.cursor_down
		self.commands["'"] = self.jump_up
		self.commands["/"] = self.jump_down
		self.commands['KEY_LEFT'] = self.parent_dir
		self.commands['KEY_RIGHT'] = self.into_dir
		self.commands['KEY_ENTER'] = self.action_menu
		self.commands['KEY_ESCAPE'] = self.man.quit
		self.commands['b'] = self.man.quit
		self.commands['.'] = self.toggle_hidden_files
		self.commands['d'] = self.toggle_directories
		self.commands['f'] = self.toggle_show_files
		self.commands[' '] = self.toggle_select
		self.commands['a'] = self.select_all
		self.commands['h'] = self.show_help
		self.commands['q'] = self.man.quit

	def cursor_up(self):
		if self.man.current_index is not None and self.man.current_index > 0:
			self.man.set_current_file(self.man.current_index-1)

	def cursor_down(self):
		if self.man.current_index is not None and self.man.current_index < len(self.man.filelist)-1:
			self.man.set_current_file(self.man.current_index+1)

	def jump_up(self):
		if self.man.current_index is not None and self.man.current_index > 0:
			newindex = self.man.current_index-SCREEN_JUMP
			if newindex < 0:
				newindex = 0
			self.man.set_current_file(newindex)

	def jump_down(self):
		if self.man.current_index is not None and self.man.current_index < len(self.man.filelist)-1:
			newindex = self.man.current_index+SCREEN_JUMP
			if newindex > len(self.man.filelist)-1:
				newindex = len(self.man.filelist)-1
			self.man.set_current_file(newindex)

	def parent_dir(self):
		self.man.goto_dir('..', set_current_by_name=self.man.current_dir)

	def into_dir(self):
		if self.man.current_file is not None and self.man.current_file.filetype == FileType.DIR:
			self.man.goto_dir(self.man.current_file.filename)

	def action_menu(self):
		self.man.curr_screen = self.man.screens.actions

	def show_help(self):
		self.man.curr_screen = self.man.screens.help

	def toggle_file_display(self, display_param_name):
		dparam = not getattr(self.man, display_param_name)
		setattr(self.man, display_param_name, dparam)
		self.man.collect_dir()
		newindex = self.man.find_filelist_index_by_name(self.man.current_file.filename)
		self.man.set_current_file(newindex)

	def toggle_hidden_files(self):
		self.toggle_file_display('show_hidden_files')

	def toggle_directories(self):
		self.toggle_file_display('show_directories')

	def toggle_show_files(self):
		self.toggle_file_display('show_files')

	def toggle_select(self):
		if self.man.current_file in self.man.selected_files:
			self.man.deselect_current()
		else:
			self.man.select_current()

	def select_all(self):
		if len(self.man.selected_files) > 0:
			self.man.selected_files.clear()
		else:
			self.man.selected_files = self.man.filelist.copy()

	def filelist_str(self, width, height):
		filelist_str = []
		term = self.man.term

		for file in self.man.filelist:
			outstr = ''
			fillchar = ' '
			if self.man.is_selected(file):
				fillchar = UTF.line.solid.horizontal
			if file == self.man.current_file:
				outstr += '->'
			else:
				outstr += (fillchar*2)
			symbol = FILETYPE_SYMBOL[file.filetype]
			if file.filetype == FileType.FILE:
				symbol = fillchar
			outstr += symbol+fillchar
			filename = file.filename
			if len(filename) >= width-4:
				filename = filename[:width-6]+'..'
			outstr += term.ljust(filename, width=width, fillchar=fillchar)

			filelist_str.append(outstr)

		scroll_distance = 0
		if self.man.current_index is not None and self.man.current_index > height-1:
			scroll_distance = self.man.current_index - height+1

		return filelist_str[scroll_distance:]

	def get_filetype_display(self):
		type = 'filetype.item'
		if self.man.show_files and not self.man.show_directories:
			type = 'filetype.file'
		if not self.man.show_files and self.man.show_directories:
			type = 'filetype.dir'
		if self.man.total_files == 1:
			type += '.single'
		else:
			type += '.multi'
		return _(type)

	def current_file_details(self):
		typestr = self.get_filetype_display()
		details_str = _('filelist.details').format(self.man.displayed_files,
													self.man.total_files,
													typestr)
		detail_file = self.man.current_file
		if detail_file:
			data = {
				'filename': detail_file.filename,
				'perms': str(detail_file.perms),
				'size': detail_file.size,
				'created': detail_file.created.strftime("%b %d,%Y %H:%M"),
				'modified': detail_file.modified.strftime("%b %d,%Y %H:%M"),
			}
			details_str += _('filelist.file.details').format(**data)
		return details_str


	def render(self):
		term = self.man.term
		echo(term.clear)

		echo(term.reverse)
		#path_border = Border()
		#path_border.bottom_border = UTF.line.double.horizontal
		path_window = Window(term, 0, 0, height=PATH_WINDOW_HEIGHT, border=None)
		path_window.content = self.man.pwd
		path_window.render()
		echo(term.normal)

		filelist_border = Border()
		filelist_border.right_border = UTF.line.double.vertical
		filelist_window = Window(term, 0, PATH_WINDOW_HEIGHT,
									width=FILELIST_WIDTH, border=filelist_border)
		filelist_window.render_content = self.filelist_str
		filelist_window.render()

		file_details_border = Border()
		file_details_border.bottom_border = UTF.line.double.horizontal
		file_details = Window(term, FILELIST_WIDTH, PATH_WINDOW_HEIGHT,
								height=FILE_DETAILS_HEIGHT, border=file_details_border)
		file_details.content = self.current_file_details()
		file_details.render()