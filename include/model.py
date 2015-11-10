# model - provides WFmodel for TCP interaction with power supplies


from itertools import takewhile
import socket

from share.config import negativeAddress, positiveAddress


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
    data = self.readAllData(sock)
    return data

  def determineSocket(self, supply):
    if supply == 0:
      return self.negativeSocket
    elif supply == 1:
      return self.positiveSocket

  def readAllData(self, sock):
    data = ""
    while "\n" not in data:
      data = "{}{}".format(data, sock.recv(1024).decode())
    return data[:-1]

  def closeConnection(self):
    self.closeSocket(self.negativeSocket)
    self.closeSocket(self.positiveSocket)

  def closeSocket(self, sock):
    sock.close()
