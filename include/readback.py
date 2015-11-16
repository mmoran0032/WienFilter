# readback - simplifies creating the power supply displays


from include.bar import Bar


class Readback(object):

    def __init__(self, name, size, showBar=True):
        self.name = name
        self.size = size
        self.showBar = showBar
        self.value = 0.0
        self.setpoint = 0.0
        self.limit = None

    def __str__(self):
        display = "{0:<13s}    {1:8.3f}".format(self.name, self.setpoint)
        display = "{0}    {1:8.3f}    ".format(display, self.value)
        display = self.buildBar(self.size - len(display), display)
        return display

    def buildBar(self, barsize, display):
        if barsize < 0:
            self.showBar = False
        if self.showBar and self.limit is not None:
            percent = abs(self.value / self.limit * 100)
            bar = Bar(barsize, percent)
            display = "{}{}".format(display, str(bar))
        return display

    def updateValues(self, value, setpoint, limit=None):
        self.value = value
        self.setpoint = setpoint
        self.limit = limit
