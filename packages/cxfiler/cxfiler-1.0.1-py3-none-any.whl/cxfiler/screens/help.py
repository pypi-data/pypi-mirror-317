from bwk import Window
from bwk.screen import Screen

from ..strings import gettext as _

#-==@class
class HelpText(Screen):
	#-== When the /H key is pressed,
	# this screen activates to display the help text.
	#
	#-== *Available command keys:*
	# @table
	# Key(s)              |
	# ----------------------------------------------------------
	# Any key             | Close the help text window

	def process_input(self, key):
		self.back_to_main()

	def back_to_main(self):
		self.man.curr_screen = self.man.screens.main

	def render(self):
		helpwin = Window(self.man.term, 0, 0, border='*'*8)
		helpwin.content = _('main.help.text')
		helpwin.render()