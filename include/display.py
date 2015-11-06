# display - provides WFdisplay to show values for power supplies


import curses
import sys


class WFdisplay(object):
  def __init(self):
    self.initializeCurses()

  def initializeCurses(self):
    self.screen = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)

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

  def addStatusReadback(self, status):
    self.addSupply("Positive", status)
    self.addSupply("Negative", status)

  def addSupply(self, supply, status, startX, startY):
    self.statusDisplay.attron(curses.A_BOLD | curses.color_pair(1))
    self.addstr(startY, startX, "{} Power Supply".format(supply))
    self.addstr(startY+1, startX,
                "Voltage (kV): {}".format(status[supply]["voltage"]))
    self.addstr(startY+2, startX,
                "Current (μA): {}".format(status[supply]["current"]))
    self.addstr(startY+3, startX,
                "Ramp Rate (V/s): {}".format(status[supply]["rate"]))

  def refreshDisplay(self):
    self.screen.noutrefresh()
    self.status.noutrefresh()
    self.statusDisplay.noutrefresh()
    curses.doupdate()

  def end(self):
    curses.echo()
    curses.nocbreak()
    curses.curs_set(0)
    curses.endwin()
