import tkinter as tk

from controller import Controller


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self._controller = Controller(self)

        self.pack()
        self._create_widgets()

        self.redraw()

    def _create_widgets(self):
        self.master.title("Logic Gate Simulation")

        self.master.minsize(800, 600)
        self.master.maxsize(800, 600)

        self._canvas = tk.Canvas(self, width=650, height=600)
        self._canvas.bind("<Button-1>", self._controller.clicked_on_board)
        self._canvas.bind("<Button-3>", lambda _: self._controller.cancel_dragging())
        self._canvas.bind("<Motion>", self._on_motion)
        self._canvas.bind("<B1-Motion>", self._controller.drag_selected_block)
        self._canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        self._run_button = tk.Button(self.master,
                                     text='Run Simulation',
                                     bg='lightgreen',
                                     relief='flat',
                                     command=self._controller.run_simulation)
        self._run_button.place(x=650, y=550, width=120)

        toolbox = tk.Listbox(self, width=150)
        toolbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        toolbox.bind('<Double-Button-1>', self._tool_selected)

        for block_name in self._controller.block_constructors.keys():
            toolbox.insert(tk.END, block_name)

    def _on_motion(self, event):
        self._mouse_pos = event
        self.redraw()

    def _tool_selected(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self._controller.tool_selected(value)

    def redraw(self):
        self._canvas.delete("all")

        all_blocks = self._controller.observed_blocks
        line_from = self._controller.dragging_line_from
        bounding_box = self._controller.bounding_box

        if line_from is not None and self._mouse_pos is not None:
            self._canvas.create_line(*line_from.middle(),
                                     self._mouse_pos.x, self._mouse_pos.y)

        for block in all_blocks:
            for connector in block.connectors:
                for connected in connector.connections:
                    self._canvas.create_line(*connector.middle(), *connected.middle())

        for block in all_blocks:
            self._canvas.create_rectangle(*block.rect())
            for connector in block.connectors:
                self._canvas.create_rectangle(*connector.rect())

            x, y = block.middle()
            text = block.label()
            self._canvas.create_text(x, y, text=text)

        if bounding_box is not None:
            self._canvas.create_rectangle(bounding_box, outline='blue', dash=(3,5))

ROOT = tk.Tk()
APP = Application(master=ROOT)
APP.mainloop()
