from pyemon.task import *
from pyemon.path import *
from pyemon.option import *
from pyemon.status import *
from .template import *
import glob

class RenderTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([Option("o", "output", "", "Output file path")])

  def run(self, argv):
    self.OptionParser.parse(argv)
    templates = {}
    for path in glob.glob("**/*.tngn", recursive = True):
      templates[Path.from_file_path(path).to_module_name()] = path
    if len(self.OptionParser.Argv) == 0:
      strings = ["<Templates>"]
      for name in templates.keys():
        strings.append("""  {}""".format(name))
        strings.append("```")
        strings.append(Template.read(templates[name]))
        strings.append("```")
        strings.append("")
      sys.exit("\n".join(strings))
    else:
      format = ""
      name = List.shift(self.OptionParser.Argv)
      if name in templates:
        format = Template.read(templates[name])
      outputFilePath = self.OptionParser.find_option_from_long_name("output").Value
      if len(outputFilePath) == 0:
        print(Template.render(format, self.OptionParser.Argv), end = "")
      else:
        Template.write(outputFilePath, format, self.OptionParser.Argv)
        print(Status(outputFilePath, "done"))
Task.set(RenderTask("<template name> <args>"))

Task.parse_if_main(__name__, Task.get("help"))
def main():
  pass
