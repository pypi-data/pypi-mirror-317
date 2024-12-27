from ...task import *

class PackageTestTask(Task):
  def run(self, argv):
    Command(["pipenv", "run", "pytest", "-s"] + argv).run()
Task.parse_if_main(__name__, PackageTestTask("<pytest args>"))
