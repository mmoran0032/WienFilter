# display - provides WFdisplay to show values for power supplies


import curses
from time import sleep

from include.bar import Bar


class WFDisplay(object):
  def __init__(self, controller):
    self.isUpdating = True
    self.refreshTime = 0.5
    self.controller = controller
    self.initializeCurses()
    self.status = self.controller.getCurrentStatus()
    self.assembleScreen()

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
    self.statusWindow = curses.newwin(curses.LINES-1, curses.COLS, 1, 0)
    self.statusDisplay = self.statusWindow.subwin(curses.LINES-4,
                                                  curses.COLS-2, 2, 1)
    self.statusWindow.nodelay(True)
    self.statusWindow.box()

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
    self.statusDisplay.addstr(startY+2, startX+17,
                              "{0:10.3f}".format(status["current"]))
    self.statusDisplay.addstr(startY+3, startX+17,
                              "{0:10d}".format(status["rate"]))
    self.createAndAddBar(status["voltage"], 110.0, startY+1, startX+35)
    self.createAndAddBar(status["current"], 2.0, startY+2, startX+35)

  def createAndAddBar(self, value, maximum, y, x):
    percent = abs(value)/float(maximum) * 100
    bar = Bar(35, percent)
    if percent > 75:
      self.statusDisplay.addstr(y, x, str(bar),
                                curses.A_BOLD | curses.color_pair(2))
    else:
      self.statusDisplay.addstr(y, x, str(bar),
                                curses.A_BOLD | curses.color_pair(3))

  def display(self):
    while self.isUpdating:
      self.statusDisplay.clear()
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
    self.statusDisplay.noutrefresh()
    curses.doupdate()

  def end(self):
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()
    self.isUpdating = False
