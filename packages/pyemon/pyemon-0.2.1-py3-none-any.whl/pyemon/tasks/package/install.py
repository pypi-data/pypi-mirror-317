from ...task import *

class PackageInstallTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([
      Option("p", "pip", None, "PIP"),
      Option("d", "dev", None, "Development"),
      Option("t", "test", None, "TestPYPI"),
    ])

  def run(self, argv):
    self.OptionParser.parse(argv)
    args = [
      self.OptionParser.find_option_from_long_name("pip").value_by_bool("pip", "pipenv"),
      "install"
    ]
    if self.OptionParser.find_option_from_long_name("dev").Value:
      args.append("--dev")
    if self.OptionParser.find_option_from_long_name("test").Value:
      args.append("-i https://test.pypi.org/simple/")
    Command(args + self.OptionParser.Argv).run()
Task.parse_if_main(__name__, PackageInstallTask("<pip(pipenv) install args>"))
