import tkinter as tk
from tkinter import Menu

from blades_util.ui.model import Model


class Output:
    def __init__(self, m: Model, r: tk.Tk):
        self.menu = None
        self.text_area = None
        self.model = m
        self.root = r
        self.build_ui()
        self.model.set_output_holder(self.update_output)

    def update_output(self, output_list: list[str]):
        self.text_area.delete("1.0", tk.END)  # Clear the text area
        for line in output_list:
            self.text_area.insert(tk.END, line + "\n")  # Add each line

    def build_ui(self):
        self.text_area = tk.Text(self.root, wrap="word")  # Create a text widget
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Right-click context menu
        self.menu = Menu(self.root, tearoff=0)
        self.menu.add_command(label="Copy All", command=self.copy_to_clipboard)

        self.text_area.bind("<Button-3>", self.show_context_menu)  # Bind right-click

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_area.get("1.0", tk.END))

    def show_context_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()


if __name__ == '__main__':
    root = tk.Tk()
    output = Output(Model(), root)
    root.mainloop()
