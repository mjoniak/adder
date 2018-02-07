import collections

import block
import components
from simulation import Simulation


class Controller:
    def __init__(self, view):
        self._view = view

        self.observed_blocks = set()
        self.dragging_line_from = None
        self._dragging_pos = None
        self.bounding_box = None
        self._selected_block = None

        self._init_board()

        self.block_constructors = {
            "Source": block.source,
            "NOT Block": block.negation,
            "AND Block": block.conjunction,
            "OR Block": block.alternative,
            "XOR Block": block.xor,
            "NAND Block": block.nand,
            "NOR Block": block.nor,
            "Display": block.display_block,
            "RS Flip-flop": components.rs_flip_flop
        }

    def clicked_on_board(self, event):
        clicked_connectors = (b.inside_connector(event) for b in self.observed_blocks)
        clicked_connector = next((c for c in clicked_connectors if c), None)
        if clicked_connector:
            self._clicked_on_connector(clicked_connector)
        else:
            clicked_block = next((b for b in self.observed_blocks if b.contains(event)), None)
            if clicked_block is not None:
                self._clicked_on_block(clicked_block)
            else:
                self._unclick_block()

        self._view.redraw()

    def _clicked_on_block(self, clicked_block: block.Block):
        if self._selected_block is clicked_block:
            clicked_block.switch()

        self._selected_block = clicked_block
        self._calculate_bounding_box()
        self._view.redraw()

    def _unclick_block(self):
        self._selected_block = None
        self.bounding_box = None

    def _calculate_bounding_box(self):
        box = self._selected_block.rect()
        self.bounding_box = (box[0] - 10, box[1] - 10, box[2] + 10, box[3] + 10)

    def _clicked_on_connector(self, connector):
        if self.dragging_line_from is None:
            self.dragging_line_from = connector
        else:
            self.dragging_line_from.connect_with(connector)
            self.dragging_line_from = None

    def cancel_dragging(self):
        self.dragging_line_from = None
        self._view.redraw()

    def run_simulation(self):
        simulation = Simulation(list(self.observed_blocks))
        simulation.run()
        self._view.redraw()

    def tool_selected(self, tool_name):
        constructor = self.block_constructors[tool_name]
        constructed = constructor(x=100, y=100)
        if isinstance(constructed, collections.Iterable):
            self.observed_blocks.update(constructed)
        else:
            self.observed_blocks.add(constructed)
        self._view.redraw()

    def drag_selected_block(self, position):
        if self._selected_block is not None:
            delta = position.x - self._selected_block.x, position.y - self._selected_block.y
            self._selected_block.translate(delta)
            self._calculate_bounding_box()
        self._view.redraw()

    def _init_board(self):
        # block1 = source(x=100, y=100)
        # self.observed_blocks.add(block1)
        #
        # block2 = negation(x=200, y=100)
        # self.observed_blocks.add(block2)
        #
        # block3 = display_block(x=300, y=100)
        # self.observed_blocks.add(block3)
        pass
