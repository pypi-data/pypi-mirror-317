from .string import *

class Status:
  def __init__(self, name, status = "skip"):
    self.Name = name
    self.Status = status

  def skip(self):
    self.Status = "skip"

  def done(self):
    self.Status = "done"

  def to_string(self):
    return """{} is {}.""".format(String.console_string(self.Name, "cyan"), self.Status)

  def __str__(self):
    return self.to_string()
