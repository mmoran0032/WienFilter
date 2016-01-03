#!/usr/bin/env python3


from include.display import WFDisplay


class DummyController:

    def __init__(self):
        self.status = {
            "Positive": {
                "status": "0110001",
                "voltage": {
                    "value": 88.776, "setpoint": 88.78, "limit": 110
                },
                "current": {
                    "value": 0.824, "setpoint": 1.0, "limit": 2.0
                },
                "rate": {
                    "value": 250, "setpoint": 250
                }
            },
            "Negative": {
                "status": "0110001",
                "voltage": {
                    "value": -28.773, "setpoint": -28.74, "limit": -110
                },
                "current": {
                    "value": 0.512, "setpoint": 1.0, "limit": 2.0
                },
                "rate": {
                    "value": 250, "setpoint": 250
                }
            }
        }


if __name__ == "__main__":
    d = WFDisplay(DummyController())
    d.initialize()
    d.display()
