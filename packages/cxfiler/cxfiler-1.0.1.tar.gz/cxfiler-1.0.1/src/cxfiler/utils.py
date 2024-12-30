import os, pwd, grp
from datetime import datetime

from .strings import gettext as _

# FILER window sizes
PATH_WINDOW_HEIGHT = 1
FILELIST_WIDTH = 40
FILE_DETAILS_HEIGHT = 10
SCREEN_JUMP = 20

#-==@class
class FileType:
	#-== Enum class that defines file types.
	# @attributes
	# DIR: directory
	# FILE: non-directory file
	# LINK: symbolic or hard link
	# OTHER: other/unknown

	DIR = 'directory'
	FILE = 'file'
	LINK = 'link'
	OTHER = 'other'


ORDERS_OF_MAGNITUDE = [
	' byte', ' kB', ' MB', ' GB', ' TB',
	' PB', ' EB', ' ZB', ' YB', ' RB', ' QB'
]

FILETYPE_SYMBOL = {
	FileType.DIR: '/',
	FileType.FILE: ' ',
	FileType.LINK: '@',
	FileType.OTHER: '*'
}

PERMS = {
	'0': '---',
	'1': '--x',
	'2': '-w-',
	'3': '-wx',
	'4': 'r--',
	'5': 'r-x',
	'6': 'rw-',
	'7': 'rwx',
}


#-==@class
class ScanDirHelper:
	#-== Helper class which takes in a file and extracts information
	# into a simple and useful data structure.
	# @attributes
	# filename: the name of the file along with its file extension
	# inode: the inode reference for the file
	# path: the absolute path of the file
	# perms: a string indicating the permissions set on the file
	# owner: the owner of the file
	# group: the permission group of the file
	# filetype: one of the types listed in the /FileType enum class
	# size_bytes: the size of the file in bytes
	# size: a string indicating the file size in a human readable format
	# created: the date the file was created
	# modified: the date the file was most recently modified

	#-==@method
	def __init__(self, direntry):
		#-== Takes a file object and extracts all the relevant information about it.
		# @params
		# direntry: the file object to read

		stat = direntry.stat(follow_symlinks=False)
		self.filename = direntry.name
		self.inode = direntry.inode()
		self.path = os.path.abspath(direntry.path)
		self.perms = self.receive_perms(stat.st_mode)
		self.owner = pwd.getpwuid(stat.st_uid)[0]
		self.group = grp.getgrgid(stat.st_gid)[0]
		self.filetype = self.check_file_type(direntry)
		self.size_bytes = stat.st_size
		self.size = self.human_readable_size(stat.st_size)
		self.created = datetime.fromtimestamp(stat.st_ctime)
		try:
			self.created = datetime.fromtimestamp(stat.st_birthtime)
		except:
			pass
		self.modified = datetime.fromtimestamp(stat.st_mtime)

	#-==@method
	def is_hidden_file(self):
		#-== Indicates if the file is a hidden file.
		# @returns
		# /True if the filename starts with a period ( /. ),
		# /False otherwise.

		return self.filename[0] == '.'

	#-==@method
	def receive_perms(self, st_mode):
		#-== Transforms the permissions octet into
		# a more readable string in the format /rwxrwxrwx

		perms_oct_str = ''
		if st_mode is not None:
			perms_oct_str = '{:o}'.format(st_mode&0o07777)
		return self._translate_perms(perms_oct_str)


	def _translate_perms(self, perms_oct_str):
		# Private method that translates the permissins octet
		# into a more readable string in the format rwxrwxrwx
		owner = '   '
		group = '   '
		other = '   '
		if len(perms_oct_str) >= 3:
			owner = PERMS[perms_oct_str[0]]
			group = PERMS[perms_oct_str[1]]
			other = PERMS[perms_oct_str[2]]
		return owner+group+other

	#-==@method
	def check_file_type(self, direntry):
		#-== @returns
		# One of the file types in the /FileType enum class.

		if direntry.is_symlink():
			return FileType.LINK
		if direntry.is_dir(follow_symlinks=False):
			return FileType.DIR
		if direntry.is_file(follow_symlinks=False):
			return FileType.FILE
		return FileType.OTHER

	#-==@method
	def human_readable_size(self, size_bytes, magnitude=0):
		#-== @returns
		# A string of the file size in a human readable format.

		#mag = float(pow(1024, magnitude+1))
		if size_bytes > 1024:
			size = self.human_readable_size(size_bytes/1024, magnitude+1)
		else:
			if magnitude == 0:
				size = str(size_bytes) + ORDERS_OF_MAGNITUDE[magnitude]
				if size_bytes != 1:
					size += 's'
			else:
				size = '{:.1f}'.format(size_bytes) + ORDERS_OF_MAGNITUDE[magnitude]
		return size


	def __str__(self):
		outstr = '\n------------------------------------'
		outstr+= '\nFilename:    '+str(self.filename)
		outstr+= '\niNode:       '+str(self.inode)
		outstr+= '\nPath:        '+str(self.path)
		outstr+= '\nPermissions: '+str(self.perms)
		outstr+= '\nOwner:       '+str(self.owner)
		outstr+= '\nGroup:       '+str(self.group)
		outstr+= '\nSize:        '+str(self.size)
		outstr+= '\nCreated:     '+str(self.created)
		outstr+= '\nModified:    '+str(self.modified)
		return _('scandirhelper.str.repr').format(**vars(self))