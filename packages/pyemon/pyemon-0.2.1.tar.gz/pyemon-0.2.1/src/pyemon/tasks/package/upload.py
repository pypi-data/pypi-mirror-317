from ...task import *

class PackageUploadTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([Option("p", "pypi", None, "PYPI")])

  def run(self, argv):
    self.OptionParser.parse(argv)
    repository = self.OptionParser.find_option_from_long_name("pypi").value_by_bool("pypi", "testpypi")
    Command(["pipenv", "run", "python", "-m", "twine", "upload", "--repository", repository, "dist/*"]).run()
Task.parse_if_main(__name__, PackageUploadTask("<twine upload args>"))
