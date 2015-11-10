# controller - provides WFcontroller to process info from user and model


from time import sleep

from include.display import WFdisplay
from include.model import WFmodel


class WFcontroller(object):
  def __init__(self):
    self.refreshTime = 0.5
    self.status = {"Pos": {"status": 0, "voltage": 0, "current": 0, "rate": 0},
                   "Neg": {"status": 0, "voltage": 0, "current": 0, "rate": 0}}
    self.model = WFmodel()
    self.display = WFdisplay(self.status)

  def __str__(self):
    return "WF: {}\n    {}".format(self.model, self.display)

  def run(self):
    while True:
      self.querySupplies()
      self.convertData()
      self.display.receiveData(self.status)
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
    self.status["Neg"]["status"] = self.convertIndicator(self.negativeOutput)
    self.status["Pos"]["status"] = self.convertIndicator(self.positiveOutput)
    self.status["Neg"]["voltage"] = self.convertNumber(self.negativeV, -3)
    self.status["Neg"]["current"] = self.convertNumber(self.negativeA, 6)
    self.status["Pos"]["voltage"] = self.convertNumber(self.positiveV, -3)
    self.status["Pos"]["current"] = self.convertNumber(self.positiveA, 6)

  def convertIndicator(self, indicator):
    ind = indicator.split(":")[1]
    if len(ind) == 1:
      ind = int(ind)
    return ind

  def convertNumber(self, number, power=1):
    num = float(number.split(":")[1])
    num *= 10**power
    return num
