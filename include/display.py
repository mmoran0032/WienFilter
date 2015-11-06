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
    status = curses.newwindow(curses.LINES-2, curses.COLS, 1, 0)
