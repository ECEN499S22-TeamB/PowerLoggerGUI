""""
Tkinter practice
Tutorial link: https://realpython.com/python-gui-tkinter/
Austin Hilderbrand
"""
#
# Building Your First Python GUI Application with Tkinter
#

# # Import Tkinter
# import tkinter as tk

# # Create a new window
# window = tk.Tk()

# # ============ Adding a Widget
# # Add some text to the window
# greeting = tk.Label(text="Hello, Tkinter") # Create a label widget
# greeting.pack() # Add it to the window (one possible way)

# # Wait for user input
# window.mainloop()   # CRITICAL: script won't work without this

# # ========= Check your understanding
# # Exercise: Create a Tkinter window
# # Create a new window
# window = tk.Tk()

# # Add some text to the window
# message = tk.Label(text="Python rocks!")
# message.pack()

# # Wait for user input
# window.mainloop()

#
# Working with Widgets
#

# Imports
import tkinter as tk
import tkinter.ttk as ttk # Themed Tkinter

# # Wildcard imports
# # This will automatically override legacy widgets witih themed ones 
# #     where possible.
# # No longer need to prefix the widget's class name with its 
# #     corresponding Python module. 
# from tkinter import *
# from tkinter.ttk import *

window = tk.Tk()

# # ===== Displaying Text and Images With Label Widgets
# # # Changing text colors
# # label = Label(
# #     text="Hello, Tkinter",
# #     foreground="white",  # Set the text color to white
# #     background="black"  # Set the background color to black
# # )

# # Another example, also change label width and height
# label = tk.Label(
#     text="Hello, Tkinter",
#     fg="Chartreuse",
#     bg="#191970",
#     width=10,
#     height=10
# )

# label.pack()

# # ========= Displaying Clickable Buttons With Button Widgets
# button = tk.Button(
#     text="Click me!",
#     width=25,
#     height=5,
#     bg="blue",
#     fg="yellow",
# )

# # button.pack()

# # ========= Gettting User Input With Entry Widgets
# # Creates a widget with a blue background, some yellow text, and a width of 50 text units
# entry = tk.Entry(fg="yellow", bg="blue", width=50)
# entry.pack()

# # NOTE: The remainder of this section was done in Python shell

# ========== Getting Multiline User Input With Text Widgets
# NOTE: This entire section was done in Python shell

# # ========== Assigning Widgets to Frames With Frame Widgets
# Creates a frame and assigns it to the main application window
# (Will be empty)
# frame = tk.Frame()
# frame.pack()

# # Create two frame widgets, each with a label
# frame_a = tk.Frame()
# frame_b = tk.Frame()

# label_a = tk.Label(master=frame_a, text="I'm in Frame A")
# label_a.pack()

# label_b = tk.Label(master=frame_b, text="I'm in Frame B")
# label_b.pack()

# frame_a.pack()
# frame_b.pack()

# ======= Adjusting Frame Appearances With Reliefs


# Wait for user input
window.mainloop()