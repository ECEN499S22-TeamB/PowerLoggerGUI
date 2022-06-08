"""
project_window.py
This script launches a new data collection window. 
Author: Austin Hilderbrand
"""

# ============= Imports
import tkinter as tk
from tkinter import messagebox


# ============= Globals
# Create a new window
window = tk.Tk()


# ============= Event handlers
#
# donothing
#
def donothing():
    """Test function that does nothing."""
    messagebox.showinfo('Nothing', 'No function.')


# ============= Setup visuals
def setup():
    # Configure the window
    window.title("Power Logger: Project Window")


# # ============= Run setup and enter event loop
if __name__ == '__main__':
    setup()
    window.mainloop()