import tkinter as tk

from blades_util.ui.controller import Controller
from blades_util.ui.model import Model


class Buttons:


    def __init__(self, c: Controller,m: Model, r: tk.Tk):
        self.root = r
        self.controller = c
        self.model = m

    def build_buttons(self):
        button_save = tk.Button(self.root, text="Save", command=self.handle_save)
        button_save.pack(side=tk.TOP, fill=tk.X)

        button_save_as = tk.Button(self.root, text="Save As", command=self.handle_save_as)
        button_save_as.pack(side=tk.TOP, fill=tk.X)

        button_act_on_selected = tk.Button(self.root, text="Act On Selected", command=self.handle_act_on_selected)
        button_act_on_selected.pack(side=tk.TOP, fill=tk.X)

        button_regenerate = tk.Button(self.root, text="Regenerate", command=self.handle_regenerate)
        button_regenerate.pack(side=tk.TOP, fill=tk.X)

        button_advance_week = tk.Button(self.root, text="Advance Week", command=self.handle_advance_week)
        button_advance_week.pack(side=tk.TOP, fill=tk.X)

    def handle_save(self):
        self.controller.save_manager()

    def handle_save_as(self):
        new_manager_name = None  # give me a popup for a string input
        self.controller.save_manager_as(new_manager_name)

    def handle_act_on_selected(self):
        print("Act On Selected button pressed")

    def handle_regenerate(self):
        self.model.update_current_manager(self.controller.generate_new_manager())

    def handle_advance_week(self):
        self.model.update_current_manager(name=None,
                                          factions= self.controller.advance_one_week())


root = tk.Tk()

if __name__ == "__main__":
    app = tk.Tk()
    Buttons(Controller(), Model(), app)
    app.mainloop()
