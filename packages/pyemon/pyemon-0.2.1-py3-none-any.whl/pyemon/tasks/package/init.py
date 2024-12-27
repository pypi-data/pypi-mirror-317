from ...task import *
from ...status import *
from ...path import *

class PackageInitTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([
      Option("u", "user-name", "", "User name"),
      Option("e", "email", "", "Email"),
      Option("description", "description", "", "Description"),
      Option("p", "project-name", "", "Project name")
    ])

  def run(self, argv):
    self.OptionParser.parse(argv)
    userName = self.OptionParser.find_option_from_long_name("user-name").Value
    email = self.OptionParser.find_option_from_long_name("email").Value
    description = self.OptionParser.find_option_from_long_name("description").Value
    projectName = self.OptionParser.find_option_from_long_name("project-name").value_if_not(os.path.basename(os.getcwd()))
    srcRootDir = os.path.abspath("""{}/../../scripts""".format(os.path.dirname(__file__)))

    for baseName in [".gitignore", "MANIFEST.in", "setup.py"]:
      self.copy_if_not_exists(srcRootDir, ".", baseName)

    if len(projectName) == 0 or len(email) == 0 or len(description) == 0:
      return

    baseName = "README.md"
    dst = baseName
    status = Status(os.path.relpath(dst))
    if not Command.exists(dst):
      Command.file_write(dst, Command.file_read(os.path.join(srcRootDir, baseName)).format(projectName = projectName, description = description))
      status.done()
    print(status)

    baseName = "pyproject.toml"
    dst = baseName
    status = Status(dst)
    if not Command.exists(dst):
      Command.file_write(dst, Command.file_read(os.path.join(srcRootDir, baseName)).format(userName = userName, email = email, description = description, projectName = projectName))
      status.done()
    print(status)

    Command.mkdir(os.path.join("src", projectName))
    dirName = "tests"
    Command.mkdir(dirName)
    baseName = "test.py"
    path = Path.from_file_path(os.path.join(dirName, baseName))
    path.File = """{}_{}""".format(path.File, projectName)
    dst = path.to_string()
    status = Status(dst)
    if not Command.exists(dst):
      Command.file_write(dst, Command.file_read(os.path.join(srcRootDir, dirName, baseName)).format(projectName = projectName))
      status.done()
    print(status)

    if not os.path.isfile("Pipfile"):
      Command(["pipenv", "--python", str(sys.version_info[0])]).run()
      Command(["pipenv", "install", "--dev", "pytest"]).run()

    Command(["pipenv", "install", "--dev", "build"]).run()
    Command(["pipenv", "install", "--dev", "twine"]).run()
Task.parse_if_main(__name__, PackageInitTask())
