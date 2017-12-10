import tkinter as tk
from typing import List

from block import Block


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self._observed_blocks : List[Block] = []

        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.master.title("Logic Gate Simulation")

        self.master.maxsize(800, 600)
        self.master.minsize(800, 600)

        self._canvas = tk.Canvas(self.master, width=800, height=600)
        self._canvas.bind("<Button-1>", self.on_click)
        self._canvas.pack()

        block1 = Block(50, 100, name="Block #1")
        self.add_block(block1)

        block2 = Block(200, 150, name="Block #2")
        self.add_block(block2)

    def add_block(self, block: Block):
        self._canvas.create_rectangle(*block.rect())
        self._observed_blocks.append(block)

    def on_click(self, event):
        clicked_block = next((b for b in self._observed_blocks if b.contains(event)), None)
        if clicked_block:
            clicked_block.notify()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
