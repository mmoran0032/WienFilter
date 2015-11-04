#!/usr/bin/env python3


import socket
import sys

from configDummy import negativeAddress, positiveAddress

responseDummy = {
  ">DON?": "DON:1",
  ">KS?": "KS: 01100000",
  ">M0?": "M0:+0.00000E+00",
  ">M1?": "M1:+0.00000E+00"
}


def main(address):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if address == "neg":
    s.bind(negativeAddress)
  elif address == "pos":
    s.bind(positiveAddress)
  s.listen(1)

  while True:
    connection, clientAddress = s.accept()
    try:
      print("connection from {}".format(clientAddress))
      while True:
        data = connection.recv(50)
        if data and data in responseDummy:
          print(data)
          output = responseDummy[data]
          print(output)
          connection.sendall(output)
        else:
          break
    finally:
      connection.close()


if __name__ == "__main__":
  try:
    address = sys.argv[1]
    main(address)
  except IndexError:
    sys.exit()
