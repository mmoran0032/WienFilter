# model - provides WFModel for TCP interaction with power supplies


import socket


class WFModel:

    def __init__(self, address):
        self.address = address
        self.socket = self.createAndConnectSocket(address)
        self.previous = "No previous message"
        self.connected = False

    def createAndConnectSocket(self, address=None):
        if address is None:
            address = self.address
        try:
            s = socket.create_connection(address, timeout=5)
            self.connected = True
            return s
        except socket.timeout:
            print("timeout exceeed for establishing connection\n")
            raise
        except socket.gaierror:
            print("address not found\n")
            raise

    def communicate(self, command):
        try:
            self.socket.send(command.encode())
            data = self.readAllData()
            return data
        except socket.timeout:
            print("communication timed out\n")
            raise

    def readAllData(self):
        data = ""
        while "\n" not in data:
            data = "{}{}".format(data, self.socket.recv(1024).decode())
        return data[:-1]

    def disconnect(self):
        self.socket.close()
        self.connected = False
