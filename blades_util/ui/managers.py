import tkinter as tk

from tkinter import Listbox
from blades_util.ui.model import Model


class Managers:
    def __init__(self, m: Model, r: tk.Frame):
        self.model = m
        self.root = r
        self.current_list = []
        self.listbox = None
        self.build_ui()
        self.model.set_manager_list_updater(self.update_new_managers)

    def update_new_managers(self, in_managers: list[str]):
        self.current_list = in_managers
        self.listbox.delete(0, tk.END)  # Clear existing list
        for manager in in_managers:
            self.listbox.insert(tk.END, manager)  # Add new managers

    def on_selected(self, event):
        selection = self.listbox.curselection()
        if selection:
            selected_manager = self.listbox.get(selection[0])
            self.model.set_selected_manager(selected_manager)

    def build_ui(self):
        self.listbox = Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_selected)


if __name__ == '__main__':
    root = tk.Tk()
    f = tk.Frame(root)
    f.pack(fill=tk.BOTH, expand=True)
    managers = Managers(Model(), f)
    root.mainloop()
