# controller - provides WFcontroller to process info from user and model


from include.display import WFDisplay
from include.model import WFModel
from share.config import negativeAddress, positiveAddress


class WFController(object):
  def __init__(self):
    self.status = {"Pos": {"status": 0, "voltage": 0, "current": 0, "rate": 0},
                   "Neg": {"status": 0, "voltage": 0, "current": 0, "rate": 0}}
    self.posModel = WFModel(positiveAddress)
    self.negModel = WFModel(negativeAddress)
    self.display = WFDisplay(self)

  def __str__(self):
    return "WF: {}\n    {}".format(self.model, self.display)

  def run(self):
    _ = self.getCurrentStatus()
    self.display.display()

  def querySupplies(self):
    self.querySingleSupply(self.posModel, "Pos")
    self.querySingleSupply(self.negModel, "Neg")

  def querySingleSupply(self, supply, name):
    self.status[name] = {
      "status": supply.communicate(">KS?\n"),
      "voltage": supply.communicate(">M0?\n"),
      "current": supply.communicate(">M1?\n")
    }

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

  def getCurrentStatus(self):
    self.querySupplies()
    self.convertData()
    return self.status
