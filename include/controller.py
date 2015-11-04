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
    self.refreshTime = 3

  def __str__(self):
    return "WF: {}\n    {}".format(self.model, self.display)

  def run(self):
    while True:
      for supply in ("pos", "neg"):
        data = self.model.communicate(supply, "")
        self.display.show(data)
      sleep(self.refreshTime)
