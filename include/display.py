# display - provides WFdisplay to show values for power supplies


import curses
import sys


class WFdisplay(object):
  def __init__(self, status):
    self.initializeCurses()
    self.status = status

  def __str__(self):
    return "WF-display, using curses {}".format(curses.version.decode())

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

  def assembleScreen(self):
    self.createTitleAndMenu()
    self.createStatusWindow()
    self.addStatusReadback()

  def createTitleAndMenu(self):
    self.screen.addstr("WIEN FILTER MONITOR",
                       curses.A_REVERSE | curses.color_pair(4))
    self.screen.chgat(-1, curses.A_REVERSE)
    self.screen.addstr(curses.LINES-1, 0,
                       "'E' edit values, 'C' close connection, 'Q' shutdown")
    self.screen.chgat(curses.LINES-1, 1, curses.A_BOLD | curses.color_pair(3))
    self.screen.chgat(curses.LINES-1, 18, curses.A_BOLD | curses.color_pair(3))
    self.screen.chgat(curses.LINES-1, 40, curses.A_BOLD | curses.color_pair(2))

  def createStatusWindow(self):
    self.status = curses.newwindow(curses.LINES-2, curses.COLS, 1, 0)
    self.statusDisplay = self.status.subwin(curses.LINES-4,
                                            curses.COLS-2, 2, 1)
    self.status.box()

  def addStatusReadback(self):
    self.addSupply("Positive", self.status["Pos"], 4, 3)
    self.addSupply("Negative", self.status["Neg"], 4, 8)

  def addSupply(self, supply, status, startX, startY):
    self.statusDisplay.attron(curses.A_BOLD | curses.color_pair(1))
    self.statusDisplay.addstr(startY, startX, "{} Power Supply".format(supply))
    self.statusDisplay.addstr(startY+1, startX, "Voltage (kV):")
    self.statusDisplay.addstr(startY+2, startX, "Current (μA):")
    self.statusDisplay.addstr(startY+3, startX, "Ramp Rate (V/s):")
    self.statusDisplay.attroff(curses.A_BOLD)
    self.statusDisplay.addstr(startY+1, startX+17,
                              "{0:10.3f}".format(status["voltage"]))
    self.statusDisplay.addstr(startY+1, startX+17,
                              "{0:10.3f}".format(status["current"]))
    self.statusDisplay.addstr(startY+1, startX+17,
                              "{0:10.1f}".format(status["rate"]))

  def display(self):
    self.statusDisplay.clear()
    self.addStatusReadback()
    self.refreshDisplay()

  def refreshDisplay(self):
    self.screen.noutrefresh()
    self.status.noutrefresh()
    self.statusDisplay.noutrefresh()
    curses.doupdate()

  def receiveData(self, data):
    self.status = data

  def end(self):
    curses.echo()
    curses.nocbreak()
    curses.curs_set(0)
    curses.endwin()
