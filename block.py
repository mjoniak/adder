from typing import Tuple


class Block(object):
    def __init__(self, x, y, name=""):
        self._width = 50
        self._height = 50
        self._x, self._y = x, y
        self._name = name

    def rect(self) -> Tuple[int, int, int, int]:
        return self._x, self._y, self._x + self._width, self._y + self._height

    def notify(self):
        print(self._name, "clicked")

    def contains(self, position):
        return self._x <= position.x <= self._x + self._width \
               and self._y <= position.y <= self._y + self._height
