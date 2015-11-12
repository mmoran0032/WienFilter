#!/usr/bin/env python3


from include.display import WFDisplay


class DummyController(object):

    def __init__(self):
        self._status = {
            "Pos": {
                "status": "0110001",
                "voltage": 88.776,
                "current": 0.824,
                "rate": 250
            },
            "Neg": {
                "status": "0110001",
                "voltage": -28.773,
                "current": 0.512,
                "rate": 250
            }
        }

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


if __name__ == "__main__":
    d = WFDisplay(DummyController())
    d.initialize()
    d.display()
