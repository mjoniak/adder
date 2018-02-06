from typing import Tuple


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def rect(self) -> Tuple[int, int, int, int]:
        return self.x, self.y, self.x + self.width, self.y + self.height

    def contains(self, position):
        return self.x <= position.x <= self.x + self.width \
               and self.y <= position.y <= self.y + self.height

    def pos(self):
        return self.x, self.y

    def middle(self):
        return self.x + self.width / 2, self.y + self.height / 2

    def translate(self, delta):
        self.x += delta[0]
        self.y += delta[1]
