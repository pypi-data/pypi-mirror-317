import os
import wx
class filemgr:
	@staticmethod
	def get_contents(fn, mode="r"):
		try:
			with open(fn, mode) as d:
				return d.read()
		except:
			return ""

	@staticmethod
	def put_contents(fn, content, mode="w", overwrite=True):
		if not overwrite and os.path.exists(fn):
			return False
		try:
			with open(fn, mode) as f:
				f.write(content)
				return True
		except:
			return False

	@staticmethod
	def exists(path):
		return os.path.isfile(path)

	@staticmethod
	def delete(p):
		if os.path.exists(p):
			os.remove(p)
			return True
		else:
			return False

	@staticmethod
	def get_size(fn):
		return os.path.getsize(fn)

	@staticmethod
	def search(dest):
		files_list = []
		try:
			for f in os.listdir(dest):
				if os.path.isfile(f):
					files_list.append(f)
			return files_list
		except:
			return []

class dirmgr:
	@staticmethod
	def create(path):
		try:
			os.mkdir(path)
			return True
		except:
			return False

	@staticmethod
	def delete(path):
		try:
			os.rmdir(path)
			return True
		except:
			return False

	@staticmethod
	def exists(path):
		return os.path.isdir(path)

	@staticmethod
	def search(dest):
		dirs_list = []
		try:
			for f in os.listdir(dest):
				if os.path.isdir(f):
					dirs_list.append(f)
			return dirs_list
		except:
			return []
#other
def select_file(title="Choose File", wildcard="All files (*.*)|*.*", multi=False):
	app = wx.App(False)  # Create wx.App object
	style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
	if multi:
		style |= wx.FD_MULTIPLE
	dialog = wx.FileDialog(None, title, wildcard=wildcard, style=style)
	paths = []

	if dialog.ShowModal() == wx.ID_OK:
		if multi:
			paths = dialog.GetPaths()
		else:
			paths = [dialog.GetPath()]
	dialog.Destroy()
	app.ExitMainLoop()  # Destroy wx.App object
	return paths

def select_folder(title="Choose Folder"):
	app = wx.App(False)  # Create wx.App object
	dialog = wx.DirDialog(None, title)
	path = ""

	if dialog.ShowModal() == wx.ID_OK:
		path = dialog.GetPath()
	dialog.Destroy()
	app.ExitMainLoop()  # Destroy wx.App object
	return path
