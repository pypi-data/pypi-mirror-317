from ...task import *
from ...path import *
import glob
import importlib

class TaskRunTask(Task):
  def run(self, argv):
    builtinTaskNames = list(map(lambda task: task.Name, Task.tasks()))
    sys.path.append(os.getcwd())
    tasks = {}
    for path in glob.glob("**/pyetask.py", recursive = True):
      for task in importlib.import_module(Path.from_file_path(path).to_module_name()).Task.tasks():
        if task.Name not in builtinTaskNames:
          tasks[task.Name] = task
    if len(argv) == 0:
      strings = ["<Tasks>"]
      for task in tasks.values():
        strings.append(task.to_string("  "))
        strings.append("")
      sys.exit("\n".join(strings))
    if "help" in tasks:
      tasks.pop("help")
    if argv[0] == "help":
      argv.pop(0)
      strings = []
      if len(argv) == 0:
        strings.append("""{}""".format(" ".join(list(map(lambda task: task.Name, tasks.values())))))
      else:
        strings.append("<Tasks>")
        for name in argv:
          if name in tasks:
            strings.append(tasks[name].to_string("  "))
          else:
            strings.append("""  {}""".format(String.undefined_string(name)))
          strings.append("")
      sys.exit("\n".join(strings))
    else:
      name = List.shift(argv)
      if name in tasks:
        tasks[name].run(argv)
      else:
        sys.exit(String.undefined_string(name))
Task.parse_if_main(__name__, TaskRunTask("<task name> <task args>"))
