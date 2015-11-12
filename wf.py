#!/usr/bin/env python3


import include
from include.controller import WFcontroller


if __name__ == "__main__":
    controller = WFcontroller()
    print(controller)
    controller.run()
