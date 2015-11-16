# controller - provides WFController to process info from user and model


from include.display import WFDisplay
from include.model import WFModel
from share.config import negativeAddress, positiveAddress


class WFController(object):

    def __init__(self):
        # self._status = {
        #     "Positive": {
        #         "status": 0,
        #         "voltage": {"value": 0, "setpoint": 0, "limit": 0},
        #         "current": {"value": 0, "setpoint": 0, "limit": 0},
        #         "rate": 0
        #     },
        #     "Negative": {
        #         "status": 0,
        #         "voltage": {"value": 0, "setpoint": 0, "limit": 0},
        #         "current": {"value": 0, "setpoint": 0, "limit": 0},
        #         "rate": 0
        #     }
        # }
        self._status = dict()
        self.posModel = WFModel(positiveAddress)
        self.negModel = WFModel(negativeAddress)
        self.display = WFDisplay(self)
        self.selection = None

    def run(self):
        try:
            self.display.initialize()
            self.display.display()
        except:
            self.display.end()
            raise

    @property
    def status(self):
        self.querySupplies()
        self.convertAllData()
        return self._status

    def querySupplies(self):
        if self.posModel.connected:
            self.querySingleSupply(self.posModel, "Positive")
        if self.negModel.connected:
            self.querySingleSupply(self.negModel, "Negative")

    def querySingleSupply(self, supply, name):
        self._status[name]["status"] = supply.communicate(">KS?\n")
        self._status[name]["voltage"]["value"] = supply.communicate(">M0?\n")
        self._status[name]["current"]["value"] = supply.communicate(">M1?\n")

    def convertAllData(self):
        self._status["Positive"] = self.convertData(self._status["Positive"])
        self._status["Negative"] = self.convertData(self._status["Negative"])

    def convertData(self, subStatus):
        newStatus = {}
        newStatus["status"] = self.convertIndicator(subStatus["status"])
        newStatus["voltage"]["value"] = self.convertNumber(
            subStatus["voltage"]["value"], -3)
        newStatus["current"]["value"] = self.convertNumber(
            subStatus["current"]["value"], 6)
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
