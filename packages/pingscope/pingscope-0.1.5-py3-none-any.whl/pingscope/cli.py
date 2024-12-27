from pyemon.list import *
from pyemon.task import *
from pyemon.status import *
from .pingscope import *

class PingTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([
      Option("c", "count", "5", "Count"),
      Option("m", "max-count", "30", "Max count"),
    ])

  def run(self, argv):
    self.OptionParser.parse(argv)
    pingFileName = List.shift(self.OptionParser.Argv)
    dst = List.shift(self.OptionParser.Argv)
    if pingFileName is not None and dst is not None:
      count = int(self.OptionParser.find_option_from_long_name("count").Value)
      maxCount = int(self.OptionParser.find_option_from_long_name("max-count").Value)
      pingscope = Pingscope(maxCount)
      pingFilePath = """{}.ping""".format(pingFileName)
      pingscope.save(pingFilePath, dst, count)
      print(Status(pingFilePath, "done"))
      pngFilePath = """{}.png""".format(pingFileName)
      pingscope.to_figure().Write(pngFilePath)
      print(Status(pngFilePath, "done"))
Task.set(PingTask("<ping file name> <dst>"))

Task.parse_if_main(__name__, Task.get("help"))
def main():
  pass
