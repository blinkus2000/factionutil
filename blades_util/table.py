import tkinter as tk
from tkinter import ttk
from typing import Dict, Tuple

from blades_util.controller import Controller
from blades_util.utils import convert_dict, get_row_as_list


class SimpleTable(tk.Tk):
    def __init__(self, name: str, data: Dict[Tuple[str, str], float]):
        super().__init__()
        self.title(name)
        self.tree = None
        self.dict_data = data
        self.factions = convert_dict(self.dict_data)
        self.faction_tuple = tuple(self.factions)
        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=('Helvetica', 8))  # Set a smaller font size

        self.create_table()

    def create_table(self):
        self.tree = ttk.Treeview(self)

        # Define columns
        faction_tuple = ('faction_name',) + self.faction_tuple
        self.tree['columns'] = faction_tuple

        # Format columns
        self.tree.column("#0", width=0, stretch=tk.YES)
        max_len = max(len(faction) for faction in self.factions)
        self.tree.column("faction_name", anchor=tk.W, width=max_len * 6)

        # Create headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("faction_name", text="Faction Name", anchor=tk.W)
        # Calculate the maximum length of faction names
        # Assuming you have a fixed width for each character and a fixed height for each row
        char_width = 5  # This is an arbitrary number; you'll need to adjust it based on your font
        for faction in self.factions:
            self.tree.heading(faction, text=faction, anchor=tk.CENTER)
            self.tree.column(faction, width=len(faction) * char_width, anchor=tk.CENTER)

        # Add data to the treeview
        for faction in self.factions:
            as_list = get_row_as_list(faction, self.dict_data)
            row = (faction,) + tuple(as_list)
            self.tree.insert("", tk.END, values=row)

            # Create a vertical scrollbar
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # Pack the treeview and the scrollbar
        vsb.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def on_select(self, event):
        # The event object will contain information about the selection
        selected_items = self.tree.selection()  # This returns the selected items' IDs
        for item_id in selected_items:
            item = self.tree.item(item_id)
            print("You selected:", item['values'][0])  # This will print the values of the selected row


if __name__ == "__main__":
    # Example data
    controller: Controller = Controller()
    name, factions = controller.generate_new_manager()
    app = SimpleTable(name, factions)
    app.mainloop()
