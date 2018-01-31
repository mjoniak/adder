from collections import namedtuple
from unittest import TestCase

from block import Block, source, negation, alternative, conjunction, nand, nor, xor

Point = namedtuple('Point', ['x', 'y'])


class ConnectorTest(TestCase):
    def test_inside_connector_no_connectors(self):
        block = Block(0, 0, input_connectors_n=0, output_connectors_n=0)
        conn = block.inside_connector(Point(0, 0))
        self.assertIsNone(conn)

    def test_inside_connector_input(self):
        block = Block(0, 0, input_connectors_n=1, output_connectors_n=0)
        left_middle = Point(0, Block.HEIGHT / 2)
        conn = block.inside_connector(left_middle)
        self.assertTrue(conn.contains(left_middle))

    def test_inside_connector_output(self):
        block = source()
        right_middle = Point(Block.WIDTH, Block.HEIGHT / 2)
        conn = block.inside_connector(right_middle)
        self.assertTrue(conn.contains(right_middle))

    def test_source_block_pushes_signal(self):
        source_block = source()
        source_block.push()
        self.assertEqual(1, source_block.outputs[0].value)

    def test_connector_pushes_to_next(self):
        source_block = source()
        second_block = Block(0, 0, input_connectors_n=1, output_connectors_n=0)
        source_block.outputs[0].connect_with(second_block.inputs[0])

        source_block.push()

        for c2 in second_block.inputs:
            self.assertEqual(1, c2.value)

    def test_negation(self):
        source_block = source(0)
        not_block = negation()
        source_block.outputs[0].connect_with(not_block.inputs[0])
        source_block.push()
        not_block.push()
        self.assertEqual(1, not_block.outputs[0].value)

    def test_alternative(self):
        self.assertEqual(0, test_block(0, 0, alternative))
        self.assertEqual(1, test_block(1, 0, alternative))
        self.assertEqual(1, test_block(0, 1, alternative))
        self.assertEqual(1, test_block(1, 1, alternative))

    def test_conjunction(self):
        self.assertEqual(0, test_block(0, 0, conjunction))
        self.assertEqual(0, test_block(1, 0, conjunction))
        self.assertEqual(0, test_block(0, 1, conjunction))
        self.assertEqual(1, test_block(1, 1, conjunction))

    def test_nand(self):
        self.assertEqual(1, test_block(0, 0, nand))
        self.assertEqual(1, test_block(1, 0, nand))
        self.assertEqual(1, test_block(0, 1, nand))
        self.assertEqual(0, test_block(1, 1, nand))

    def test_nor(self):
        self.assertEqual(1, test_block(0, 0, nor))
        self.assertEqual(0, test_block(1, 0, nor))
        self.assertEqual(0, test_block(0, 1, nor))
        self.assertEqual(0, test_block(1, 1, nor))

    def test_xor(self):
        self.assertEqual(0, test_block(0, 0, xor))
        self.assertEqual(1, test_block(1, 0, xor))
        self.assertEqual(1, test_block(0, 1, xor))
        self.assertEqual(0, test_block(1, 1, xor))


def test_block(first_input, second_input, block_factory) -> int:
    first_source_block = source(value=first_input)
    second_source_block = source(value=second_input)
    block = block_factory()
    first_source_block.outputs[0].connect_with(block.inputs[0])
    second_source_block.outputs[0].connect_with(block.inputs[1])
    first_source_block.push()
    second_source_block.push()
    block.push()

    return block.outputs[0].value
