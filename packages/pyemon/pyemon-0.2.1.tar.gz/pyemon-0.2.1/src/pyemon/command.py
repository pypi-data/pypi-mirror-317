import subprocess
import datetime
import os
import sys
import shutil
import glob
import yaml
from .string import *

class Command:
  def __init__(self, args, **kwargs):
    self.Args = args
    self.Kwargs = kwargs

  def run(self, onProcess = None):
    if onProcess is None:
      onProcess = lambda result: String.console_string("""Fail: Return code is {}.""".format(result.returncode), "red")
    print(String.console_string("""[{}] {} $ {}""".format(datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S"), os.getcwd(), self.to_string()), "green"))
    result = subprocess.run(self.Args, **self.Kwargs)
    if result.returncode != 0:
      exitArg = onProcess(result)
      if exitArg is not None:
        sys.exit(exitArg)
    return result

  def capture(self):
    self.Kwargs = dict(capture_output = True, text = True, encoding = "utf-8") | self.Kwargs
    return self

  def to_string(self):
    if type(self.Args) is str:
      return self.Args
    return " ".join(self.Args)

  def __str__(self):
    return self.to_string()

  @classmethod
  def exists(cls, path):
    return os.path.exists(path)

  @classmethod
  def exists_assert(cls, path):
    if Command.exists(path) is False:
      sys.exit(String.does_not_exist_string(path))

  @classmethod
  def copy(cls, src, dst):
    if os.path.isfile(src):
      shutil.copy2(src, dst)
    else:
      shutil.copytree(src, dst)

  @classmethod
  def copy_if_not_exists(cls, src, dst):
    if not os.path.exists(os.path.join(dst, os.path.basename(src))):
      Command.copy(src, dst)
      return True
    return False

  @classmethod
  def rm(cls, path):
    if os.path.isfile(path):
      os.remove(path)
    elif os.path.isdir(path):
      shutil.rmtree(path)

  @classmethod
  def move(cls, src, dst):
    Command.rm(os.path.join(dst, os.path.basename(src)))
    shutil.move(src, dst)

  @classmethod
  def mkdir(cls, path):
    if 0 < len(path):
      os.makedirs(path, exist_ok = True)

  @classmethod
  def rmkdir(cls, path):
    Command.rm(path)
    Command.mkdir(path)

  @classmethod
  def chdir(cls, path):
    os.chdir(path)

  @classmethod
  def getdir(cls):
    return os.getcwd()

  @classmethod
  def find(cls, pattern, recursive = True):
    paths = []
    for path in glob.glob(pattern, recursive = recursive):
      paths.append(path)
    return paths

  @classmethod
  def yaml_load(cls, filePath):
    with open(filePath, "r", encoding = "utf-8") as file:
      return yaml.safe_load(file)
    return {}

  @classmethod
  def yaml_save(cls, filePath, data):
    Command.mkdir(os.path.dirname(filePath))
    with open(filePath, "w", encoding = "utf-8", newline = "\n") as file:
      yaml.dump(data, file, sort_keys = False, default_flow_style = False, allow_unicode = True)

  @classmethod
  def file_read(cls, filePath):
    with open(filePath, "r", encoding = "utf-8") as file:
      return file.read()
    return ""

  @classmethod
  def file_write(cls, filePath, data):
    Command.mkdir(os.path.dirname(filePath))
    with open(filePath, "w", encoding = "utf-8", newline = "\n") as file:
      file.write(data)
