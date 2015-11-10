# controller - provides WFcontroller to process info from user and model


from time import sleep

from include.display import WFdisplay
from include.model import WFmodel


class WFcontroller(object):
  def __init__(self):
    self.model = WFmodel()
    self.display = WFdisplay()
    self.refreshTime = 0.5
    self.data = {}

  def __str__(self):
    return "WF: {}\n    {}".format(self.model, self.display)

  def run(self):
    while True:
      self.querySupplies()
      self.convertData()
      self.display.receiveData(self.data)
      self.display.display()
      sleep(self.refreshTime)

  def querySupplies(self):
    self.negativeOutput = self.model.communicate(0, ">DON?\n")
    self.positiveOutput = self.model.communicate(1, ">DON?\n")
    self.negativeV = self.model.communicate(0, ">M0?\n")
    self.negativeA = self.model.communicate(0, ">M1?\n")
    self.positiveV = self.model.communicate(1, ">M0?\n")
    self.positiveA = self.model.communicate(1, ">M1?\n")

  def convertData(self):
    self.data["Neg"]["status"] = self.convertIndicator(self.negativeOutput)
    self.data["Pos"]["status"] = self.convertIndicator(self.positiveOutput)
    self.data["Neg"]["voltage"] = self.convertNumber(self.negativeV, -3)
    self.data["Neg"]["current"] = self.convertNumber(self.negativeA, 6)
    self.data["Pos"]["voltage"] = self.convertNumber(self.positiveV, -3)
    self.data["Pos"]["current"] = self.convertNumber(self.positiveA, 6)

  def convertIndicator(self, indicator):
    ind = indicator.split(":")[1]
    if len(ind) == 1:
      ind = int(ind)
    return ind

  def convertNumber(self, number, power=1):
    num = float(number.split(":")[1])
    num *= 10**power
    return num
