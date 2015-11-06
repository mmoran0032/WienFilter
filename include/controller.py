# controller - provides WFcontroller to process info from user and model


from time import sleep

import include
from include.display import WFdisplay
from include.model import WFmodel

import share
from share.commands import commands


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
    self.negativeOutput = self.model.communicate(0, ">DON?")
    self.positiveOutput = self.model.communicate(1, ">DON?")
    self.negativeV = self.model.communicate(0, ">M0?")
    self.negativeA = self.model.communicate(0, ">M1?")
    self.positiveV = self.model.communicate(1, ">M0?")
    self.positiveA = self.model.communicate(1, ">M1?")

  def convertData(self):
    self.data["Negative"]["status"] = self.convertIndicator(self.negativeOutput)
    self.data["Positive"]["status"] = self.convertIndicator(self.positiveOutput)
    self.data["Negative"]["voltage"] = self.convertNumber(self.negativeV)
    self.data["Negative"]["current"] = self.convertNumber(self.negativeA)
    self.data["Positive"]["voltage"] = self.convertNumber(self.positiveV)
    self.data["Positive"]["current"] = self.convertNumber(self.positiveA)

  def convertIndicator(self, indicator):
    ind = indicator.split(":")[1]
    if len(ind) == 1:
      ind = int(ind)
    return ind

  def convertNumber(self, number):
    num = float(number.split(":")[1])
    return num
