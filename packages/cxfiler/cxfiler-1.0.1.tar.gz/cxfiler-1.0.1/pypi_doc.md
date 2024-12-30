#  F.I.L.E.R.

###  (File Investigation with Less Effort and Remembering)

----------------------------------------


 FILER is an intuitive file explorer with modern input and ease-of-use.

##  Installation


 As FILER is a Python application, it is installed via ```pip```.

```
pip3 install cxfiler

```



 To fully get the most use out of FILER, you should also add the following to your shell profile ( ```.bashrc```, ```.bash_profile```, ```.zshrc```, etc.):

```
filer() {
	cxfiler
	cd $(cat $HOME/.cxfilerexit)
}

```



 This will create a shell function which will run FILER and then change directory to the directory FILER was pointed to when you quit.

#  Usage

----------------------------------------

##  Navigating the Filesystem

| Key | Description |
|---|---|
| &uarr; | Move the cursor up 1 entry |
| " | Move the cursor up 1 screenful |
| &darr; | Move the cursor down 1 entry |
| ? | Move the cursor down 1 screenful |
| &larr; | Move up to the parent directory of the current directory |
| &rarr; | Move into teh directory (if cursor is on a directory) |
| Enter | Open action menu / Select action menu item |
| B or ESC | Back out of a menu |
| Space | Select / Deselect item |
| A | Select / Deselect all |
| . | Show / hide hidden files |
| D | Show / hide directories |
| F | Show / hide non-directory files |
| H | Display help |
| Q | Quit |


##  Rename a File


 To rename a file, move the cursor onto a file and press ```Enter```. This will open the action menu. Move the cursor to "Rename" and press ```Enter```. Type the new name for the file and press ```Enter```. You can use the ```B```key or the ```ESC```key to back out of the rename operation.

##  Copy / Move Files


 To copy or move files, you must first select 1 or more files. To do this, move the cursor to a file, then press ```Space```to select it. You can press ```Space```on a previously selected file to deselect it. Once you have all the files selected that you want to copy or move, navigate to the directory you want to copy or move the files to. Press ```Enter```and then select "Copy to here" or "Move to here" and press ```Enter```again.

##  Delete Files


 To delete a single file, move the cursor onto the file you want to delete. Then, press ```Enter```to open the action menu. To delete multiple files, use the ```Space```key to select the files, then press ```Enter```to open the action menu. Once the action menu is open, select "Delete", and press ```Enter```again. You will be asked to confirm the delete by pressing ```Y```or cancel the delete by pressing ```N```. You can use the ```B```key or the ```ESC```key to back out of the delete operation.

