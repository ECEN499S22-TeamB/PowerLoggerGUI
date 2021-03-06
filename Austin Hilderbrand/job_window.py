"""
job_window.py
This script launches a new data collection window. 
Author: Austin Hilderbrand
"""

# ============= Imports
from copy import deepcopy
import tkinter as tk
import tkinter.ttk as ttk
# from ttkthemes import ThemedTk
from tkinter import messagebox
import time
import sys
from datetime import date


# ============= Globals
# Time & date
today = date.today()
year = today.year
yr = year % 100 # Keep last 2 digits

# Command line args passed from caller (main_menu.py) ---------------
# Job number
if len(sys.argv) < 2:
    job_number = str(9999) # For testing purposes
else:
    job_number = sys.argv[1]   # Unique Job ID
job_number = job_number.zfill(4)  # Leading zeros if less than 4 digits

# Windows -----------------------------------------------------------
job_window = None
settings_window = None

# Job settings --------------------------------------------------
# TODO: figure out how to get the real values from Job Settings window
# job_settings dictionary (will get written to JSON)
job_settings = {
    "Job Number": job_number,
    "COM Port": "",
    "Shunt Resistor": None, # Ohms
    "Decimation": None,     # samples/update
    "Flag Trigger": None    # A
}

com_port = job_settings["COM Port"]
shunt_resistor = job_settings["Shunt Resistor"]
decimation = job_settings["Decimation"]
flag_trigger = job_settings["Flag Trigger"]

# Widget
lbl_settings_details = None

# Starting output string
settings_details = f"Job Number: \n" +\
    f"COM Port: \n" +\
    f"Shunt Resistor: \n" +\
    f"Decimation Factor: \n" +\
    f"Flag Trigger: "

# COM ports
lbx_com_port = None     # Make this widget global
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
previous_selected = None
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
    global job_window # Connect to the global variable
    if flag:
        change_color()
    else:
        lbl_flags_beacon.config(bg="white") # If no flag, make bg white
    job_window.after(200, flash_beacon)         # Run every 200 ms

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

    # Update the listbox
    flags_list.append(f"ERROR{i}\n") # DEBUG
    i += 1 # DEBUG
    if not flags_details:
        flags_details = tk.StringVar(value=flags_list)
    else:
        flags_details.set(flags_list)
    lbx_flags_details['listvariable'] = flags_details # Update the widget

    # Decide how to focus the listbox
    lbx_flags_details.see("end") # Keep latest output in view
    # If user has made a selection, keep it visible
    idxs = lbx_flags_details.curselection()
    if len(idxs)==1:
            idx = lbx_flags_details.curselection()
            lbx_flags_details.selection_set(idx)
            lbx_flags_details.see(idx)
    job_window.after(1000, update_flags_details, i)

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
            job_window.after(1000, update_com_ports)
    except:
        job_window.after(1000, update_com_ports)        


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
    """Confirm the user wants to close the job window."""
    global job_window # Connect to the global variable
    if messagebox.askokcancel(
        message="Are you sure you want to close the window?", 
        icon='warning', title="Please confirm."):
        job_window.destroy()

#
# retry_settings
#
def retry_settings(message):
    """Close settings window, and try again."""
    # If the user didn't select a COM port, show error dialog
    messagebox.showerror(title="Error: Invalid Input", message=message)
    settings_window.destroy()
    get_settings()

#
# deselect_item
#
def deselect_item(event):
    """Left click deselects the listbox item."""
    global previous_selected # Connect to the global variables
    global lbx_flags_details # 

    if lbx_flags_details.curselection() == previous_selected:
        lbx_flags_details.selection_clear(0, tk.END)
    previous_selected = lbx_flags_details.curselection()

# ============= Setup visuals
#
# setup_job_window
#
def setup_job_window():
    """Setup the Job Window GUI."""
    # Connect to the global variables ------------------
    # Windows
    global job_window

    # Widgets
    global lbl_settings_details # Settings
    global lbl_flags_beacon     # Flags
    global flags_details
    global lbx_flags_details
    global previous_selected
    global history_details      # History
    global lbx_history_details
    global pgr_status_bar       # Status
    # Convert to tk var types
    # TODO: add code here

    # Create window ------------------------------------
    job_window = tk.Tk()
    # Configure the window -----------------------------
    job_window.title(f"Power Logger: RTS{yr} - J{job_number}")
    job_window.attributes('-topmost', True)
    job_window.geometry('600x750-10+10')    # Place in upper right screen
    # TODO: Redo layout with grid for more robustness?
    job_window.resizable(False, False)      # Don't make window resizable

    # Intercept the close button
    job_window.protocol("WM_DELETE_WINDOW", ask_close)

    # Create a ttk style instance
    style = ttk.Style(job_window)
    style.theme_use('clam') # Choose the theme for ttk frames/widgets

    # Create frames ------------------------------------
    frm_settings = tk.Frame(
        master=job_window,
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_settings_details = tk.Frame(
        master=job_window,
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_levels = tk.Frame(
        master=job_window, 
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_levels_details = tk.Frame(
        master=job_window, 
        relief=tk.GROOVE, 
        borderwidth=2)
    frm_flags = tk.Frame(
        master=job_window,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_flags_details = tk.Frame(
        master=job_window,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_history = tk.Frame(
        master=job_window,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_history_details = tk.Frame(
        master=job_window,
        relief=tk.GROOVE,
        borderwidth=2)
    frm_status = tk.Frame(
        master=job_window, 
        relief=tk.GROOVE,
        borderwidth=2)

    # Create the File menu widget
    menubar = tk.Menu(job_window)   # Create the menubar
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
        text="Job Settings", 
        font="tkHeadingFont")
    btn_settings_edit = tk.Button(
        frm_settings, 
        text="Edit", 
        width=15, 
        relief=tk.GROOVE, 
        borderwidth=2, 
        bg="#c9c9c9",
        command=get_settings)
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
    # Create widgets
    lbx_flags_details = tk.Listbox( 
        # TODO: replace Listbox with something else?
        frm_flags_details,
        listvariable=flags_details,
        height=4,
        bg="white")
    # Configure widgets
    job_window.bind('<ButtonPress-1>', deselect_item)
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
    job_window['menu'] = menubar
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
def get_settings():
    """Setup the Job Settings GUI."""
    # Connect to globals -------------------------------
    # Windows
    global job_window
    global settings_window
    # Widgets
    global lbx_com_port
    # Settings
    global shunt_resistor
    global decimation
    global flag_trigger
    # Convert to tk var types
    shunt_resistor = tk.StringVar(value="")
    decimation = tk.IntVar(value=0)
    flag_trigger = tk.StringVar(value="")

    # Helper functions ---------------------------------
    def close_okay():
        """Extract user-selected settings and close the settings window."""
        # Connect to the global variables --------------
        # Widgets
        global lbl_settings_details
        # Settings
        global com_port 
        global shunt_resistor 
        global decimation
        global flag_trigger

        # Extract settings -----------------------------
        # Input validation - COM port selection
        # TODO: fortify validation?
        idxs = lbx_com_port.curselection()
        if len(idxs)!=1:
            retry_settings("Please select a COM port.")
            return

        # Extract values from tk vars
        idx = lbx_com_port.curselection()
        com_port = lbx_com_port.get(idx)
        shunt_resistor = shunt_resistor.get()
        decimation = decimation.get()
        flag_trigger = flag_trigger.get()

        # Input validation - remaining settings
        if shunt_resistor == "":
            retry_settings("Please enter a valid shunt resistor value.")
            return
        if decimation == 0:
            retry_settings("Please enter a valid decimation factor.")
            return
        if flag_trigger == "":
            retry_settings("Please enter a valid flag trigger.")
            return

        # Convert tk.StringVar --> float
        shunt_resistor = float(shunt_resistor)
        flag_trigger = float(flag_trigger)

        # Update job settings
        job_settings["COM Port"] = com_port
        job_settings["Shunt Resistor"] = shunt_resistor
        job_settings["Decimation"] = decimation
        job_settings["Flag Trigger"] = flag_trigger

        # Update job settings widget -------------------
        settings_details = f"Job number: \t\t{job_number}\n" +\
            f"COM Port: \t\t{com_port}\n" +\
            f"Shunt Resistor: \t\t{shunt_resistor} \u03A9\n" +\
            f"Decimation Factor: \t{decimation} samples/update\n" +\
            f"Flag Trigger: \t\t\u00B1 {flag_trigger} A"
        lbl_settings_details['text'] = settings_details
        

        # Close settings window ------------------------
        settings_window.destroy()

    # Open window (or don't) ---------------------------    
    try:
        # If a settings window is already open, exit
        if settings_window.state() == "normal":
            return # TODO: add more functionality here
    except:
        # If not, open a new settings window
        settings_window = None
        settings_window = tk.Toplevel(job_window)

    # Configure the window -----------------------------
    settings_window.title(
        f"Power Logger: Job Settings (RTS{yr} - J{job_number})")
    settings_window.lift(job_window)
    settings_window.geometry('400x140-10+10')
    settings_window.resizable(False, False)

    # Create frames ------------------------------------
    frm_job_number = tk.Frame(
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
        borderwidth=2,
        padx=5, pady=5) 

    # Setup com port frame -----------------------------
    # Create widgets
    lbl_com_port = tk.Label(
        frm_com_port,
        text="COM Port",
        anchor="w",
        width=25)
    lbx_com_port = tk.Listbox(
        frm_com_port,
        listvariable=active_com_ports,
        selectmode="browse",
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
        textvariable=shunt_resistor,
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
    ent_decimation = tk.Entry(
        frm_decimation,
        textvariable=decimation,
        width=15,
        relief=tk.GROOVE,
        borderwidth=2)
    lbl_decimation_units = tk.Label(
        frm_decimation,
        text="samples/update",
        anchor="w",
        width=15)
    # Pack widgets
    lbl_decimation.pack(side=tk.LEFT)
    ent_decimation.pack(side=tk.LEFT)
    lbl_decimation_units.pack(side=tk.LEFT)

    # Setup flag trigger frame -------------------------
    # Create widgets
    lbl_flag_trigger = tk.Label(
        frm_flag_trigger,
        text="Flag Trigger\t\t\t\u00B1",
        anchor="w",
        width=23)
    lbl_flag_trigger_prefix = tk.Label(
        frm_flag_trigger,
        text="\u00B1")
    ent_flag_trigger = tk.Entry(
        frm_flag_trigger,
        textvariable=flag_trigger,
        width=15,
        relief=tk.GROOVE,
        borderwidth=2)
    lbl_flag_trigger_units = tk.Label(
        frm_flag_trigger,
        text="A",
        anchor="w",
        width=15)
    # Pack widgets
    lbl_flag_trigger.pack(side=tk.LEFT)
    lbl_flag_trigger_prefix.pack(side=tk.LEFT)
    ent_flag_trigger.pack(side=tk.LEFT)
    lbl_flag_trigger_units.pack(side=tk.LEFT)

    # Setup okaycancel frame ---------------------------
    # Configure the grid
    frm_okaycancel.rowconfigure(0, weight=1)
    frm_okaycancel.columnconfigure(0, weight=1)
    frm_okaycancel.columnconfigure(1, weight=1)
    frm_okaycancel.columnconfigure(2, weight=1)
    # Create widgets
    btn_okay = tk.Button(
        frm_okaycancel,
        text="Okay",
        relief=tk.GROOVE,
        borderwidth=2,
        width=15,
        bg="#c9c9c9",
        command=close_okay)
    btn_cancel = tk.Button(
        frm_okaycancel,
        text="Cancel",
        relief=tk.GROOVE,
        borderwidth=2,
        width=15,
        bg="#c9c9c9",
        command=settings_window.destroy)
    # Pack widgets
    btn_okay.grid(row=0, column=0, sticky="e")
    btn_cancel.grid(row=0, column=2, sticky="w")

    # Pack frames in window
    frm_com_port.pack(fill=tk.X)
    frm_shunt_resistor.pack(fill=tk.X)
    frm_decimation.pack(fill=tk.X)
    frm_flag_trigger.pack(fill=tk.X)
    frm_okaycancel.pack(fill=tk.BOTH)


# # ============= Run setup and enter event loop
if __name__ == '__main__':
    setup_job_window()
    get_settings()
    pgr_status_bar.start(10) # DEBUG
    job_window.after(200, flash_beacon)
    job_window.after(1000, update_flags_details)
    job_window.after(1000, update_com_ports)
    job_window.mainloop()