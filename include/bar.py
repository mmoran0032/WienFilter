

from math import modf

# bars = [" ", " ", " ", "|", "|", "|", "|", "█", "█"]
# bars = [" ", " ", " ", " ", "|", "|", "|", "|", "|"]
bars = [" ", " ", " ", " ", "█", "█", "█", "█", "█"]


class Bar(object):
  def __init__(self, size, percent=0, preChar="[", postChar="]", emptyChar=" ",
               withText=True):
    self.size = size
    self.percent = percent
    self.preChar = preChar
    self.postChar = postChar
    self.emptyChar = emptyChar
    self.withText = withText

  def __str__(self):
    frac, whole = modf(self.getSize() * self.getPercent() / 100.0)
    output = bars[8] * int(whole)
    if frac > 0:
      output += bars[int(frac * 8)]
      whole += 1
    output = "{}{}".format(output, self.emptyChar*int(self.getSize() - whole))
    if self.withText:
      output = "{0}{1:>6.2f}%".format(output, self.percent)
    return output

  def getSize(self, decorated=False):
    if decorated:
      return self.size
    if self.withText:
      return self.size - 6

  def getPercent(self):
    return self.percent

  def setPercent(self, value):
    if 0 <= value <= 100:
      self.percent = value
