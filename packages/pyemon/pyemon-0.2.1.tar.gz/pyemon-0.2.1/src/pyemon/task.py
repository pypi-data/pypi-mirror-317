from .option import *
from .command import *
from .status import *
import sys
import inflection
import copy

class Task:
  __Tasks = {}

  def __init__(self, caption = ""):
    name = inflection.underscore(self.__class__.__name__)
    if name.endswith("_task"):
      name = name[:-5]
    self.__Name = name.replace("_", ".")
    self.Caption = caption
    self.OptionParser = OptionParser()

  @property
  def Name(self):
    return self.__Name

  def run(self, argv):
    pass

  def copy(self, srcDir, dstDir, fileName):
    Command.copy(os.path.join(srcDir, fileName), dstDir)
    print(Status(os.path.relpath(os.path.join(dstDir, fileName)), "done"))

  def copy_if_not_exists(self, srcDir, dstDir, fileName):
    status = Status(os.path.relpath(os.path.join(dstDir, fileName)))
    if Command.copy_if_not_exists(os.path.join(srcDir, fileName), dstDir):
      status.done()
    print(status)

  def to_string(self, indent = ""):
    strings = []
    if len(self.Caption) == 0:
      strings.append("""{}{}""".format(indent, self.__Name))
    else:
      strings.append("""{}{} # {}""".format(indent, self.__Name, self.Caption))
    string = self.OptionParser.to_string("""{}  """.format(indent))
    if 0 < len(string):
      strings.append(string)
    return "\n".join(strings)

  def __str__(self):
    return self.to_string()

  @classmethod
  def set(cls, task):
    Task.__Tasks[task.Name] = task
    return task

  @classmethod
  def unset(cls, name):
    if name in Task.__Tasks:
      return Task.__Tasks.pop(name)
    return None

  @classmethod
  def get(cls, name):
    if name in Task.__Tasks:
      return Task.__Tasks[name]
    else:
      return None

  @classmethod
  def tasks(cls):
    return tuple(Task.__Tasks.values())

  @classmethod
  def parse(cls, argv):
    if 0 < len(argv):
      newArgv = copy.deepcopy(argv)
      name = List.shift(newArgv)
      if name in Task.__Tasks:
        task = Task.unset(name)
        task.run(newArgv)
        Task.set(task)
      else:
        sys.exit(String.undefined_string(name))

  @classmethod
  def parse_if_main(cls, name, task = None):
    if task is not None:
      Task.set(task)
    if name == "__main__" or name.split(".")[-1] == "cli":
      argv = copy.deepcopy(sys.argv[1:])
      if task is not None:
        argv.insert(0, task.Name)
      Task.parse(argv)

class HelpTask(Task):
  def run(self, argv):
    if len(argv) == 0:
      strings = ["<Tasks>"]
      for task in [self] + list(Task.tasks()):
        strings.append(task.to_string("  "))
        strings.append("")
      sys.exit("\n".join(strings))
    if argv[0] == "help":
      argv.pop(0)
      strings = []
      if len(argv) == 0:
        strings.append("""{}""".format(" ".join(list(map(lambda task: task.Name, Task.tasks())))))
      else:
        strings.append("<Tasks>")
        for name in argv:
          task = Task.get(name)
          if task is None:
            strings.append("""  {}""".format(String.undefined_string(name)))
          else:
            strings.append(task.to_string("  "))
          strings.append("")
      sys.exit("\n".join(strings))
    else:
      Task.parse(argv)
Task.set(HelpTask("<task names>"))
