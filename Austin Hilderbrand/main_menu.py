"""
main_menu.py
This script will launch the Power Logger main menu.
Author: Austin Hilderbrand
"""

# ============= Imports
import tkinter as tk
from tkinter import messagebox
import os
import subprocess


# ============= Globals
# Create a new window
window = tk.Tk()
dir_path = os.path.dirname(os.path.realpath(__file__))


# ============= Event handlers
#
# donothing
#
def donothing():
    """Test function that does nothing."""
    messagebox.showinfo('Nothing', 'No function.')

#
# ask_close
#
def ask_close():
    """Confirm the user wants to close the window."""
    if messagebox.askokcancel(
        message="Are you sure you want to close the window?", 
        icon='warning', title="Please confirm."):
        window.destroy()

#
# create_project
#
def create_project():
    """Launch a new project window."""
    subprocess.Popen(['python', dir_path+'\project_window.py']) 
    # TODO: Improve cross-platform compatibility?


# ============= Setup visuals
def setup():
    # Configure the window
    window.title("Power Logger: Main Menu")

    # Configure the window grid
    window.columnconfigure(0, minsize=300, weight=1)
    window.columnconfigure(1, minsize=300, weight=1)
    window.rowconfigure(0, minsize=100, weight=1)
    window.rowconfigure(1, minsize=100, weight=1)

    # Create button widgets
    btn_new = tk.Button(window, text="New Project", relief=tk.RIDGE, borderwidth=10, command=create_project)
    btn_load = tk.Button(window, text="Load Project", relief=tk.RIDGE, borderwidth=10)
    btn_settings = tk.Button(window, text="System Settings", relief=tk.RIDGE, borderwidth=10)
    btn_quit = tk.Button(window, text="Quit", relief=tk.RIDGE, borderwidth=10, command=ask_close)

    # Place button widgets on grid
    btn_new.grid(row=0, column=0, sticky="nsew")
    btn_load.grid(row=0, column=1, sticky="nsew")
    btn_settings.grid(row=1, column=0, sticky="nsew")
    btn_quit.grid(row=1, column=1, sticky="nsew")

    # Create the File menu widget
    menubar = tk.Menu(window)   # Create the menubar
    menu_file = tk.Menu(menubar, tearoff=0)
    menu_file.add_command(label="New", command=donothing)
    menu_file.add_command(label="Open", command=donothing)
    menu_file.add_command(label="Save", command=donothing)
    menu_file.add_separator()
    menu_file.add_command(label="Exit", command=ask_close)
    menubar.add_cascade(label="File", menu=menu_file)

    # Create the Help menu widget
    menu_help = tk.Menu(menubar, tearoff=0)
    menu_help.add_command(label="Help Index", command=donothing)
    menu_help.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=menu_help)

    # Pack the menu widgets
    window['menu'] = menubar

    # Intercept the close button
    window.protocol("WM_DELETE_WINDOW", ask_close)


# ============= Run setup and enter event loop
if __name__ == '__main__':
    setup()
    window.mainloop()