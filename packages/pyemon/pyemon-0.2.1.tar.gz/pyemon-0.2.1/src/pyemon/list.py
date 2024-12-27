class List:
  @classmethod
  def get(cls, list, index, defaultValue = None):
    if index < len(list):
      return list[index]
    return defaultValue

  @classmethod
  def shift(cls, list, defaultValue = None):
    if 0 < len(list):
      return list.pop(0)
    return defaultValue
