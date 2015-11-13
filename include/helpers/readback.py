# readback - handles a control/display for a power supply


from include.helpers.bar import Bar


class Readback(object):

    def __init__(self, name, width):
        self.setpoint = 0.0
        self.actual = 0.0
        self.percent = None
        self.limit = None
        self.showBar = False
        self.showDecimal = True
        self.name = name
        self.width = width

    def buildDisplay(self):
        if self.showDecimal:
            return self.buildDisplay_decimal()
        else:
            return self.buildDisplay_noDecimal()

    def buildDisplay_decimal(self):
        display = "{0:<13s}    {1:8.3f}".format(self.name, self.setpoint)
        display = "{0}    {1:8.3f}    ".format(display, self.actual)
        display = self.buildBar(self.width - len(display), display)
        return display

    def buildDisplay_noDecimal(self):
        display = "{0:<13s}    {1:8d}".format(self.name, self.setpoint)
        display = "{0}    {1:8d}    ".format(display, self.actual)
        display = self.buildBar(self.width - len(display), display)
        return display

    def buildBar(self, barsize, display):
        if barsize < 0:
            self.showBar = False
        if self.showBar and self.limit is not None:
            self.percent = abs(self.actual) / self.limit * 100
            bar = Bar(barsize, self.percent)
            display = "{}{}".format(display, str(bar))
        return display

    def updateValues(self, setpoint, actual, limit=None):
        self.setpoint = setpoint
        self.actual = actual
        self.limit = limit
