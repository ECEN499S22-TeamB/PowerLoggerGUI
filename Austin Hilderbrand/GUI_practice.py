""""
Tkinter practice
Tutorial link: https://realpython.com/python-gui-tkinter/
Austin Hilderbrand
"""
# ---------------------------------------------------------------------------
# -------- Building Your First Python GUI Application with Tkinter ---------
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# -------------------------- Working with Widgets ---------------------------
# ---------------------------------------------------------------------------

# # Imports
# import tkinter as tk
# import tkinter.ttk as ttk # Themed Tkinter

# # Wildcard imports
# # This will automatically override legacy widgets witih themed ones 
# #     where possible.
# # No longer need to prefix the widget's class name with its 
# #     corresponding Python module. 
# from tkinter import *
# from tkinter.ttk import *

# window = tk.Tk()

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
# # Creates a widget with a blue background, some yellow text, 
# #   and a width of 50 text units
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

# # ======= Adjusting Frame Appearances With Reliefs
# # packs five Frame widgets into a window, each with a different value 
# #   for the relief argument
# border_effects = {
#     "flat": tk.FLAT,
#     "sunken": tk.SUNKEN,
#     "raised": tk.RAISED,
#     "grooved": tk.GROOVE,
#     "ridge": tk.RIDGE
# }

# for relief_name, relief in border_effects.items():
#     frame = tk.Frame(master=window, relief=relief, borderwidth=5)
#     frame.pack(side=tk.LEFT)
#     label = tk.Label(master=frame, text=relief_name)
#     label.pack()

# # ======= Check Your Understanding
# ent = tk.Entry(width=40)
# ent.pack()
# ent.insert(0, "What is your name?")

# # Wait for user input
# window.mainloop()

# ---------------------------------------------------------------------------
# ----------- Controlling Layout with Geometry Managers ---------------------
# ---------------------------------------------------------------------------

# # Imports
# import tkinter as tk

# # Open a new window
# window = tk.Tk()

# # ======== The .pack() Geometry Manager
# # .pack() using defaults
# frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
# frame1.pack()

# frame2 = tk.Frame(master=window, width=50, height=50, bg="yellow")
# frame2.pack()

# frame3 = tk.Frame(master=window, width=25, height=25, bg="blue")
# frame3.pack()

# # Frames fill the window horizontally
# frame1 = tk.Frame(master=window, height=100, bg="red")
# frame1.pack(fill=tk.X)

# frame2 = tk.Frame(master=window, height=50, bg="yellow")
# frame2.pack(fill=tk.X)

# frame3 = tk.Frame(master=window, height=25, bg="blue")
# frame3.pack(fill=tk.X)

# # Frames fill the window vertically
# frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
# frame1.pack(fill=tk.Y, side=tk.LEFT)

# frame2 = tk.Frame(master=window, width=100, bg="yellow")
# frame2.pack(fill=tk.Y, side=tk.LEFT)

# frame3 = tk.Frame(master=window, width=50, bg="blue")
# frame3.pack(fill=tk.Y, side=tk.LEFT)

# # Frames fill the window in both directions (most responsive)
# frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
# frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# frame2 = tk.Frame(master=window, width=100, bg="yellow")
# frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# frame3 = tk.Frame(master=window, width=50, bg="blue")
# frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# # ============ The .place Geometry Manager
# frame = tk.Frame(master=window, width=150, height=150)
# frame.pack()

# label1 = tk.Label(master=frame, text="I'm at (0,0)", bg="red")
# label1.place(x=0, y=0)

# label2 = tk.Label(master=frame, text="I'm at (75, 75)", bg="Yellow")
# label2.place(x=75, y=75)

# =========== The .grid() Geometry Manager
# # Creates a 3x3 grid of frames with label widgets packed into them
# for i in range(3):
#     # Window resizing
#     window.columnconfigure(i, weight=1, minsize=75)
#     window.rowconfigure(i, weight=1, minsize=50)

#     for j in range(3):
#         frame = tk.Frame(
#             master=window,
#             relief=tk.RAISED,
#             borderwidth=5
#         )
#         frame.grid(row=i, column=j, padx=3, pady=3)
#         label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
#         label.pack(padx=3, pady=3)

# # Creates two label widgets and places them in a grid with one column
# #   and two rows
# window.columnconfigure(0, minsize=250)
# window.rowconfigure([0, 1], minsize=100)

# label1 = tk.Label(text="A")
# label1.grid(row=0, column=0, sticky="ne")

# label2 = tk.Label(text="B")
# label2.grid(row=1, column=0, sticky="sw")

# # Different ways to make widgets fill the grid
# window.rowconfigure(0, minsize=50)
# window.columnconfigure([0, 1, 2, 3], minsize=50)

# label1 = tk.Label(text="1", bg="black", fg="white")
# label2 = tk.Label(text="2", bg="black", fg="white")
# label3 = tk.Label(text="3", bg="black", fg="white")
# label4 = tk.Label(text="4", bg="black", fg="white")

# label1.grid(row=0, column=0)
# label2.grid(row=0, column=1, sticky="ew")
# label3.grid(row=0, column=2, sticky="ns")
# label4.grid(row=0, column=3, sticky="nsew")

# ============ Check Your Understanding
# # Solution code (to save time)
# # Create a new window with the title "Address Entry Form"
# window.title("Address Entry Form")

# # Create a new frame `frm_form` to contain the Label
# # and Entry widgets for entering address information
# frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
# # Pack the frame into the window
# frm_form.pack()

# # Create the Label and Entry widgets for "First Name"
# lbl_first_name = tk.Label(master=frm_form, text="First Name:")
# ent_first_name = tk.Entry(master=frm_form, width=50)
# # Use the grid geometry manager to place the Label and
# # Entry widgets in the first and second columns of the 
# # first row of the grid 
# lbl_first_name.grid(row=0, column=0, sticky="e")
# ent_first_name.grid(row=0, column=1)

# # Create the Label and Entry widgets for "Last Name"
# lbl_last_name = tk.Label(master=frm_form, text="Last Name:")
# ent_last_name = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the second row of the grid
# lbl_last_name.grid(row=1, column=0, sticky="e")
# ent_last_name.grid(row=1, column=1)

# # Create the Label and Entry widgets for "Address Line 1"
# lbl_address1 = tk.Label(master=frm_form, text="Address Line 1:")
# ent_address1 = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the third row of the grid
# lbl_address1.grid(row=2, column=0, sticky="e")
# ent_address1.grid(row=2, column=1)

# # Create the Label and Entry widgets for "Address Line 2"
# lbl_address2 = tk.Label(master=frm_form, text="Address Line 2:")
# ent_address2 = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the fourth row of the grid
# lbl_address2.grid(row=3, column=0, sticky=tk.E)
# ent_address2.grid(row=3, column=1)

# # Create the Label and Entry widgets for "City"
# lbl_city = tk.Label(master=frm_form, text="City:")
# ent_city = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the fifth row of the grid
# lbl_city.grid(row=4, column=0, sticky=tk.E)
# ent_city.grid(row=4, column=1)

# # Create the Label and Entry widgets for "State/Province"
# lbl_state = tk.Label(master=frm_form, text="State/Province:")
# ent_state = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the sixth row of the grid
# lbl_state.grid(row=5, column=0, sticky=tk.E)
# ent_state.grid(row=5, column=1)

# # Create the Label and Entry widgets for "Postal Code"
# lbl_postal_code = tk.Label(master=frm_form, text="Postal Code:")
# ent_postal_code = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the seventh row of the grid
# lbl_postal_code.grid(row=6, column=0, sticky=tk.E)
# ent_postal_code.grid(row=6, column=1)

# # Create the Label and Entry widgets for "Country"
# lbl_country = tk.Label(master=frm_form, text="Country:")
# ent_country = tk.Entry(master=frm_form, width=50)
# # Place the widgets in the eight row of the grid
# lbl_country.grid(row=7, column=0, sticky=tk.E)
# ent_country.grid(row=7, column=1)

# # Create a new frame `frm_buttons` to contain the
# # Submit and Clear buttons. This frame fills the
# # whole window in the horizontal direction and has
# # 5 pixels of horizontal and vertical padding.
# frm_buttons = tk.Frame()
# frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

# # Create the "Submit" button and pack it to the
# # right side of `frm_buttons`
# btn_submit = tk.Button(master=frm_buttons, text="Submit")
# btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

# # Create the "Clear" button and pack it to the
# # right side of `frm_buttons`
# btn_clear = tk.Button(master=frm_buttons, text="Clear")
# btn_clear.pack(side=tk.RIGHT, ipadx=10)

# # SHORTENED FORM
# # Create a new window with the title "Address Entry Form"
# window.title("Address Entry Form")

# # Create a new frame `frm_form` to contain the Label
# # and Entry widgets for entering address information
# frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
# # Pack the frame into the window
# frm_form.pack()

# # List of field labels
# labels = [
#     "First Name:",
#     "Last Name:",
#     "Address Line 1:",
#     "Address Line 2:",
#     "City:",
#     "State/Province:",
#     "Postal Code:",
#     "Country:",
# ]

# # Loop over the list of field labels
# for idx, text in enumerate(labels):
#     # Create a Label widget with the text from the labels list
#     label = tk.Label(master=frm_form, text=text)
#     # Create an Entry widget
#     entry = tk.Entry(master=frm_form, width=50)
#     # Use the grid geometry manager to place the Label and
#     # Entry widgets in the row whose index is idx
#     label.grid(row=idx, column=0, sticky="e")
#     entry.grid(row=idx, column=1)

# # Create a new frame `frm_buttons` to contain the
# # Submit and Clear buttons. This frame fills the
# # whole window in the horizontal direction and has
# # 5 pixels of horizontal and vertical padding.
# frm_buttons = tk.Frame()
# frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

# # Create the "Submit" button and pack it to the
# # right side of `frm_buttons`
# btn_submit = tk.Button(master=frm_buttons, text="Submit")
# btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

# # Create the "Clear" button and pack it to the
# # right side of `frm_buttons`
# btn_clear = tk.Button(master=frm_buttons, text="Clear")
# btn_clear.pack(side=tk.RIGHT, ipadx=10)

# # Keep window open
# window.mainloop()

# ---------------------------------------------------------------------------
# ----------------- Making Your Applications Interactive --------------------
# ---------------------------------------------------------------------------
