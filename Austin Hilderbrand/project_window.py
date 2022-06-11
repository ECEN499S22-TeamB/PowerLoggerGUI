"""
project_window.py
This script launches a new data collection window. 
Author: Austin Hilderbrand
"""

# ============= Imports
from os import device_encoding
import tkinter as tk
from tkinter import messagebox


# ============= Globals
# Project settings
# TODO: figure out how to get the real values from Project Settings window
device_name = "Device1"
com_port = "COM1"
shunt_resistor = 5 # Ohms
sample_rate = 1 # Hz

# Device levels
# TODO: integrate DATAQ code and assign real values
volts = 20
amps = 1


# ============= Event handlers
#
# donothing
#
def donothing():
    """Test function that does nothing."""
    messagebox.showinfo('Nothing', 'No function.')

#
# change_color
#
# def change_color(lbl_flags_beacon):
#     """Flash the color of the flags beacon box."""
#     current_color = lbl_flags_beacon.cget("background")
#     if current_color == "red":
#         next_color = "white"  
#     else:
#         next_color = "red"
#     lbl_flags_beacon.config(background=next_color)
#     window.after(200, change_color(lbl_flags_beacon))



# ============= Setup visuals
#
# setup
#
def setup():
    """Setup the GUI."""
    # Local helper functions ---------------------------
    #
    # change_color
    #
    def change_color():
        """Flash the color of the flags beacon box."""
        current_color = lbl_flags_beacon.cget("background")
        if current_color == "red":
            next_color = "white"  
        else:
            next_color = "red"
        lbl_flags_beacon.config(background=next_color)
        window.after(200, change_color)

    # Configure the window
    window.title("Power Logger: Project Window")
    window.geometry('600x750-10+10') # Place in upper right screen

    # Create frames ------------------------------------
    frm_settings = tk.Frame(
        master=window, 
        height=20, 
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_settings_details = tk.Frame(
        master=window, 
        height=150, 
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_levels = tk.Frame(
        master=window, 
        height=20, 
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_levels_details = tk.Frame(
        master=window, 
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_flags = tk.Frame(
        master=window, 
        height=20,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_flags_details = tk.Frame(
        master=window, 
        height=50)
    frm_history = tk.Frame(
        master=window, 
        height=20)
    frm_history_details = tk.Frame(
        master=window, 
        height=300)
    frm_status = tk.Frame(
        master=window, 
        height=20)

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
    settings_details = f"""
    Device Name: \t\t{device_name}
    COM Port: \t\t{com_port}
    Shunt Resistor: \t\t{shunt_resistor} \u03A9
    Sample Rate: \t\t{sample_rate} Hz
    """
    lbl_settings_details = tk.Label(
        frm_settings_details, 
        text=settings_details, 
        justify=tk.LEFT)
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
    lbl_voltage.pack(side=tk.LEFT)
    lbl_current.pack(side=tk.RIGHT)

    # Setup flags frame (header) -----------------------
    # Create widgets
    lbl_flags_header = tk.Label(
        frm_flags, 
        text="Flags", 
        font="tkHeadingFont")
    lbl_flags_beacon = tk.Label(
        frm_flags,  
        width=15, 
        relief=tk.SUNKEN, 
        borderwidth=2, 
        bg="red")
    change_color() # Allows the GUI to flash the beacon
    # Pack widgets
    lbl_flags_header.pack(side=tk.LEFT)
    lbl_flags_beacon.pack(side=tk.RIGHT)

    # Pack frames in window ----------------------------
    frm_settings.pack(fill=tk.X)
    frm_settings_details.pack(fill=tk.X)
    frm_levels.pack(fill=tk.X)
    frm_levels_details.pack(fill=tk.X)
    frm_flags.pack(fill=tk.X)


# # ============= Run setup and enter event loop
if __name__ == '__main__':
    window = tk.Tk() # Create a new window
    setup()
    window.mainloop()