#!/usr/bin/env python3


from include.display import WFDisplay


class DummyController(object):

    def __init__(self):
        self.status = {
            "Positive": {
                "status": "0110001",
                "voltage": {
                    "value": 88.776, "setpoint": 88.78, "limit": 110
                },
                "current": 0.824,
                "rate": 250
            },
            "Negative": {
                "status": "0110001",
                "voltage": {
                    "value": -28.773, "setpoint": -28.74, "limit": -110
                },
                "current": 0.512,
                "rate": 250
            }
        }


if __name__ == "__main__":
    d = WFDisplay(DummyController())
    d.initialize()
    d.display()
