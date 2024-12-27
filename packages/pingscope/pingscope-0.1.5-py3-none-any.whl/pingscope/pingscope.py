import ping3
import math
import json
import graspgraph as gg
from pyemon.time import *
from pyemon.path import *

class PingRank:
  def __init__(self, roundTripTime):
    if roundTripTime < 10:
      self.__Name = "S"
      self.__Color = gg.Color.from_hex_code("#0000FF") # blue
    elif roundTripTime < 15:
      self.__Name = "A"
      self.__Color = gg.Color.from_hex_code("#87CEEB") # skyblue
    elif roundTripTime < 20:
      self.__Name = "B"
      self.__Color = gg.Color.from_hex_code("#00FF00") # green
    elif roundTripTime < 30:
      self.__Name = "C"
      self.__Color = gg.Color.from_hex_code("#FFFF00") # yellow
    elif roundTripTime < 50:
      self.__Name = "D"
      self.__Color = gg.Color.from_hex_code("#FFA500") # orange
    else:
      self.__Name = "E"
      self.__Color = gg.Color.from_hex_code("#FF0000") # red

  @property
  def Name(self):
    return self.__Name

  @property
  def Color(self):
    return self.__Color

class Pingscope:
  def __init__(self, maxCount = 30):
    self.MaxCount = maxCount
    self.RoundTripTimes = []

  def run(self, dst, count = 5, onOutput = None):
    runStopwatch = Stopwatch()
    self.RoundTripTimes = []
    if onOutput is None:
      onOutput = lambda line: None
    onOutput("""#{}\n""".format(json.dumps({"Dst": dst, "Count": count})))
    roundTripTime = Pingscope.ping(dst)
    if roundTripTime < 1000:
      pingStopwatch = Stopwatch()
      for _ in range(count):
        pingStopwatch.start()
        roundTripTime = Pingscope.ping(dst)
        self.RoundTripTimes.append(roundTripTime)
        onOutput("""{}\n""".format(roundTripTime))
        if roundTripTime < 1000:
          pingStopwatch.stop()
          Time.cycle_sleep(pingStopwatch.ElapsedTime)
    else:
      self.RoundTripTimes.append(1000)
      onOutput("1000\n")
    simpleStats = gg.SimpleStats(self.RoundTripTimes)
    runStopwatch.stop()
    onOutput("""#{}\n""".format(json.dumps({"Avg": math.ceil(simpleStats.Avg), "Min": math.ceil(simpleStats.Min), "Max": math.ceil(simpleStats.Max), "ElapsedTime": runStopwatch.ElapsedTime})))
    return self

  def save(self, filePath, dst, count = 5):
    Path.from_file_path(filePath).makedirs()
    with open(filePath, mode = "w", newline = "\n") as file:
      self.run(dst, count, lambda line: file.write(line))
    return self

  def load(self, filePath):
    self.RoundTripTimes = []
    with open(filePath) as file:
      while True:
        line = file.readline()
        if not line:
          break
        if not line.startswith("#"):
          self.RoundTripTimes.append(int(line))
    return self

  def to_figure(self):
    simpleStats = gg.SimpleStats(self.RoundTripTimes)
    rank = PingRank(math.ceil(simpleStats.Avg))
    rgb = rank.Color.to_string("""rgb({R}, {G}, {B})""")
    rgba = rank.Color.to_string("""rgba({R}, {G}, {B}, 0.15)""")
    figure = gg.Statsgraph(
      gg.StatsgraphAxis(gg.Array.arange(1, len(self.RoundTripTimes)), self.MaxCount),
      gg.StatsgraphAxis(self.RoundTripTimes),
      gg.StatsgraphColors(layoutTitle = rgb, line = rgb, fill = rgba)).to_figure()
    figure.LayoutTitleText = """<b>[pingscope]<br>{}(Avg:{}ms Min:{}ms Max:{}ms)""".format(rank.Name, math.ceil(simpleStats.Avg), math.ceil(simpleStats.Min), math.ceil(simpleStats.Max))
    figure.XTitleText = "Elapsed time(sec)"
    figure.YTitleText = "Round trip time(ms)"
    return figure

  @classmethod
  def ping(cls, dst):
    roundTripTime = ping3.ping(dst, timeout = 1, unit = "ms")
    if not roundTripTime:
      roundTripTime = 1000
    else:
      roundTripTime = math.ceil(roundTripTime)
    return roundTripTime
