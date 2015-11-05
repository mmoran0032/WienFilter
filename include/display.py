# display - provides WFdisplay to show values for power supplies


import curses
import curses.panel
from curses.textpad import Textbox
import sys


class WFdisplay(object):
  def __init__(self):
    self.termX = 80
    self.termY = 24
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

  def catchKey(self):
    self.pressedkey = self.term_window.getch()
    if isExitKey():
      self.end()
      sys.exit(0)

  def isExitKey(self):
    return self.pressedkey in (ord("q"), ord("Q"))

  def end(self):
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()

  def initializeLineColumn(self):
    self.initializeLine()
    self.initializeColumn()

  def initializeLine(self):
    self.line = 0
    self.nextLine = 0

  def initializeColumn(self):
    self.cloumn = 0
    self.nextColumn = 0

  def newLine(self):
    self.line = self.nextLine

  def newColumn(self):
    self.column = self.nextColumn

  def display(self, data):
    self.initializeLineColumn()
    screenY, screenX = self.screen.getmaxyx()
    pluginMaxWidth = None
    # build individual stats views

  def flush(self, data):
    self.termWindow.erase()
    self.display(data)

  def update(self, data):
    self.flush(data)
    exitKeyPressed = False
    while not exitKeyPressed:
      pressedKey = self.catchKey()
      exitKeyPressed = pressedKey in (ord("q"), ord("Q"))
      if not exitKeyPressed and pressedKey > -1:
        self.flush(data)
      curses.napms(100)














