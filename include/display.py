# display - provides WFDisplay to show values for power supplies


import curses
from time import sleep

from include.readback import Readback


class WFDisplay(object):

    def __init__(self, controller):
        self.isUpdating = True
        self.refreshTime = 0.5
        self.controller = controller

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

    def addStatusReadback(self):
        self.addSupply(self.ppsDisplay, "Positive", self.status["Positive"])
        self.addSupply(self.npsDisplay, "Negative", self.status["Negative"])

    def addSupply(self, window, supply, status, startY=1, startX=1):
        window.box()
        window.attron(curses.A_BOLD | curses.color_pair(1))
        window.addstr(startY - 1, startX, " {} Power Supply ".format(supply))
        window.addstr(startY + 6, startX + 1, "Status:")
        window.attroff(curses.A_BOLD)

        self.addReadbackWithBar(window, "Voltage (kV):", status["voltage"],
                                startY + 1, startX + 1)
        self.addReadbackWithBar(window, "Current (μA):", status["current"],
                                startY + 2, startX + 1)

        ramp = Readback("Ramp Rate:", 71, showBar=False, numberFormat="8d")
        ramp.updateValues(status["rate"]["value"],
                          status["rate"]["setpoint"])
        window.addstr(startY + 4, startX + 1, str(ramp))
        window.chgat(startY + 4, startX + 1, 13, curses.A_BOLD)
        window.chgat(startY + 4, startX + 30, 8, curses.A_BOLD)

        window.addstr(startY + 6, startX + 18,
                      "{0:>8s}".format(status["status"]), curses.A_BOLD)

    def addReadbackWithBar(self, window, name, status, y, x):
        info = Readback(name, 71)
        info.updateValues(status["value"], status["setpoint"], status["limit"])
        window.addstr(y, x, str(info))
        window.chgat(y, x, 13, curses.A_BOLD)
        if info.percent > 75:
            window.chgat(y, x + 29, 44, curses.A_BOLD | curses.color_pair(2))
        else:
            window.chgat(y, x + 29, 44, curses.A_BOLD | curses.color_pair(3))

    def refreshDisplay(self):
        self.screen.noutrefresh()
        self.statusWindow.noutrefresh()
        self.ppsDisplay.noutrefresh()
        self.npsDisplay.noutrefresh()
        curses.doupdate()

    def handleKeypress(self, key):
        if key in (ord("q"), ord("Q")):
            self.end()

    def end(self):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(1)
        curses.endwin()
        self.isUpdating = False
