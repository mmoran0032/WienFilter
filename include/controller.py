# controller - provides WFcontroller to process info from user and model


from time import sleep

import include
from include.display import WFdisplay
from include.model import WFmodel
from include.monitor import WFmonitor

import share
from share.commands import commands


class WFcontroller(object):
  def __init__(self):
    self.model = WFmodel()
    self.display = WFdisplay()
    self.refreshTime = 3
    self.data = {}

  def __str__(self):
    return "WF: {}\n    {}".format(self.model, self.display)

  def run(self):
    while True:
      self.querySupplies()
      self.display.display(self.data)
      sleep(self.refreshTime)

  def querySupplies(self):
    self.negativeOutput = self.model.communicate(0, ">DON?")
    self.positiveOutput = self.model.communicate(1, ">DON?")
    self.negativeV = self.model.communicate(0, ">M0?")
    self.negativeA = self.model.communicate(0, ">M1?")
    self.positiveV = self.model.communicate(1, ">M0?")
    self.positiveA = self.model.communicate(1, ">M1?")

  def convertData(self):
    self.data["nOut"] = self.convertIndicator(self.negativeOutput)
    self.data["pOut"] = self.convertIndicator(self.positiveOutput)
    self.data["nV"] = self.convertNumber(self.negativeV)
    self.data["nA"] = self.convertNumber(self.negativeA)
    self.data["pV"] = self.convertNumber(self.positiveV)
    self.data["pA"] = self.convertNumber(self.positiveA)

  def convertIndicator(self, indicator):
    ind = indicator.split(":")[1]
    if len(ind) == 1:
      ind = int(ind)
    return ind

  def convertNumber(self, number):
    num = float(number.split(":")[1])
    return num
