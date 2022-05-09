""""
Tkinter practice
Austin Hilderbrand
"""
# Setup visuals --------------------------------------------------------------
# Import Tkinter
import tkinter as tk

# Create a new window
window = tk.Tk()

# Add some text to the window
greeting = tk.Label(text="Hello, Tkinter") # Create a label widget
greeting.pack() # Add it to the window (one possible way)
# ----------------------------------------------------------------------------


# Wait for user input --------------------------------------------------------
window.mainloop()   # CRITICAL: script won't work without this
# ----------------------------------------------------------------------------