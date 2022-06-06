"""
main_menu.py
This script will launch the Power Logger main menu.
Author: Austin Hilderbrand
"""

# ============= Imports
import tkinter as tk
from random import randint
from tkinter import messagebox

# ============= Event handlers


# ============= Setup visuals
# Create a new window
window = tk.Tk()
window.title("Power Logger")

# Configure the window
window.columnconfigure(0, minsize=300, weight=1)
window.columnconfigure(1, minsize=300, weight=1)
window.rowconfigure(0, minsize=100, weight=1)
window.rowconfigure(1, minsize=100, weight=1)

# Create widgets
btn_new = tk.Button(window, text="New Project", relief=tk.RIDGE, borderwidth=10)
btn_load = tk.Button(window, text="Load Project", relief=tk.RIDGE, borderwidth=10)
btn_settings = tk.Button(window, text="System Settings", relief=tk.RIDGE, borderwidth=10)
btn_quit = tk.Button(window, text="Quit", relief=tk.RIDGE, borderwidth=10)

# Setup window grid layout
btn_new.grid(row=0, column=0, sticky="nsew")
btn_load.grid(row=0, column=1, sticky="nsew")
btn_settings.grid(row=1, column=0, sticky="nsew")
btn_quit.grid(row=1, column=1, sticky="nsew")

# ============= Run the event loop
window.mainloop()