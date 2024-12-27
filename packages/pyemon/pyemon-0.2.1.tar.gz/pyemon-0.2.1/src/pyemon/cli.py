from .tasks.package.build import *
from .tasks.package.init import *
from .tasks.package.install import *
from .tasks.package.test import *
from .tasks.package.upload import *
from .tasks.task.run import *

Task.parse_if_main(__name__, Task.get("help"))
def main():
  pass
