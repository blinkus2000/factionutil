import tkinter as tk
import tkinter.simpledialog as diag
import tkinter.messagebox as msg
from blades_util.controller import Controller
from blades_util.ui.model import Model


class Buttons:

    def __init__(self, c: Controller, m: Model, r: tk.Frame):
        self.root = r
        self.controller = c
        self.model = m
        self.build_buttons()

    def build_buttons(self):
        button_save = tk.Button(self.root, text="Save", command=self.handle_save)
        button_save.pack(side=tk.TOP, fill=tk.X)

        button_save_as = tk.Button(self.root, text="Save As", command=self.handle_save_as)
        button_save_as.pack(side=tk.TOP, fill=tk.X)

        button_save_as = tk.Button(self.root, text="Load", command=self.handle_load)
        button_save_as.pack(side=tk.TOP, fill=tk.X)

        button_act_on_selected = tk.Button(self.root, text="Act On Selected", command=self.handle_act_on_selected)
        button_act_on_selected.pack(side=tk.TOP, fill=tk.X)

        button_regenerate = tk.Button(self.root, text="Regenerate", command=self.handle_regenerate)
        button_regenerate.pack(side=tk.TOP, fill=tk.X)

        button_advance_week = tk.Button(self.root, text="Advance Week", command=self.handle_advance_week)
        button_advance_week.pack(side=tk.TOP, fill=tk.X)

    def handle_save(self):
        self.controller.manager.saved_results = self.model.current_output_list
        self.controller.save_manager()

    def handle_save_as(self):
        # Popup for getting a string input
        new_manager_name = diag.askstring("Input", "Enter New Manager Name:", parent=self.root)
        if new_manager_name:  # Check if the input is not None or empty
            self.controller.save_manager_as(new_manager_name)
            self.model.update_managers(self.controller.get_available_managers())

    def handle_load(self):
        if self.model.selected_manager:
            faction= self.controller.load_manager(self.model.selected_manager)
            self.model.update_current_manager(self.model.selected_manager, faction)
            self.model.current_output(self.controller.manager.saved_results)
        else:
            msg.showerror("No Manager Selected!", "Please Select A Manager")

    def handle_act_on_selected(self):
        faction_str = self.model.get_selected()
        if faction_str:
            # Create a new top-level window
            popup = tk.Toplevel(self.root)
            popup.title("Select Adjustment")
            popup.geometry("200x100")  # Adjust the size as needed

            # Create a Spinbox for integer input
            spinbox = tk.Spinbox(popup, from_=-10, to=10, increment=1, value=0)
            spinbox.pack(pady=10)

            # Function to handle the confirmation
            def on_confirm():
                value = int(spinbox.get())
                if value != 0:
                    faction = self.controller.player_adjust_faction(faction_str, value)
                    self.controller.manager_name
                    self.model.update_current_manager(name=self.controller.manager_name, factions=faction)
                popup.destroy()

            # Confirm button
            confirm_button = tk.Button(popup, text="Confirm", command=on_confirm)
            confirm_button.pack(pady=10)

    def handle_regenerate(self):
        name, factions = self.controller.generate_new_manager()
        self.model.update_current_manager(name, factions)

    def handle_advance_week(self):
        results,table = self.controller.advance_one_week()
        self.model.update_current_manager(name=None,
                                          factions=table)
        self.model.current_output(results)


if __name__ == "__main__":
    root = tk.Tk()
    f = tk.Frame(root)
    f.pack(fill=tk.BOTH, expand=True)
    Buttons(Controller(), Model(), f)
    root.mainloop()
