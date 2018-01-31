import operator
from itertools import chain
from typing import Optional

from connector import Connector
from rectangle import Rectangle


class Block(Rectangle):
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, x, y, input_connectors_n, output_connectors_n, get_value=None):
        super().__init__(x, y, self.WIDTH, self.HEIGHT)
        self._add_input(input_connectors_n)
        self._add_output(output_connectors_n)
        self._get_value = get_value

    def _add_input(self, input_connectors_n: int):
        separator = self._calculate_separator(input_connectors_n)
        self.inputs = [self._ith_connector(i, separator, self.x) for i in range(input_connectors_n)]

    def _add_output(self, output_connectors_n: int):
        separator = self._calculate_separator(output_connectors_n)
        self.outputs = [self._ith_connector(i, separator, self.x + self.width) for i in range(output_connectors_n)]

    def _calculate_separator(self, input_connectors_n: int):
        return (self.height - input_connectors_n * Connector.WIDTH) / (input_connectors_n + 1)

    def _ith_connector(self, i: int, separator: int, x: int):
        return Connector(x - Connector.WIDTH / 2, self.y + (i + 1) * separator + i * Connector.WIDTH)

    def inside_connector(self, position) -> Optional[Connector]:
        for connector in self.connectors:
            if connector.contains(position):
                return connector
        return None

    @property
    def connectors(self):
        return chain(self.inputs, self.outputs)

    def push(self):
        for c in self.outputs:
            c.push(self._get_value(self.inputs))


def source(value=1, x=0, y=0):
    return Block(x, y, input_connectors_n=0, output_connectors_n=1, get_value=lambda _: value)


def negation(x=0, y=0):
    return Block(x, y, input_connectors_n=1, output_connectors_n=1, get_value=lambda inputs: not inputs[0].value)


def alternative(x=0, y=0):
    return double_block(x, y, operator.or_)


def conjunction(x=0, y=0):
    return double_block(x, y, operator.and_)


def nand(x=0, y=0):
    return double_block(x, y, lambda a, b: not (a and b))


def nor(x=0, y=0):
    return double_block(x, y, lambda a, b: not (a or b))


def xor(x=0, y=0):
    return double_block(x, y, operator.xor)


def double_block(x=0, y=0, get_value=lambda _, __: 0):
    return Block(x, y, input_connectors_n=2, output_connectors_n=1,
                 get_value=lambda inputs: get_value(inputs[0].value, inputs[1].value))
