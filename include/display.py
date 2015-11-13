# display - provides WFDisplay to show values for power supplies


import curses
from time import sleep

# from include.helpers.powerStatus import PSStatus
from include.helpers.readback import Readback


class WFDisplay(object):

    def __init__(self, controller):
        self.isUpdating = True
        self.refreshTime = 0.5
        self.controller = controller

    def __str__(self):
        return "WFDisplay, using curses {}".format(curses.version.decode())

    def initialize(self):
        self.initializeCurses()
        self.status = self.controller.status
        self.assembleScreen()

    def initializeCurses(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)

    def assembleScreen(self):
        self.createTitle()
        self.createGlobalOptions()
        self.createStatusWindow()
        self.addStatusReadback()

    def createTitle(self):
        self.screen.chgat(0, 0, curses.color_pair(5))
        self.screen.addstr(0, 2, "WIEN FILTER MONITOR AND CONTROL",
                           curses.A_BOLD | curses.color_pair(5))

    def createGlobalOptions(self):
        self.screen.chgat(curses.LINES - 1, 0, curses.color_pair(5))
        self.screen.addstr(curses.LINES - 1, 2, "SET   DISCONNECT   EXIT",
                           curses.A_BOLD | curses.color_pair(5))

    def createStatusWindow(self):
        self.statusWindow = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
        self.ppsDisplay = self.statusWindow.subwin(10, curses.COLS - 4, 2, 2)
        self.npsDisplay = self.statusWindow.subwin(10, curses.COLS - 4, 12, 2)
        self.statusWindow.nodelay(True)

    def addStatusReadback(self):
        self.addSupply(self.ppsDisplay, "Positive", self.status["Pos"], 1, 1)
        self.addSupply(self.npsDisplay, "Negative", self.status["Neg"], 1, 1)

    def addSupply(self, window, supply, status, startX, startY):
        window.box()
        window.addstr(startY - 1, startX, " {} Power Supply ".format(supply),
                      curses.A_BOLD | curses.color_pair(4))

        self.voltageReadback = Readback("Voltage (kV):", 71)
        self.voltageReadback.updateValues(status["voltage"],
                                          status["voltage"], 110.0)
        self.voltageReadback.showBar = True
        window.addstr(startY + 1, startX + 1,
                      self.voltageReadback.buildDisplay())
        self.currentReadback = Readback("Current (μA):", 71)
        self.currentReadback.updateValues(status["current"],
                                          status["current"], 2.0)
        self.voltageReadback.showBar = True
        window.addstr(startY + 2, startX + 1,
                      self.currentReadback.buildDisplay())
        self.rampReadback = Readback("Ramp Rate:", 71)
        self.rampReadback.updateValues(status["rate"], status["rate"])
        self.rampReadback.showDecimal = False
        window.addstr(startY + 4, startX + 1,
                      self.rampReadback.buildDisplay())
        window.addstr(startY + 6, startX + 1, "Status:")
        window.addstr(startY + 6, startX + 18,
                      "{0:>8s}".format(status["status"]))

    def display(self):
        while self.isUpdating:
            self.ppsDisplay.clear()
            self.npsDisplay.clear()
            self.status = self.controller.status
            self.addStatusReadback()
            self.refreshDisplay()
            key = self.statusWindow.getch()
            if key != -1:
                self.handleKeypress(key)
            sleep(self.refreshTime)

    def handleKeypress(self, key):
        if key in (ord("q"), ord("Q")):
            self.end()

    def refreshDisplay(self):
        self.screen.noutrefresh()
        self.statusWindow.noutrefresh()
        self.ppsDisplay.noutrefresh()
        self.npsDisplay.noutrefresh()
        curses.doupdate()

    def end(self):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
        self.isUpdating = False
