import tkinter as tk
from typing import Set

from block import Block, source, negation, display_block
from connector import Connector
from simulation import Simulation


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

        block1 = source(x=100, y=100)
        self._observed_blocks.add(block1)

        block2 = negation(x=200, y=100)
        self._observed_blocks.add(block2)

        block3 = display_block(x=300, y=100)
        self._observed_blocks.add(block3)

        self._run_button = tk.Button(self.master,
                                     text='Run Simulation',
                                     bg='lightgreen',
                                     relief='flat',
                                     command=self._run_simulation)
        self._run_button.place(x=650, y=550, width=120)

    def _run_simulation(self):
        simulation = Simulation(list(self._observed_blocks))
        simulation.run()
        self._redraw()

    def _on_left_click(self, event):
        clicked_connectors = (b.inside_connector(event) for b in self._observed_blocks)
        clicked_connector = next((c for c in clicked_connectors if c), None)
        if clicked_connector:
            if self._dragging_line_from is None:
                self._dragging_line_from = clicked_connector
            else:
                self._dragging_line_from.connect_with(clicked_connector)
                self._dragging_line_from = None
        else:
            clicked_block = next((b for b in self._observed_blocks if b.contains(event)), None)
            if clicked_block:
                clicked_block.switch()

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

            x, y = block.middle()
            text = block.label()
            self._canvas.create_text(x, y, text=text)

ROOT = tk.Tk()
APP = Application(master=ROOT)
APP.mainloop()
