# controller - provides WFController to process info from user and model


from include.display import WFDisplay
from include.model import WFModel
from share.config import negativeAddress, positiveAddress


class WFController(object):

    def __init__(self):
        self._status = {
            "Pos": {"status": 0, "voltage": 0, "current": 0, "rate": 0},
            "Neg": {"status": 0, "voltage": 0, "current": 0, "rate": 0}
        }
        self.setpoints = {
            "Pos": {"status": 0, "voltage": 0, "current": 0, "rate": 0},
            "Neg": {"status": 0, "voltage": 0, "current": 0, "rate": 0}
        }
        self.posModel = WFModel(positiveAddress)
        self.negModel = WFModel(negativeAddress)
        self.display = WFDisplay(self)
        self.selection = None

    def __str__(self):
        return "WF: {} {}\n    {}".format(self.posModel, self.negModel,
                                          self.display)

    def run(self):
        try:
            self.display.initialize()
            self.display.display()
        except:
            self.display.end()
            raise

    def querySupplies(self):
        self.querySingleSupply(self.posModel, "Pos")
        self.querySingleSupply(self.negModel, "Neg")

    def querySingleSupply(self, supply, name):
        self._status[name] = {
            "status": supply.communicate(">KS?\n"),
            "voltage": supply.communicate(">M0?\n"),
            "current": supply.communicate(">M1?\n")
        }

    def convertAllData(self):
        self._status["Pos"] = self.convertData(self._status["Pos"])
        self._status["Neg"] = self.convertData(self._status["Neg"])

    def convertData(self, subStatus):
        newStatus = {}
        newStatus["status"] = self.convertIndicator(subStatus["status"])
        newStatus["voltage"] = self.convertNumber(subStatus["voltage"], -3)
        newStatus["current"] = self.convertNumber(subStatus["current"], 6)
        return newStatus

    def convertIndicator(self, indicator):
        ind = indicator.split(":")[1]
        if len(ind) == 1:
            ind = int(ind)
        return ind

    def convertNumber(self, number, power=1):
        num = float(number.split(":")[1])
        num *= 10 ** power
        return num

    @property
    def status(self):
        self.querySupplies()
        self.convertAllData()
        return self._status
