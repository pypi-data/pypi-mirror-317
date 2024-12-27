import os

class Directory:
  @classmethod
  def split(cls, path):
    names = []
    splitedPath = [path]
    while 0 < len(splitedPath[0]):
      splitedPath = os.path.split(splitedPath[0])
      names.append(splitedPath[-1])
    names.reverse()
    return names
