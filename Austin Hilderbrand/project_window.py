"""
project_window.py
This script launches a new data collection window. 
Author: Austin Hilderbrand
"""

# ============= Imports
from os import device_encoding
import tkinter as tk
from tkinter import messagebox
import time


# ============= Globals
# Windows
project_window = None
settings_window = None

# Project settings
# TODO: figure out how to get the real values from Project Settings window
device_name = "Device1"
com_port = "COM1"
shunt_resistor = 5  # Ohms
sample_rate = 1     # Hz
flag_trigger = 0.5  # V
# Output strings
settings_details = f"""
    Device Name: \t\t{device_name}\t\t\tFlag Trigger: \u00B1 {flag_trigger} V
    COM Port: \t\t{com_port}
    Shunt Resistor: \t\t{shunt_resistor} \u03A9
    Sample Rate: \t\t{sample_rate} Hz
    """

# Device levels
# TODO: integrate DATAQ code and assign real values
volts = 20
amps = 1

# Flagging
lbx_flags_details = None    # Make this widget global
flags_list = []             # Start with empty list for the listbox
flags_details = None        # Make StringVar type
lbl_flags_beacon = None     # Make this widget global
flag = False

# Readings history
lbx_flags_details = None    # Make 
history_list = []           # Start with empty list for the listbox
history_details = None      # Make StringVar type

# Status
status = "<placeholder>"


# ============= mainloop functions
#
# toggle_flag
#
def toggle_flag():
    """Toggles the flag for testing purposes."""
    global flag # Connect with the global variable
    flag = not flag

#
# flash_beacon
#
def flash_beacon():
    """Enable or disable the flashing beacon."""
    global project_window # Connect to the global variable
    if flag:
        change_color()
    else:
        lbl_flags_beacon.config(bg="white") # If no flag, make bg white
    project_window.after(200, flash_beacon)         # Run every 200 ms

#
# change_color
#
def change_color():
    """Change the color of the flags beacon box."""
    current_color = lbl_flags_beacon.cget("background")
    if current_color == "red":
        next_color = "white"  
    else:
        next_color = "red"
    lbl_flags_beacon.config(background=next_color)

# 
# update_flags_details
#
def update_flags_details(i=0):
    """Update the flags details listbox."""
    global flags_list        # Connect to the global variables
    global flags_details     #
    global lbx_flags_details #
    flags_list.append(f"ERROR{i}\n") # DEBUG
    i += 1 # DEBUG
    if not flags_details:
        flags_details = tk.StringVar(value=flags_list)
    else:
        flags_details.set(flags_list)
    lbx_flags_details['listvariable'] = flags_details # Update the widget
    lbx_flags_details.see("end") # Keep latest output in view
    project_window.after(1000, update_flags_details, i)


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
    global project_window # Connect to the global variable
    if messagebox.askokcancel(
        message="Are you sure you want to close the window?", 
        icon='warning', title="Please confirm."):
        project_window.destroy()

# ============= Setup visuals
#
# setup_project_window
#
def setup_project_window():
    """Setup the Project Window GUI."""
    global project_window       # Connect to the global variable
    project_window = tk.Tk()    # Create a new project window
    # TODO: Redo layout with grid for more robustness?
    # Configure the window -----------------------------
    project_window.title("Power Logger: Project Window")
    project_window.geometry('600x750-10+10')    # Place in upper right screen
    project_window.resizable(False, False)      # Don't make window resizable

    # Intercept the close button
    project_window.protocol("WM_DELETE_WINDOW", ask_close)

    # Create frames ------------------------------------
    frm_settings = tk.Frame(
        master=project_window,
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_settings_details = tk.Frame(
        master=project_window,
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_levels = tk.Frame(
        master=project_window, 
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_levels_details = tk.Frame(
        master=project_window, 
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_flags = tk.Frame(
        master=project_window,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_flags_details = tk.Frame(
        master=project_window,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_history = tk.Frame(
        master=project_window,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_history_details = tk.Frame(
        master=project_window,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_status = tk.Frame(
        master=project_window, 
        relief=tk.GROOVE,
        borderwidth=2)

    # Setup settings frame (header) --------------------
    # Create widgets
    lbl_settings_header = tk.Label(
        frm_settings, 
        text="Project Settings", 
        font="tkHeadingFont")
    btn_settings_edit = tk.Button(
        frm_settings, 
        text="Edit", 
        width=15, 
        relief=tk.GROOVE, 
        borderwidth=2, 
        bg="#c9c9c9")
    # Pack widgets
    lbl_settings_header.pack(side=tk.LEFT)
    btn_settings_edit.pack(side=tk.RIGHT)

    # Setup settings frame (details) -------------------
    # Create widgets
    lbl_settings_details = tk.Label(
        frm_settings_details, 
        text=settings_details, 
        justify=tk.LEFT,
        font=("tkFixedFont", 10))
    # Pack Widgets
    lbl_settings_details.pack(side=tk.LEFT, fill=tk.BOTH)

    # Setup device levels frame (header) ---------------
    # Create widgets
    lbl_levels_header = tk.Label(
        frm_levels, 
        text="Device Levels", 
        font="tkHeadingFont")
    # Pack widgets
    lbl_levels_header.pack(side=tk.LEFT)

    # Setup device levels frame (details) --------------
    # Create widgets
    lbl_voltage = tk.Label(
        frm_levels_details, 
        text=f"{volts} V", 
        width=16, height=2, 
        bg="white", 
        font=("Arial", 25), 
        relief=tk.SUNKEN, 
        borderwidth=5)
    lbl_current = tk.Label(
        frm_levels_details, 
        text=f"{amps} A", 
        width=16, 
        height=2, 
        bg="white", 
        font=("Arial", 25), 
        relief=tk.SUNKEN, 
        borderwidth=5)
    # Pack widgets
    frm_levels_details.columnconfigure(0, weight=1)
    frm_levels_details.columnconfigure(1, weight=1)
    lbl_voltage.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    lbl_current.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)

    # Setup flags frame (header) -----------------------
    # Create widgets
    lbl_flags_header = tk.Label(
        frm_flags, 
        text="Flags", 
        font="tkHeadingFont")
    global lbl_flags_beacon # Connect with the global variable
    lbl_flags_beacon = tk.Label(
        frm_flags,  
        width=15, 
        relief=tk.SUNKEN,
        borderwidth=2,
        bg="white")
    btn_toggle_flag = tk.Button(
        frm_flags,
        text="Toggle flag",
        width=15,
        relief=tk.RIDGE,
        borderwidth=2,
        bg="#c9c9c9",
        command=toggle_flag)
    # Pack widgets
    lbl_flags_header.pack(side=tk.LEFT)
    lbl_flags_beacon.pack(side=tk.RIGHT)
    btn_toggle_flag.pack(side=tk.RIGHT)

    # Setup flags frame (details) ----------------------
    global flags_details     # Connect to the global variables
    global lbx_flags_details #
    # Create widgets
    lbx_flags_details = tk.Listbox(
        frm_flags_details,
        listvariable=flags_details,
        height=4,
        bg="white")
    # Pack widgets
    lbx_flags_details.pack(fill=tk.BOTH)

    # Setup readings history frame (header) ------------
    # Create widgets
    lbl_history_header = tk.Label(
        frm_history, 
        text="Readings History", 
        font="tkHeadingFont")
    # Pack widgets
    lbl_history_header.pack(side=tk.LEFT)

    # Setup readings history frame (details) -----------
    global history_details     # Connect to the global variables
    global lbx_history_details #
    # Create widgets
    lbx_history_details = tk.Listbox(
        frm_history_details,
        listvariable=history_details,
        bg="white",
        height=21
    )
    # Pack widgets
    lbx_history_details.pack(fill=tk.BOTH)

    # Setup status frame
    # Create widgets
    lbl_status = tk.Label(
        # TODO: finish this widget
        frm_status,
        text=status)
    lbl_status_beacon = tk.Label(
        # TODO: finish this widget
        frm_status,
        relief=tk.SUNKEN,
        borderwidth=2,
        width=15,
        bg="white")
    # Pack widgets
    lbl_status.pack(side=tk.LEFT)
    lbl_status_beacon.pack(side=tk.RIGHT)

    # Pack frames in window ----------------------------
    frm_settings.pack(fill=tk.X)
    frm_settings_details.pack(fill=tk.X)
    frm_levels.pack(fill=tk.X)
    frm_levels_details.pack(fill=tk.X)
    frm_flags.pack(fill=tk.X)
    frm_flags_details.pack(fill=tk.X)
    frm_history.pack(fill=tk.X)
    frm_history_details.pack(fill=tk.BOTH)
    frm_status.pack(fill=tk.X)

#
# setup_settings_window
#
def open_settings_window():
    """Setup the Project Settings GUI."""
    global settings_window  # Connect to the global variable
    # TODO: add code here



# # ============= Run setup and enter event loop
if __name__ == '__main__':
    # open_settings_window()
    # settings_window.main
    setup_project_window()
    project_window.after(200, flash_beacon)
    project_window.after(1000, update_flags_details)
    project_window.mainloop()