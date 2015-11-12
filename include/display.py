# display - provides WFDisplay to show values for power supplies


import curses
from time import sleep

from include.bar import Bar


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
        window.attron(curses.A_BOLD | curses.color_pair(1))
        window.addstr(startY - 1, startX, " {} Power Supply ".format(supply))
        window.addstr(startY + 1, startX + 1, "Voltage (kV):")
        window.addstr(startY + 2, startX + 1, "Current (μA):")
        window.addstr(startY + 4, startX + 1, "Ramp Rate:")
        window.addstr(startY + 6, startX + 1, "Status:")
        window.attroff(curses.A_BOLD)
        window.addstr(startY + 1, startX + 18,
                      "{0:8.3f}".format(status["voltage"]))
        window.addstr(startY + 1, startX + 30,
                      "{0:8.3f}".format(status["voltage"]))
        window.addstr(startY + 2, startX + 18,
                      "{0:8.3f}".format(status["current"]))
        window.addstr(startY + 2, startX + 30,
                      "{0:8.3f}".format(status["current"]))
        window.addstr(startY + 4, startX + 18,
                      "{0:8d}".format(status["rate"]))
        window.addstr(startY + 4, startX + 30,
                      "{0:8d}".format(status["rate"]), curses.A_BOLD)
        window.addstr(startY + 6, startX + 18,
                      "{0:>8s}".format(status["status"]))
        self.addBar(window, status["voltage"], 110.0, startY + 1, startX + 42)
        self.addBar(window, status["current"], 2.0, startY + 2, startX + 42)

    def addBar(self, window, value, maximum, y, x):
        percent = abs(value) / float(maximum) * 100
        bar = Bar(30, percent)
        window.addstr(y, x, str(bar))
        if percent > 75:
            window.chgat(y, x - 12, 43, curses.A_BOLD | curses.color_pair(2))
        else:
            window.chgat(y, x - 12, 43, curses.A_BOLD | curses.color_pair(3))

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
