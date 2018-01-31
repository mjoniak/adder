import tkinter as tk
from typing import Set

from block import Block
from connector import Connector


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self._observed_blocks: Set[Block] = set()
        self._dragging_line_from: Connector = None

        self._create_widgets()
        self.pack()

        self._dragging_pos = None

        self._redraw()

    def _create_widgets(self):
        self.master.title("Logic Gate Simulation")

        self.master.maxsize(800, 600)
        self.master.minsize(800, 600)

        self._canvas = tk.Canvas(self.master, width=800, height=600)
        self._canvas.bind("<Button-1>", self._on_left_click)
        self._canvas.bind("<Button-3>", self._on_right_click)
        self._canvas.bind("<Motion>", self._on_motion)
        self._canvas.pack()

        block1 = Block(50, 100, 2, 1)
        self._observed_blocks.add(block1)

        block2 = Block(200, 150, 1, 1)
        self._observed_blocks.add(block2)

    def _on_left_click(self, event):
        clicked_connectors = (b.inside_connector(event) for b in self._observed_blocks)
        clicked = next((c for c in clicked_connectors if c), None)
        if clicked:
            if self._dragging_line_from is None:
                self._dragging_line_from = clicked
            else:
                self._dragging_line_from.connect_with(clicked)
                self._dragging_line_from = None

        self._redraw()

    def _on_right_click(self, _):
        self._dragging_line_from = None
        self._redraw()

    def _on_motion(self, event):
        self._dragging_pos = event
        self._redraw()

    def _redraw(self):
        self._canvas.delete("all")

        if self._dragging_line_from is not None and self._dragging_pos is not None:
            self._canvas.create_line(*self._dragging_line_from.middle(),
                                     self._dragging_pos.x, self._dragging_pos.y)

        for block in self._observed_blocks:
            for connector in block.connectors:
                for connected in connector.connections:
                    self._canvas.create_line(*connector.middle(), *connected.middle())

        for block in self._observed_blocks:
            self._canvas.create_rectangle(*block.rect())
            for connector in block.connectors:
                self._canvas.create_rectangle(*connector.rect())


ROOT = tk.Tk()
APP = Application(master=ROOT)
APP.mainloop()
