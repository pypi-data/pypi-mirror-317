from .list import *

class Option:
  def __init__(self, shortName = "", longName = "", defaultValue = None, caption = ""):
    self.__ShortName = shortName[0]
    self.__LongName = longName
    self.__DefaultValue = defaultValue
    self.__Caption = caption
    self.Value = defaultValue

  @property
  def ShortName(self):
    return self.__ShortName

  @property
  def LongName(self):
    return self.__LongName

  @property
  def DefaultValue(self):
    return self.__DefaultValue

  @property
  def Caption(self):
    return self.__Caption

  def value_by_bool(self, value_if_true, value_if_false):
    if self.Value is True:
      return value_if_true
    return value_if_false

  def value_if_not(self, value):
    if not self.Value:
      return value
    return self.Value

class OptionParser:
  def __init__(self, options = []):
    self.__Options = {}
    for option in options:
      self.add_option(option)
    self.Argv = []

  def add_option(self, option):
    self.__Options[option.LongName] = option

  def find_option_from_short_name(self, shortName):
    for option in self.__Options.values():
      if option.ShortName == shortName:
        return option
    return None

  def find_option_from_long_name(self, longName):
    if longName in self.__Options:
      return self.__Options[longName]
    return None

  def find_option(self, name):
    if len(name) == 1:
      return self.find_option_from_short_name(name)
    else:
      return self.find_option_from_long_name(name)

  def parse(self, argv):
    argc = len(argv)
    argi = 0
    newArgv = []
    parsedOptions = []
    while argi < argc:
      arg = List.get(argv, argi)
      if 2 <= len(arg):
        if arg[0] == "-":
          option = key = value = None
          if arg[1] == "-":
            splitedArg = arg[2:].split("=")
          else:
            splitedArg = arg[1:].split("=")
          key = splitedArg.pop(0)
          if 0 < len(splitedArg):
            value = "=".join(splitedArg)
          option = self.find_option(key)
          if option is None:
            newArgv.append(arg)
          else:
            parsedOptions.append(option)
            if option.DefaultValue is None:
              option.Value = True
            elif value is None:
              argi += 1
              option.Value = List.get(argv, argi, option.DefaultValue)
            else:
              option.Value = value
        else:
          newArgv.append(arg)
      else:
        newArgv.append(arg)
      argi += 1
    self.Argv = newArgv
    return self

  def to_string(self, indent = ""):
    strings = []
    withValueOptions = []
    noValueOptions = []
    longNameMaxLen = 0
    defaultValueMaxLen = 0
    for option in self.__Options.values():
      longNameMaxLen = max(len(option.LongName), longNameMaxLen)
      defaultValue = option.DefaultValue
      if defaultValue is None:
        defaultValue = ""
      defaultValueMaxLen = max(len(defaultValue), defaultValueMaxLen)
      if option.DefaultValue is None:
        noValueOptions.append(option)
      else:
        withValueOptions.append(option)
    format = """{}  -{{}}|--{{:<{}}} {{:<{}}} # {{}}""".format(indent, longNameMaxLen, defaultValueMaxLen)
    if 0 < len(withValueOptions):
      strings.append("""{}[With value]""".format(indent))
      for option in withValueOptions:
        strings.append(format.format(option.ShortName, option.LongName, option.DefaultValue, option.Caption))
    if 0 < len(noValueOptions):
      if 0 < len(withValueOptions):
        strings.append("")
      strings.append("""{}[No value]""".format(indent))
      for option in noValueOptions:
        strings.append(format.format(option.ShortName, option.LongName, "", option.Caption))
    return "\n".join(strings)

  def __str__(self):
    return self.to_string()
