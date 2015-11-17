# readback - simplifies creating the power supply displays


from include.bar import Bar


class Readback(object):

    def __init__(self, name, size, showBar=True, numberFormat="8.3f"):
        self.name = name
        self.size = size
        self.showBar = showBar
        self.value = 0.0
        self.setpoint = 0.0
        self.limit = None
        self.percent = None
        self.numberFormat = numberFormat

    def __str__(self):
        display = "{0:<13s}    {1:{nf}}    {2:{nf}}    ".format(
            self.name, self.setpoint, self.value, nf=self.numberFormat)
        display = self.buildBar(self.size - len(display), display)
        return display

    def buildBar(self, barsize, display):
        if barsize < 0:
            self.showBar = False
        if self.showBar and self.limit is not None:
            self.percent = abs(self.value / self.limit * 100)
            bar = Bar(barsize, self.percent)
            display = "{}{}".format(display, str(bar))
        return display

    def updateValues(self, value, setpoint, limit=None):
        self.value = value
        self.setpoint = setpoint
        self.limit = limit
