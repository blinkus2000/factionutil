import tkinter as tk
from tkinter import ttk

from blades_util.controller import Controller
from blades_util.ui.model import Model
from blades_util.utils import convert_dict


class Table:
    def __init__(self, c: Controller, m: Model, r: tk.Frame):
        super().__init__()
        self.combobox = None
        self.style = None
        self.faction_tuple = None
        self.factions = None
        self.frame = r
        self.controller = c
        self.model = m

        self.name = None
        self.dict_data = None

        self.frame.tree = None
        self.vsb = None
        nm, mgr = self.controller.generate_new_manager()
        self.create_table_from_data(nm, mgr)
        self.model.set_current_manager_holder(self.create_table_from_data)

    def create_table_from_data(self, name: str, manager_data: dict[tuple[str, str], float]):
        self.name = name
        self.dict_data = manager_data
        self.factions = convert_dict(self.dict_data, first_str="The Players")
        self.faction_tuple = tuple(self.factions)
        self.style = ttk.Style(self.frame)
        self.style.configure("Treeview.Heading", font=('Helvetica', 8))  # Set a smaller font size
        self.create_table()

    def create_table(self):
        if self.frame.tree is not None:
            # Clear the existing treeview
            for i in self.frame.tree.get_children():
                self.frame.tree.delete(i)
        else:
            self.combobox: ttk.Combobox = ttk.Combobox(self.frame)
            self.combobox['values'] = self.faction_tuple
            self.combobox.bind('<<ComboboxSelected>>', self.on_combo_select)
            self.combobox.pack(side='left', fill='x', expand=False)
            # Treeview has not been created yet, so create it
            self.frame.tree = ttk.Treeview(self.frame)
            # Create a vertical scrollbar
            self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.frame.tree.yview)
            self.frame.tree.configure(yscrollcommand=self.vsb.set)
            # Pack the treeview and the scrollbar
            self.vsb.pack(side='right', fill='y')
            # Create a horizontal scrollbar
            self.combobox.current(0)
        self.build_tree_view()

    def build_tree_view(self):
        selected_faction: str = self.combobox.get()
        # Define columns
        faction_tuple = ('faction_name', 'their_status_with_you', 'your_status_with_them')
        faction_name, their_status_with_you, your_status_with_them = faction_tuple
        self.frame.tree['columns'] = faction_tuple
        # Format columns
        self.frame.tree.column("#0", width=0, stretch=tk.NO)

        self.frame.tree.column(faction_name, anchor=tk.W, width=100, stretch=tk.NO)
        # Create headings
        self.frame.tree.heading("#0", text="", anchor=tk.W)
        self.frame.tree.heading(faction_name, text="Faction Name", anchor=tk.W)

        self.frame.tree.heading(their_status_with_you, text=f'Their Status With {selected_faction}', anchor=tk.CENTER)
        self.frame.tree.column(their_status_with_you, width=100, anchor=tk.CENTER)

        self.frame.tree.heading(your_status_with_them, text=f'{selected_faction} Status With Them', anchor=tk.CENTER)
        self.frame.tree.column(your_status_with_them, width=100, anchor=tk.CENTER)

        # if the faction str == "The Players" I would like to set the background of that cell to be orange
        # Add data to the treeview
        the_table = self.dict_data

        for faction_row in self.factions:
            row = (faction_row, the_table[selected_faction][faction_row], the_table[faction_row][selected_faction])
            self.frame.tree.insert("", tk.END, values=row)
            # if the faction str == "The Players" I would like to set the background of that cell to be orange
        self.frame.tree.pack(side='left', fill='both', expand=True)
        self.frame.tree.bind('<<TreeviewSelect>>', self.on_select)

    def on_select(self, event):
        pass
        # The event object will contain information about the selection
        # selected_items = self.frame.tree.selection()  # This returns the selected items' IDs
        # for item_id in selected_items:
        #    item = self.frame.tree.item(item_id)
        #    self.model.set_selected(item['values'][0])

    def on_combo_select(self, event):
        self.model.set_selected(self.combobox.get())
        self.create_table()


if __name__ == "__main__":
    root = tk.Tk()
    f = tk.Frame(root)
    f.pack(fill=tk.BOTH, expand=True)
    Table(Controller(), Model(), f)
    root.mainloop()
