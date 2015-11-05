# display - provides WFdisplay to show values for power supplies


import curses
import curses.panel
from curses.textpad import Textbox
import sys


class WFdisplay(object):
  def __init__(self):
    self.size = (80, 24)
    self.screen = curses.initscr()
    self.initializeCurses()
    self.colors = {
      "title": A_BOLD,
      "no_color": curses.color_pair(1),
      "nice": curses.color_pair(4) | curses.A_BOLD,
      "default": curses.color_pair(3) | curses.A_BOLD,
      "critical": curses.color_pair(2) | curses.A_BOLD
    }
    self.term_window = self.screen.subwin(0, 0)
    self.term_window.keypad(1)
    self.term_window.nodelay(1)
    self.pressedkey = -1

  def initializeCurses(self):
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)

  def __str__(self):
    return "WF-Display: {}".format(self.data)

  def display(self, data):
    screenY, screenX = self.screen.getmaxyx()

  def updateData(self, data):
    self.data = data

  def catchKey(self):
    self.pressedkey = self.term_window.getch()
    if self.pressedkey in (ord("q"), ord("Q")):
      self.end()
      sys.exit(0)

  def end(self):
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()
