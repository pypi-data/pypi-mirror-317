class String:
  @classmethod
  def color_to_escape(cls, color):
    match color:
      case "black":
        return 0
      case "red":
        return 1
      case "green":
        return 2
      case "yellow":
        return 3
      case "blue":
        return 4
      case "magenta":
        return 5
      case "cyan":
        return 6
      case "gray":
        return 7
      case _:
        return 9

  @classmethod
  def console_string(cls, value, fgColor, bgColor = "black"):
    return """\033[{}m\033[{}m{}\033[0m""".format(String.color_to_escape(bgColor) + 40, String.color_to_escape(fgColor) + 30, value)

  @classmethod
  def undefined_string(cls, value):
    return """{} is undefined.""".format(String.console_string(value, "red"))

  @classmethod
  def does_not_exist_string(cls, value):
    return """{} does not exist.""".format(String.console_string(value, "red"))
