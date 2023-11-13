import tkinter as tk
from blades_util.controller import Controller
from blades_util.ui.managers import Managers
from blades_util.ui.model import Model
from blades_util.ui.output import Output
from blades_util.ui.table import Table
from blades_util.ui.buttons import Buttons

if __name__ == '__main__':
    c = Controller()
    managers = c.get_available_managers()
    m = Model()
    m.update_managers(managers)
    root = tk.Tk()

    # Top frame for the table
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X, expand=False)
    Table(c, m, top_frame)

    # Bottom frame to hold other frames
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Frame for buttons on the far lower left
    far_lower_left_frame = tk.Frame(bottom_frame)
    far_lower_left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    Buttons(c, m, far_lower_left_frame)

    # Frame for managers next to the buttons
    next_lower_left_frame = tk.Frame(bottom_frame)
    next_lower_left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    Managers(m, next_lower_left_frame)

    # Frame to fill the rest of the bottom space with the output
    fill_the_rest_of_the_bottom = tk.Frame(bottom_frame)
    fill_the_rest_of_the_bottom.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    Output(m, fill_the_rest_of_the_bottom)

    root.mainloop()
