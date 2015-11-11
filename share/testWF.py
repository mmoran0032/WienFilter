#!/usr/bin/env python3


from include.model import WFmodel


if __name__ == "__main__":
  m = WFmodel()
  print(m)
  print(m.communicate(0, ">DON?\n"))
  print(m.communicate(1, ">DON?\n"))
  m.closeConnection()
