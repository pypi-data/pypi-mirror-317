from ...task import *
import shutil
import glob

class PackageBuildTask(Task):
  def run(self, argv):
    for pattern in ["dist", "**/*.egg-info"]:
      for path in glob.glob(pattern, recursive = True):
        shutil.rmtree(path)
    Command(["pipenv", "run", "python", "-m", "build"] + argv).run()
Task.parse_if_main(__name__, PackageBuildTask("<build args>"))
