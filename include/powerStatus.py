# powerStatus - reformats status readback


class PSStatus(object):

    def __init__(self):
        self.status = None

    def formatData(self):
        """
        Status held by >KS as follows:
        I-REG, V-REG, ON-Status, 3-Reg, X-Stat, Cal-Mode, Unused, SEL-D
        """
        self.currentControl = bool(self.status[0])
        self.voltageControl = bool(self.status[1])
        self.supplyOn = bool(self.status[2])
        self.digitallyControlled = bool(self.status[7])
