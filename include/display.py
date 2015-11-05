# display - provides WFdisplay to show values for power supplies


import curses
import curses.panel
import sys


class WFdisplay(object):
  def __init__(self):
    self.screen = curses.initscr()
    self.initializeCurses()
    self.colors = {
      "title": A_BOLD,
      "no_color": curses.color_pair(1),
      "nice": curses.color_pair(4) | curses.A_BOLD,
      "default": curses.color_pair(3) | curses.A_BOLD,
      "critical": curses.color_pair(2) | curses.A_BOLD
    }
    self.termWindow = self.screen.subwin(0, 0)
    self.termWindow.keypad(1)
    self.termWindow.nodelay(1)
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

  def update(self, data):
    self.flushDisplay(data)
    exitKeyPressed = False
    while not exitKeyPressed:
      self.pressedkey = self.catchKey()
      exitKeyPressed = self.isExitKey()
      self.flushDisplay(data)
      curses.napms(100)

  def flushDisplay(self):
    self.termWindow.erase()
    self.display(data)

  def display(self, data):
    # THIS IS THE MAIN BRUNT OF THE DISPLAY, WITH BARS AND NUMBERS AND COLORS
    # SO HEAVY ON THE CURSES STUFF...
    pass

  def catchKey(self):
    self.pressedkey = self.term_window.getch()
    if isExitKey():
      self.end()
      sys.exit(0)

  def isExitKey(self):
    return self.pressedkey in (ord("q"), ord("Q")

  def end(self):
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()
