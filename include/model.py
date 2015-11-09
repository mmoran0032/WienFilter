# model - provides WFmodel for TCP interaction with power supplies


import socket

from share.config import negativeAddress, positiveAddress
#from share.testconfig import negativeAddress, positiveAddress


class WFmodel(object):
  def __init__(self, negAddr=negativeAddress, posAddr=positiveAddress):
    self.negativeSocket = self.createAndConnectSocket(negAddr)
    self.positiveSocket = self.createAndConnectSocket(posAddr)
    self.previous = "No previous message"

  def __str__(self):
    return "WF-Model: {}, {}".format(self.negativeSocket.getsockname(),
                                     self.positiveSocket.getsockname())

  def createAndConnectSocket(self, address):
    try:
      s = socket.create_connection(address, timeout=25)
      return s
    except socket.timeout:
      raise

  def communicate(self, supply, command):
    sock = self.determineSocket(supply)
    sock.send(command.encode())
    data = sock.recv(64).decode()[:-1]
    return data

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
