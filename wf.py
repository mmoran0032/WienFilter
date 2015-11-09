#!/usr/bin/env python3


import include
from include.controller import WFcontroller


def main():
  controller = WFcontroller()
  print(controller)
  controller.run()


if __name__ == "__main__":
  main()
