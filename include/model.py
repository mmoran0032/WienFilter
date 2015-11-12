# model - provides WFmodel for TCP interaction with power supplies


import socket


class WFModel(object):
  def __init__(self, address):
    self.socket = self.createAndConnectSocket(address)
    self.previous = "No previous message"

  def __str__(self):
    return "WF-Model: {}".format(self.socket.getsockname())

  def createAndConnectSocket(self, address):
    try:
      s = socket.create_connection(address, timeout=25)
      return s
    except socket.timeout:
      raise

  def communicate(self, command):
    sock.send(command.encode())
    data = self.readAllData(sock)
    return data

  def readAllData(self, sock):
    data = ""
    while "\n" not in data:
      data = "{}{}".format(data, sock.recv(1024).decode())
    return data[:-1]

  def disconnect(self):
    sock.close()
