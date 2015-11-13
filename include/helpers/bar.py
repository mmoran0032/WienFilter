# bar - provides Bar for visually displaying percentages and loads


from math import modf

# bars = [" ", " ", " ", "|", "|", "|", "|", "█", "█"]
# bars = [" ", " ", " ", " ", "|", "|", "|", "|", "|"]
bars = [" ", " ", " ", " ", "█", "█", "█", "█", "█"]


class Bar(object):

    def __init__(self, size, percent=0, preChar="[", postChar="]",
                 emptyChar=" ", withText=True):
        self._size = size
        self._percent = percent
        self.preChar = preChar
        self.postChar = postChar
        self.emptyChar = emptyChar
        self.withText = withText

    def __str__(self):
        frac, whole = modf(self.size * self.percent / 100.0)
        output = bars[8] * int(whole)
        if frac > 0:
            output += bars[int(frac * 8)]
            whole += 1
        output = "{}{}".format(output, self.emptyChar * int(self.size - whole))
        if self.withText:
            output = "{0}{1:>5.1f}%".format(output, self.percent)
        return output

    @property
    def size(self):
        if self.withText:
            return self._size - 5
        else:
            return self._size

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, value):
        if 0 <= value <= 100:
            self._percent = value
