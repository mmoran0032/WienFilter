# model - provides WFmodel for TCP interaction with power supplies


import socket

import share
import share.commands as commands
from share.config import negativeAddress, positiveAddress


class WFmodel(object):
  def __init__(self):
    self.negativeSocket = self.createAndConnectSocket(negativeAddress)
    self.positiveSocket = self.createAndConnectSocket(positiveAddress)

  def __str__(self):
    return "WF-Model: {}, {}".format(self.negativeSocket.getsockname(),
                                     self.positiveSocket.getsockname())

  def createAndConnectSocket(self, address):
    try:
      s = socket.create_connection(address, timeout=5)
      return s
    except socket.timeout:
      raise

  def communicate(self, supply, command):
    sock = self.determineSocket(supply)
    sock.send(command.encode())
    return sock.recv(1024).decode()

  def determineSocket(self, supply):
    if supply == 0:
      return self.negativeSocket
    elif supply == 1:
      return self.positiveSocket

  def closeConnection(self):
    self.closeSocket(self.negativeSocket)
    self.closeSocket(self.positiveSocket)

  def closeSocket(self, sock):
    sock.close()
