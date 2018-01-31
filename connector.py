from typing import Set

from rectangle import Rectangle


class Connector(Rectangle):
    WIDTH = 20
    HEIGHT = 20

    def __init__(self, x, y):
        super().__init__(x, y, self.WIDTH, self.HEIGHT)

        self.connections: Set['Connector'] = set()
        self._x, self._y = x, y

        self.value = None

    def notify(self):
        pass

    def connect_with(self, other: 'Connector'):
        self.connections.add(other)

    def push(self, value):
        self.value = value
        for c in self.connections:
            c.push(self.value)
