from pyemon.list import *
from pyemon.path import *

class Template:
  @classmethod
  def render(cls, format, args):
    if len(args) == 0:
      return format
    return format.format(*args)

  @classmethod
  def read(cls, filePath):
    with open(filePath, "r", encoding = "utf-8") as file:
      return file.read()
    return ""

  @classmethod
  def write(cls, filePath, format, args):
    Path.from_file_path(filePath).makedirs()
    with open(filePath, "w", encoding = "utf-8", newline = "\n") as file:
      file.write(Template.render(format, args))
