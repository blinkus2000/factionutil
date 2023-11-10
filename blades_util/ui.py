import tkinter as tk
from tkinter import ttk

from blades_util.controller import Controller


class FactionManagerUI(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.generate_new_manager()
        self.title('Faction Manager')
        self.create_widgets()

    def create_widgets(self):
        # Create the grid view
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.grid(row=0, column=1, sticky='nsew')

        # Create the output console
        self.console = tk.Text(self, height=10)
        self.console.grid(row=1, column=0, columnspan=2, sticky='nsew')

        # Create the input area with buttons
        self.input_frame = ttk.Frame(self)
        self.input_frame.grid(row=0, column=0, sticky='ns')

        # Buttons
        self.save_button = ttk.Button(self.input_frame, text='Save', command=self.save)
        self.save_button.pack(fill='x')

        self.save_as_button = ttk.Button(self.input_frame, text='Save As', command=self.save_as)
        self.save_as_button.pack(fill='x')

        self.generate_new_button = ttk.Button(self.input_frame, text='Generate New', command=self.generate_new)
        self.generate_new_button.pack(fill='x')

        self.advance_week_button = ttk.Button(self.input_frame, text='Advance One Week', command=self.advance_week)
        self.advance_week_button.pack(fill='x')

        # Manager selection list
        self.manager_listbox = tk.Listbox(self.input_frame)
        self.manager_listbox.pack(fill='both', expand=True)
        self.populate_manager_list()

        # Bind listbox selection event
        self.manager_listbox.bind('<<ListboxSelect>>', self.on_manager_select)

    def populate_manager_list(self):
        managers = self.controller.get_available_managers()
        for manager in managers:
            self.manager_listbox.insert(tk.END, manager)

    def on_manager_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            manager_name = event.widget.get(index)
            self.load_manager(manager_name)

    def save(self):
        self.controller.save_manager()
        self.console.insert(tk.END, "Manager saved.\n")

    def save_as(self):
        # This would open a dialog to input the name
        name = 'NewName'  # Replace with dialog result
        self.controller.save_manager_as(name)
        self.populate_manager_list()
        self.console.insert(tk.END, f"Manager saved as {name}.\n")

    def generate_new(self):
        self.controller.generate_new_manager()
        self.populate_manager_list()
        self.console.insert(tk.END, "New manager generated.\n")

    def advance_week(self):
        results, _ = self.controller.advance_one_week()
        for result in results:
            self.console.insert(tk.END, f"{result}\n")

    def load_manager(self, manager_name):
        self.controller.load_manager(manager_name)
        self.console.insert(tk.END, f"Manager {manager_name} loaded.\n")

    # Add more methods to handle UI events and update the grid and console

if __name__ == "__main__":
    controller = Controller()  # You would pass an actual controller instance here
    app = FactionManagerUI(controller)
    app.mainloop()
