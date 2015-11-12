#!/usr/bin/env python3
# wf - monitors and controls the St. GEORGE wien filter electrodes


from include.controller import WFController


if __name__ == "__main__":
    controller = WFController()
    controller.run()
