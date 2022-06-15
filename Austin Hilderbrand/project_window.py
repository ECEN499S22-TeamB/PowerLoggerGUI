"""
project_window.py
This script launches a new data collection window. 
Author: Austin Hilderbrand
"""

# ============= Imports
import tkinter as tk
import tkinter.ttk as ttk
# from ttkthemes import ThemedTk
from tkinter import messagebox
import time
import sys


# ============= Globals
# Command line args passed from caller (main_menu.py) ---------------
if len(sys.argv) < 2:
    project_ID = -1 # For testing purposes
else:
    project_ID = int(sys.argv[1]) # Unique Project ID

# Windows -----------------------------------------------------------
project_window = None
settings_window = None

# Project settings --------------------------------------------------
# TODO: figure out how to get the real values from Project Settings window
# project_settings dictionary (will get written to JSON)
project_settings = {
    "Project ID": project_ID,
    "Settings": {
        "Device Name": "",
        "COM Port": "",
        "Shunt Resistor": None, # Ohms
        "Decimation": None,     # samples/update
        "Flag Trigger": None    # A
    }
}

device_name = project_settings["Settings"]["Device Name"]
com_port = project_settings["Settings"]["COM Port"]
shunt_resistor = project_settings["Settings"]["Shunt Resistor"]
decimation = project_settings["Settings"]["Decimation"]
flag_trigger = project_settings["Settings"]["Flag Trigger"]

# Starting output string
settings_details = f"Device Name: \n" +\
    f"COM Port: \n" +\
    f"Shunt Resistor: \n" +\
    f"Decimation Factor: \n" +\
    f"Flag Trigger: "

# settings_details = f"Device Name: \t\t{device_name}\n" +\
#     f"COM Port: \t\t{com_port}\n" +\
#     f"Shunt Resistor: \t\t{shunt_resistor} \u03A9\n" +\
#     f"Decimation Factor: \t{decimation} samples/update\n" +\
#     f"Flag Trigger: \t\t\u00B1 {flag_trigger} A"

# COM ports
lbx_com_port = None    # Make this widget global
com_ports_list = []     # Start with empty list for thee listbox
active_com_ports = None # Make StringVar type

# Shunt Resistor
resistor_values = [0.01, 0.1, 1, 5, 10]

# Device levels -----------------------------------------------------
# TODO: integrate DATAQ code and assign real values
volts = 20
amps = 1

# Flagging ----------------------------------------------------------
lbx_flags_details = None    # Make this widget global
flags_list = []             # Start with empty list for the listbox
flags_details = None        # Make StringVar type
lbl_flags_beacon = None     # Make this widget global
flag = False

# Readings history --------------------------------------------------
lbx_history_details = None    # Make 
history_list = []           # Start with empty list for the listbox
history_details = None      # Make StringVar type

# Status ------------------------------------------------------------
status = "<placeholder>"
pgr_status_bar = None


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

#
# update_com_ports
#
def update_com_ports():
    """Update the active COM ports list (accessed by settings window)."""
    global lbx_com_port     # Connect to the global variables
    global com_ports_list   #
    global active_com_ports #

    # Is the settings_window running?
    try:
        if settings_window.state() == "normal":
            # If so, update the widget
            com_ports_list = ['COM1', 'COM3', 'COM5'] # DEBUG
            if not active_com_ports:
                active_com_ports = tk.StringVar(value=com_ports_list)
            else:
                active_com_ports.set(com_ports_list)
            lbx_com_port['listvariable'] = active_com_ports # Update the widget
            project_window.after(1000, update_com_ports)
    except:
        project_window.after(1000, update_com_ports)        


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
    project_window.title(f"Power Logger: Project <{project_ID}> Window")
    project_window.attributes('-topmost', True)
    project_window.geometry('600x750-10+10')    # Place in upper right screen
    project_window.resizable(False, False)      # Don't make window resizable

    # Intercept the close button
    project_window.protocol("WM_DELETE_WINDOW", ask_close)

    # Create a ttk style instance
    style = ttk.Style(project_window)
    style.theme_use('clam') # Choose the theme for ttk frames/widgets

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

    # Create the File menu widget
    menubar = tk.Menu(project_window)   # Create the menubar
    menu_file = tk.Menu(menubar, tearoff=0)
    menu_file.add_command(label="Exit", command=ask_close)
    menubar.add_cascade(label="File", menu=menu_file)

    # Create the Help menu widget
    menu_help = tk.Menu(menubar, tearoff=0)
    menu_help.add_command(label="About", command=donothing)
    menubar.add_cascade(label="Help", menu=menu_help)

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
        bg="#c9c9c9",
        command=open_settings_window)
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
    btn_start = tk.Button(
        frm_levels,
        text="Start",
        width=15, 
        relief=tk.GROOVE, 
        borderwidth=2, 
        bg="#c9c9c9",
    )
    btn_stop = tk.Button(
        frm_levels,
        text="Stop",
        width=15, 
        relief=tk.GROOVE, 
        borderwidth=2, 
        bg="#c9c9c9",
    )
    # Pack widgets
    lbl_levels_header.pack(side=tk.LEFT)
    btn_stop.pack(side=tk.RIGHT)
    btn_start.pack(side=tk.RIGHT)

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
        # TODO: replace Listbox with something else?
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
        height=22
    )
    # Pack widgets
    lbx_history_details.pack(fill=tk.BOTH)

    # Setup status frame -------------------------------
    global pgr_status_bar # Connect to the global variable
    # Create widgets
    lbl_status = tk.Label(
        frm_status,
        text=status)
    # Create and configure the ttk Progressbar widget
    style.configure('white.Horizontal.TProgressbar', background="green")
    pgr_status_bar = ttk.Progressbar(
        frm_status,
        style='white.Horizontal.TProgressbar',
        orient=tk.HORIZONTAL,
        length=100,
        mode="indeterminate")
    # Pack widgets
    lbl_status.pack(side=tk.LEFT)
    pgr_status_bar.pack(side=tk.RIGHT)

    # Pack frames in window ----------------------------
    project_window['menu'] = menubar
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
    global project_window  # Connect to the global variables
    global settings_window #
    
    try:
        # If a settings window is already open, exit
        if settings_window.state() == "normal":
            return # TODO: add more functionality here
    except:
        # If not, open a new settings window
        settings_window = None
        settings_window = tk.Toplevel(project_window)

    # Configure the window -----------------------------
    settings_window.lift(project_window)
    settings_window.geometry('400x200-10+10')
    settings_window.resizable(False, False)

    # Create frames ------------------------------------
    frm_device_name = tk.Frame(
        master=settings_window,
        relief=tk.GROOVE,
        borderwidth=2) 
    frm_com_port = tk.Frame(
        master=settings_window,
        relief=tk.GROOVE,
        borderwidth=2) 
    frm_shunt_resistor = tk.Frame(
        master=settings_window,
        relief=tk.GROOVE,
        borderwidth=2) 
    frm_decimation = tk.Frame(
        master=settings_window,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_flag_trigger = tk.Frame(
        master=settings_window,
        relief=tk.GROOVE,
        borderwidth=2) 
    frm_okaycancel = tk.Frame(
        master=settings_window,
        relief=tk.GROOVE,
        borderwidth=2) 

    # Setup device name frame --------------------------
    # Create widgets
    lbl_device_name = tk.Label(
        frm_device_name,
        text="Device Name",
        anchor="w",
        width=25)
    ent_device_name = tk.Entry(
        frm_device_name,
        width=15,
        relief=tk.GROOVE,
        borderwidth=2)
    # Pack widgets
    lbl_device_name.pack(side=tk.LEFT)
    ent_device_name.pack(side=tk.LEFT)

    # Setup com port frame -----------------------------
    global lbx_com_port # Connect to the global variable
    # Create widgets
    lbl_com_port = tk.Label(
        frm_com_port,
        text="COM Port",
        anchor="w",
        width=25)
    lbx_com_port = tk.Listbox(
        frm_com_port,
        listvariable=active_com_ports,
        width=15,
        height=1,
        relief=tk.GROOVE,
        borderwidth=2)
    # Pack widgets
    lbl_com_port.pack(side=tk.LEFT)
    lbx_com_port.pack(side=tk.LEFT)

    # Setup shunt resistor frame -----------------------
    # Create widgets
    lbl_shunt_resistor = tk.Label(
        frm_shunt_resistor,
        text="Shunt Resistor Value",
        anchor="w",
        width=25)
    cmb_shunt_resistor = ttk.Combobox(
        frm_shunt_resistor,
        values=resistor_values,
        width=13)
    lbl_resistor_units = tk.Label(
        frm_shunt_resistor,
        text="\u03A9",
        anchor="w",
        width=15)
    # Pack widgets
    lbl_shunt_resistor.pack(side=tk.LEFT)
    cmb_shunt_resistor.pack(side=tk.LEFT)
    lbl_resistor_units.pack(side=tk.LEFT)

    # Setup decimation factor frame --------------------
    # Create widgets
    lbl_decimation = tk.Label(
        frm_decimation,
        text="Decimation Factor",
        anchor="w",
        width=25)
    cmb_decimation = tk.Entry(
        frm_decimation,
        width=15)
    lbl_decimation_units = tk.Label(
        frm_decimation,
        text="samples/update",
        anchor="w",
        width=15)
    # Pack widgets
    lbl_decimation.pack(side=tk.LEFT)
    cmb_decimation.pack(side=tk.LEFT)
    lbl_decimation_units.pack(side=tk.LEFT)

    # Pack frames in window
    frm_device_name.pack(fill=tk.X)
    frm_com_port.pack(fill=tk.X)
    frm_shunt_resistor.pack(fill=tk.X)
    frm_decimation.pack(fill=tk.X)
    frm_flag_trigger.pack(fill=tk.X)
    frm_okaycancel.pack(fill=tk.BOTH)


# # ============= Run setup and enter event loop
if __name__ == '__main__':
    setup_project_window()
    open_settings_window()
    pgr_status_bar.start(10) # DEBUG
    project_window.after(200, flash_beacon)
    project_window.after(1000, update_flags_details)
    project_window.after(1000, update_com_ports)
    project_window.mainloop()