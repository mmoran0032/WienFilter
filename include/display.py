# display - provides WFdisplay to show values for power supplies


import curses
from time import sleep

from include.bar import Bar


class WFDisplay(object):

    def __init__(self, controller):
        self.isUpdating = True
        self.refreshTime = 0.5
        self.controller = controller

    def __str__(self):
        return "WF-display, using curses {}".format(curses.version.decode())

    def initialize(self):
        self.initializeCurses()
        self.status = self.controller.getCurrentStatus()
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
        self.createStatusWindow()
        self.addStatusReadback()

    def createTitle(self):
        self.screen.addstr(0, 0, "  WIEN FILTER MONITOR AND CONTROL",
                           curses.A_BOLD | curses.color_pair(5))
        self.screen.chgat(-1, curses.color_pair(5))

    def createStatusWindow(self):
        self.statusWindow = curses.newwin(curses.LINES - 1, curses.COLS, 1, 0)
        self.ppsDisplay = self.statusWindow.subwin(9, curses.COLS - 4, 2, 2)
        self.npsDisplay = self.statusWindow.subwin(9, curses.COLS - 4, 12, 2)
        self.statusWindow.nodelay(True)
        self.statusWindow.box()

    def addStatusReadback(self):
        self.addSupply(self.ppsDisplay, "Positive", self.status["Pos"], 1, 1)
        self.addSupply(self.npsDisplay, "Negative", self.status["Neg"], 1, 1)

    def addSupply(self, window, supply, status, startX, startY):
        window.attron(curses.A_BOLD | curses.color_pair(1))
        window.addstr(startY, startX, "{} Power Supply".format(supply))
        window.addstr(startY + 2, startX + 2, "Voltage (kV):")
        window.addstr(startY + 3, startX + 2, "Current (μA):")
        window.addstr(startY + 5, startX + 2, "Ramp Rate (V/s):")
        window.attroff(curses.A_BOLD)
        window.addstr(startY + 2, startX + 19,
                      "{0:10.3f}".format(status["voltage"]))
        window.addstr(startY + 3, startX + 19,
                      "{0:10.3f}".format(status["current"]))
        window.addstr(startY + 5, startX + 19,
                      "{0:10d}".format(status["rate"]))
        self.createAndAddBar(
            window,
            status["voltage"],
            110.0,
            startY + 2,
            startX + 37)
        self.createAndAddBar(
            window,
            status["current"],
            2.0,
            startY + 3,
            startX + 37)
        window.box()

    def createAndAddBar(self, window, value, maximum, y, x):
        percent = abs(value) / float(maximum) * 100
        bar = Bar(33, percent)
        if percent > 75:
            window.addstr(y, x, str(bar), curses.A_BOLD | curses.color_pair(2))
        else:
            window.addstr(y, x, str(bar), curses.A_BOLD | curses.color_pair(3))

    def display(self):
        while self.isUpdating:
            self.ppsDisplay.clear()
            self.npsDisplay.clear()
            self.status = self.controller.getCurrentStatus()
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
