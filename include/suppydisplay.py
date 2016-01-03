# supplydisplay - provides WFSupplyDisplay to show a single power supply


class WFSupplyDisplay:

    def __init__(self, name, window, size):
        self.name = name
        self.window = window
        self.size = size
        self.labels = {}
        self.readbacks = {}
        self.controls = {}

    def createView(self):
        self.window.box()
        self.createAllLabels()
        self.createAllReadbacks()
        self.createAllControls()

    def createAllLabels(self):
        for key, data in self.labels.items():
            location = data[0], data[1]
            text = data[2]
            formatting = data[3]
            self.window.addstr(location[0], location[1], text, formatting)

    def createAllReadBacks(self):
        for key, data in self.readbacks.items():
            location = data[0], data[1]
            text = data[2]
            formatting = data[3]
            self.window.addstr(location[0], location[1], text, formatting)

    def createAllControls(self):
        pass
