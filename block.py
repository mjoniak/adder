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

    def _ith_connector(self, i: int, separator: int, x: int) -> Connector:
        return Connector(x - Connector.WIDTH / 2, self.y + (i + 1) * separator + i * Connector.WIDTH, self)

    def inside_connector(self, position) -> Optional[Connector]:
        for connector in self.connectors:
            if connector.contains(position):
                return connector
        return None

    @property
    def connectors(self):
        return chain(self.inputs, self.outputs)

    def count_undefined_inputs(self):
        return sum(c.value is None for c in self.inputs)

    def push(self):
        for c in self.outputs:
            c.push(self._get_value(self.inputs))

    def switch(self, value=None):
        # TODO: separate source, display and logic blocks
        value = value if value is not None else not self.outputs[0].value
        self.outputs[0].value = value
        self._get_value = lambda _: value

    def label(self):
        connector = next(self.connectors)
        return connector.value


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


def display_block(x=0, y=0):
    return Block(x=x, y=y, input_connectors_n=1, output_connectors_n=0)


def double_block(x=0, y=0, get_value=lambda _, __: 0):
    return Block(x, y, input_connectors_n=2, output_connectors_n=1,
                 get_value=lambda inputs: (
                     (inputs[0].value is not None
                      or inputs[1].value is not None)
                     and get_value(inputs[0].value, inputs[1].value)))


def operator_of(op, *args) -> Block:
    operator_block = op()
    for block, connector in zip(args, operator_block.inputs):
        block.outputs[0].connect_with(connector)
    return operator_block
