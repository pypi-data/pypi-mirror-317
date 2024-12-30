from .multiline_strings import *

STRINGS = {
	'scandirhelper.str.repr': SCANDIRHELPER_REPR,
	'errors.general.permissions': 'Invalid permissions',
	'errors.user.display': 'Error: {}, press any key',
	'error.write.denied': 'Cannot write to this directory',
	'error.copy.denied': 'No permission to copy {}',
	'error.move.denied': 'No permission to move {}',
	'main.help.text': HELP_TEXT,
	'filetype.item.single': 'item',
	'filetype.item.multi': 'items',
	'filetype.file.single': 'file',
	'filetype.file.multi': 'files',
	'filetype.dir.single': 'dir',
	'filetype.dir.multi': 'dirs',
	'filelist.details': 'showing {} of {} {}\n',
	'filelist.file.details': FILELIST_FILE_DETAILS,
	'actions.menu.title.single': '{} file selected',
	'actions.menu.title.multi': '{} files selected',
	'actions.labels.copy.here': 'Copy to Here',
	'actions.labels.move.here': 'Move to Here',
	'actions.labels.rename': 'Rename',
	'actions.labels.permissions': 'Change Permissions',
	'actions.labels.delete': 'Delete',
	'actions.empty.menu.message': 'No actions available.',
	'actions.empty.menu.key.prompt': 'Press any key to continue..',
	'actions.delete.window.title': '!! DELETE !!',
	'actions.delete.confirm.message': 'Are you sure?',
	'actions.delete.key.prompt': '[Y]es   [N]o',
	'rename.prompt': '\n Rename to:\n  {}{}',
}

def gettext(key):
	if key in STRINGS.keys():
		return STRINGS[key]
	return key