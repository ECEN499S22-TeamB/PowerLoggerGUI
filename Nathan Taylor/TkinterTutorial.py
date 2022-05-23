"""
Building Your First Python GUI Application With Tkinter
"""
# Import Tkinter library
import tkinter as tk
# Create a window or instance of Tkinter's Tk class
window = tk.Tk()

"""
Adding a Widget
"""
# Create a Label wiget witht he text "Hello, Tkinter" and assign it to a var.
greeting = tk.Label(text="Hello, Tkinter")
# Add the widget to a window
greeting.pack()

window.mainloop()
# Runs Tkinter event loop, listens for events, i.e. buttons or keypresses
# Blocks any code that comes after until window is closed
