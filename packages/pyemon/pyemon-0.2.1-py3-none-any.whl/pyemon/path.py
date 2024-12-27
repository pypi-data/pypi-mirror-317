import os
from .directory import *

class Path:
  def __init__(self, directory = "", file = "", ext = ""):
    self.Directory = directory
    self.File = file
    self.Ext = ext

  def exists(self):
    return os.path.exists(self.to_string())

  def makedirs(self):
    if 0 < len(self.Directory):
      os.makedirs(self.Directory, exist_ok = True)

  def to_module_name(self):
    names = list(filter(lambda name: name != ".", Directory.split(self.Directory)))
    if 0 < len(self.File):
      names.append(self.File)
    return ".".join(names)

  def to_string(self):
    return Path.join(self.File, self.Ext, self.Directory)

  def __str__(self):
    return self.to_string()

  @classmethod
  def split(cls, path):
    directory, fileAndExt = os.path.split(path)
    file, ext = os.path.splitext(fileAndExt)
    if 0 < len(ext):
      ext = ext[1:]
    return directory, file, ext

  @classmethod
  def join(cls, file, ext, directory = ""):
    if len(ext) == 0:
      path = file
    else:
      path = """{}.{}""".format(file, ext)
    if 0 < len(directory):
      path = """{}/{}""".format(directory, path)
    return path

  @classmethod
  def from_file_path(self, filePath):
    return Path(*Path.split(filePath))
