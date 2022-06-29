"""
job_window.py
This script launches a new data collection window. 
Author: Austin Hilderbrand
"""

"""
ECEN 499 Senior Project
Instructor: Kevin Smith
    208-496-7612
    smithk@byui.edu

Team B - Radiation Test Solutions
    Aaron Mears (team lead)
        509-596-8539
        amears@radiationtestsolutions.com
    Austin Hilderbrand
        602-390-5594
        hil16039@byui.edu
    Nathan Taylor
        775-397-8139
        tay18060@byui.edu
    Joshua Armstrong
        208-406-8689
        arm05006@byui.edu
"""

"""
GitHub tips -------------------------------------------------------------
To upload changes
    git add .   (stage changes - LOCAL)
    git commit  (save staged changes - LOCAL)
    git push    (upload saved changes to remote repo - LOCAL-->REMOTE)
    
To receive Changes
    git pull    (download remote changes - REMOTE-->LOCAL)
    
To change branches
    git checkout branchName

To check status/verify branch
    git status
"""

# ============= Imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import time
import sys
import datetime
import serial
import serial.tools.list_ports


# ============= Globals
# Time & date
today = datetime.date.today()
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
# TODO: add code to write to/read from JSON
job_settings = {
    "Job Number": job_number,
    "COM Port": "",
    "Shunt Resistor": "",   # Ohms
    "Decimation": 0,        # samples/update
    "Flag Trigger": ""      # A
}

com_port = job_settings["COM Port"]
shunt_resistor = job_settings["Shunt Resistor"]
decimation = job_settings["Decimation"]
amps_baseline = 10 # TODO: don't hardcode - include with other settings
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
cmb_com_port = None     # Make this widget global
active_com_ports = []   # Make empty list to hold active COM ports

# Shunt Resistor
resistor_values = [0.01, 0.1, 1, 5, 10]

# Initial setup flag
initial_setup = 0 # When set to 1, initial setup completed

# Device levels ----------------------------------------
lbl_voltage = None
lbl_current = None
volts = 0.00
amps = 0.00

# GUI vars ---------------------------------------------
# Flagging
"""
flags = [bool, bool, bool]
The lower the index, the higher the priority.
flags[0] ----> Priority: 0, RED, process error (ex. disc. device)
flags[1] ----> Priority: 1, ORANGE, levels trigger (levels out of range)
flags[2] ----> Priotiry: 2, YELLOW, levels warning (levels near trigger)
"""
lbx_flags_details = None    # Make this widget global
flags_list = []             # Start with empty list for the listbox
flags_details = None        # Make StringVar type
prev_sel_flags = None       # Used for enhanced listbox deselection
lbl_flags_beacon = None     # Make this widget global
flags = [False]*3           # 3 flags
# Output string
flag_output_str = ""
flags_give_msg = [True]*len(flags) # Display the msg for each flag?

# Readings history
lbx_history_details = None  # Make this widget global
history_list = []           # Start with empty list for the listbox
history_details = None      # Make StringVar type
prev_sel_history = None     # Used for enhanced listbox deselection
# Output string
history_output_str = ""

# Status
status = "<placeholder>"
pgr_status_bar = None

# Read DAQ ---------------------------------------------
""" 
Example slist for model DI-1100
0x0000 = Analog channel 0, ±10 V range
0x0001 = Analog channel 1, ±10 V range
0x0002 = Analog channel 2, ±10 V range
0x0003 = Analog channel 3, ±10 V range
"""
slist = [0x0000,0x0001,0x0002,0x0003]

# Declare serial object for hooked DAQ
ser=serial.Serial()

# Active COM port
hooked_ports = {}
hooked_port = None  # Will hold complete port info
com_port = ""       # Will hold hooked_port.device string (ex. "COM5")

# Contains accumulated values for each analog channel 
# used for the average calculation
achan_accumulation_table = list(())

# Used to store the last available reading (averaged) for each channel
all_volts = [0]*len(slist) # Used in readings history

# Define flag to indicate if acquiring is active 
acquiring = False

# Used during data collection process
dec_count = None
slist_pointer = 0
achan_number = 0


# ============= mainloop functions
#
# next_reading
def update_levels():
    """Complete a decimation loop and update device levels with
    averaged values."""
    # Connect to global variables ----------------------
    global lbl_voltage
    global lbl_current
    global volts
    global amps
    global dec_count
    global slist_pointer
    global achan_accumulation_table
    global achan_number

    if not acquiring:
        return
    
    # TODO: this currently reads from all 4 analog input channels,
    # while only 2 are needed for this job. Change this(?)
    while (ser.inWaiting() > (2 * len(slist))):
         for i in range(len(slist)):
            # Always two bytes per sample...read them
            bytes = ser.read(2)
            # Only analog channels for a DI-1100, with dig_in states appearing
            # in the two LSBs of ONLY the first slist position
            result = int.from_bytes(bytes,byteorder='little', signed=True)

            # Since digital input states are embedded into the analog data 
            # stream there are four possibilities:
            if (dec_count == 1) and (slist_pointer == 0):
                # Decimation loop finished and first slist position
                # Two LSBs carry information only for first slist posiiton.
                # So, ... Preserve lower two bits representing digital input 
                # states
                dig_in = result & 0x3
                # Strip two LSBs from value to be added to the analog channel 
                # accumulation, preserving sign
                result = result >> 2
                result = result << 2
                # Add the value to the accumulator
                achan_accumulation_table[achan_number] = result + \
                    achan_accumulation_table[achan_number]
                achan_number += 1

                # End of a decimation loop for channel 1. So...
                # 1. Set reading for channel 1
                # 2. Set device level: volts
                # volts = accumulator value / decimation_factor
                all_volts[0] = achan_accumulation_table[achan_number-1] * \
                    10 / 32768 / decimation
                volts = all_volts[0]

            elif (dec_count == 1) and (slist_pointer != 0):
                # Decimation loop finished and NOT the first slist position
                # Two LSBs carry information only for first slist posiiton, 
                # which this isn't. So, ...
                # Just add value to the accumulator
                achan_accumulation_table[achan_number] = result + \
                    achan_accumulation_table[achan_number]
                achan_number += 1

                if slist_pointer == 1:
                    # End of a decimation loop for channel 2. So...
                    # 1. Set reading for channel 2
                    # 2. Set device levels: amps
                    all_volts[1] = \
                        achan_accumulation_table[achan_number-1] * \
                        10 / 32768 / decimation
                    amps =  (all_volts[1] - all_volts[0]) / shunt_resistor
                if slist_pointer == 2:
                    # End of a decimation loop for channel 3. So...
                    # 1. Set reading for channel 3
                    all_volts[2] = \
                        achan_accumulation_table[achan_number-1] * \
                        10 / 32768 / decimation
                if slist_pointer == 3:
                    # End of a decimation loop for channel 4. So...
                    # 1. Set reading for channel 4
                    all_volts[3] = \
                        achan_accumulation_table[achan_number-1] * \
                        10 / 32768 / decimation

            elif (dec_count != 1) and (slist_pointer == 0):
                # Decimation loop NOT finished and first slist position
                # Not the end of a decimation loop, but this is the first 
                # position in slist. So, ...
                # Just strip two LSBs, preserving sign...
                result = result >> 2
                result = result << 2
                # ...and add the value to the accumulator
                achan_accumulation_table[achan_number] = result + \
                    achan_accumulation_table[achan_number]
                achan_number += 1
            else:
                # Decimation loop NOT finished and NOT first slist position
                # Nothing to do except add the value to the accumlator
                achan_accumulation_table[achan_number] = \
                    result + achan_accumulation_table[achan_number]
                achan_number += 1

            # Get the next position in slist
            slist_pointer += 1

            if (slist_pointer + 1) > (len(slist)):
                # End of a pass through slist items
                if dec_count == 1:

                    # DEECIMATION LOOP FINISHED --------
                    dec_count = decimation # Reset decimation counter

                    # Update device levels widget
                    lbl_voltage['text'] = "{0:.2f} V".format(volts)
                    lbl_current['text'] = "{0:.2f} A".format(amps)
                    # Update flag and history widgets
                    check_conditions()
                    if any(flags):
                        update_flags_details()
                    update_readings_history()

                    # Reset analog channel accumulators to zero
                    achan_accumulation_table = [0] * \
                        len(achan_accumulation_table)
                else:
                    dec_count -= 1             
                slist_pointer = 0
                achan_number = 0

    # Repeat after 5ms pause
    job_window.after(5, update_levels)

#
# update_com_ports
#
def update_com_ports(override=0):
    """Update the active COM ports list (accessed by settings window)."""
    # Connect to the global variables
    global cmb_com_port
    global hooked_ports
    global active_com_ports
    global hooked_port

    # Is the settings_window running?
    try:
        if settings_window.state() == "normal" or override == 1:
            # If so, update the widget
            # Get a list of active com ports to scan 
            # for possible DATAQ Instruments devices
            active_com_ports = []   # Reset list
            hooked_ports = {}       # Reset dict
            hooked_port = None      # Reset port
            available_ports = list(serial.tools.list_ports.comports())
            for port in available_ports:
                # Do we have a DATAQ Instruments device?
                if ("VID:PID=0683" in port.hwid):
                    # Yes!  Dectect and assign the hooked com port
                    hooked_ports[port.device] = port
                    active_com_ports.append(port.device)
            cmb_com_port['values'] = active_com_ports # Update the widget
            job_window.after(1000, update_com_ports)
    except:
        job_window.after(1000, update_com_ports)

#
# check_conditions
#
def check_conditions():
    """Checks job conditions and, if needed, sets any flags."""
    global flags # Connect to global variables

    # Only proceed if acquiring data
    if not acquiring:
        return

    # Check serial connection status
    # flag0
    # TODO: add this functionality

    # Check device levels
    lower_limit = amps_baseline - flag_trigger
    upper_limit = amps_baseline + flag_trigger
    lower_warning = lower_limit + (0.25*flag_trigger) # 75% to trigger
    upper_warning = upper_limit - (0.25*flag_trigger) #
    # flag1
    if not (lower_limit < amps < upper_limit):
        flags[1] = True
    # flag2
    if not (lower_warning < amps < upper_warning) and not flags[1]:
        # Don't set flag2 if flag1 is already set
        flags[2] = True
    
    job_window.after(200, check_conditions)

#
# update_flag_beacon
#
def update_flag_beacon():
    """Change the color of the flags beacon box,
    depending of the top priority flag and acquiring status.
    """
    # Don't proceed if not acquiring data
    if not acquiring:
        job_window.after(200, update_flag_beacon)
        return

    # Get the current beacon color
    current_color = lbl_flags_beacon.cget("background")
    next_color = "green"
    
    # Decide on the next color
    if current_color == "white":
        if flags[0]:
            next_color = "red"
        elif flags[1]:
            next_color = "orange"
        elif flags[2]:
            next_color = "yellow"
    elif any(flags):
        next_color = "white"
    else: 
        next_color = "green"

    # Change the beacon color
    lbl_flags_beacon.config(background=next_color)

    job_window.after(200, update_flag_beacon)


# ============= Helper functions
#
# collection_teardown
#
def collection_teardown():
    """Wrapper for teardown procedures."""
    if acquiring:
        stop_collection()
    close_all_ports()
    clear_all_flags()

#
# close_all_ports
#
def close_all_ports():
    """Identify and close all hooked_ports."""
    global hooked_port  # Connect to global variables
    global com_port     #
    global ser          #

    update_com_ports(1)
    for hooked_port in hooked_ports.values():
        com_port = hooked_port.device
        open_com_port(int(com_port[3]))
        send_cmd("stop")
        ser.flushInput()
        ser.close()
        ser=serial.Serial()

#
# open_com_port
# 
def open_com_port(unique_val):
    """Hook the user-selected COM port to read from it.""" 
    global hooked_port # Connect to the global variables
    global ser         # 

    # Prevent always reading from first connected device
    hooked_port.pid += unique_val

    ser.port = com_port
    ser.timeout = 0
    ser.baudrate = '115200'
    # Open only if not already open
    if not ser.isOpen():
        ser.open()

#
# send_cmd
#
def send_cmd(command):
    """Sends a passed command string after appending <cr>"""
    ser.write((command+'\r').encode())
        
#
# config_scn_lst
# 
def config_scn_lst(): 
    """Configure the instrument's scan list.
    Scan list position must start with 0 and increment sequentially."""
    global achan_accumulation_table # Connect with the global variable

    position = 0
    for item in slist:
        send_cmd("slist "+ str(position ) + " " + str(item))
        # Add the channel to the logical list.
        achan_accumulation_table.append(0)
        position += 1

# 
# Config_DATAQ
#
def config_DATAQ():
    """Configure the DATAQ prior to collecting readings."""
    # Connect to the global variables
    global slist_pointer
    global achan_number

    # Stop in case DI-1100 is already scanning
    send_cmd("stop")
    # Define binary output mode
    send_cmd("encode 0")
    # Keep the packet size small for responsiveness
    send_cmd("ps 0")
    # Configure the instrument's scan list
    config_scn_lst()

    # Define sample rate = 1 Hz, where decimation_factor = 1000:
    # 60,000,000/(srate) = 60,000,000 / 60000 / decimation_factor = 1 Hz
    send_cmd("srate 60000")

    # This is the slist position pointer. Ranges from 0 (first position)
    # to len(slist)
    slist_pointer = 0
    # Init the logical channel number for enabled analog channels
    achan_number = 0

# 
# update_flags_details
#
def update_flags_details():
    """Update the flags details listbox."""
    # Only proceed if there is a flag which 
    proceed = False
    for idx in range(len(flags)):
        if flags[idx] and flags_give_msg[idx]:
            proceed = True
    if not proceed:
        return

    # Connect to the global variables ----------------
    global lbx_flags_details
    global flags_list
    global flags_details
    global flag_output_str

    # Return if there are no new messages to display
    if not any(flags_give_msg):
        return

    # Construct the output string
    flag_output_str = "" # Clear the output string
    # Add time
    now = datetime.datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S") # mm/dd/YY H:M:S
    flag_output_str += dt_string
    flag_output_str += "        " # Add spaces after time info
    # Flag info
    if flags[0] and flags_give_msg[0]:
        flg_string = "ERROR: Encountered problem while reading from device."
        flags_give_msg[0] = False
    elif flags[1] and flags_give_msg[1]:
        flg_string = "TRIGGER [CURRENT]: Current readings outside " + \
            "acceptable levels."
        flags_give_msg[1] = False
    elif flags[2] and flags_give_msg[2]:
        flg_string = "WARNING [CURRENT]: Abnormal current readings."
        flags_give_msg[2] = False
    flag_output_str += flg_string

    # Update the listbox
    flags_list.append(flag_output_str)
    if not flags_details:
        flags_details = tk.StringVar(value=flags_list)
    else:
        flags_details.set(flags_list)
    lbx_flags_details['listvariable'] = flags_details # Update the widget

    # Decide how to focus the listbox
    # TODO: add a way to allow the user to either keep list static or
    # always show most recent entries (will make it easier for user to browse
    # past entries)
    lbx_flags_details.see("end") # Keep latest output in view

#
# update_readings_history
#
def update_readings_history():
    """Update the readings history detail view with the new readings."""
    # Connect to the global variables ------------------
    global lbx_history_details
    global history_list
    global history_details
    global history_output_str

    # Construct the output string -------------------------
    # TODO: work on text alignment
    history_output_str = "" # Clear the output string
    # Add time
    now = datetime.datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S") # mm/dd/YY H:M:S
    history_output_str += dt_string
    history_output_str += "        " # Add spaces after time info
    # Add channel readings
    ch_string = f"channels: {all_volts[0]: .2f} V, " + \
        f"{all_volts[1]: .2f} V, {all_volts[2]: .2f} V, " + \
        f"{all_volts[3]: .2f} V"
    history_output_str += ch_string
    history_output_str += "         " # Add spaces after channels info
    # Add device levels
    lvls_string = f"device levels: {volts: .2f} V, {amps: .2f} A"
    history_output_str += lvls_string

    # Update the listbox
    history_list.append(history_output_str)
    if not history_details:
        history_details = tk.StringVar(value=history_list)
    else:
        history_details.set(value=history_list)
    lbx_history_details['listvariable'] = history_details # Update the widget

    # Decide how to focus the listbox
    # TODO: add a way to allow the user to either keep list static or
    # always show most recent entries (will make it easier for user to browse
    # past entries)
    lbx_history_details.see("end") # Keep latest output in view


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
        # End all processes relating to active data collection
        collection_teardown()
        # Close the job window and system exit
        job_window.destroy()
        SystemExit

#
# start_collection
#
def start_collection():
    """Start collecting data from the DATAQ."""
    global acquiring # Connect to the global variable

    # COM port error handling
    try:
        # Before starting data collection, make sure the COM port is still hooked.
        # If not, open settings window to force user to select a valid COM port.
        if hooked_ports[com_port] in list(serial.tools.list_ports.comports()):
            config_DATAQ()
            acquiring = True
            send_cmd("start")
            pgr_status_bar.start(10)           # Start the progress bar
            job_window.after(5, update_levels) # 5 ms between collection loops
        else: 
            message="The DATAQ has been disconnected.\n" + \
                "Please reconnect and try again."
            messagebox.showerror(
                title="Error: Device Disconnected", 
                message=message)
            get_settings()
    except:
        # A bug can be triggered a specific sequence of events involving
        # disconnecting/reconnecting DATAQs and starting the data collection
        # process. 
        # UPDATE: This is caused by uplugging the DATAQ and plugging it back
        # in, then pressing the "Start" button. It seems like forcing the 
        # user back through the settings window is a decent fix.
        # TODO: find a better fix
        message="Looks like something went wrong\nand this device is " + \
            "no longer available.\n\nPlease reset your connections " + \
            "\nand try again."
        messagebox.showerror(
            title="Error: Device Setup Malfunction",
            message=message)
        get_settings()

#
# stop_collection
#
def stop_collection():
    """Stop collecting data from the DATAQ."""
    global acquiring # Connect to the global variables
    global lbl_voltage
    global lbl_current

    if acquiring:
        send_cmd("stop") # TODO: fix: throws error if DATAQ unplugged
        pgr_status_bar.stop() # Stop the progress bar
        time.sleep(1)
        ser.flushInput() 
        acquiring = False

    # Update widgets (levels at 0 when not acquiring)
    lbl_voltage['text'] = "{0:.2f} V".format(0)
    lbl_current['text'] = "{0:.2f} V".format(0)

    clear_all_flags()

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
    # Connect to the global variables ------------------
    global prev_sel_flags
    global prev_sel_history
    global lbx_flags_details

    # Flags details listbox
    if lbx_flags_details.curselection() == prev_sel_flags:
        lbx_flags_details.selection_clear(0, tk.END)
    prev_sel_flags = lbx_flags_details.curselection()

    # History details listbox
    if lbx_history_details.curselection() == prev_sel_history:
        lbx_history_details.selection_clear(0, tk.END)
    prev_sel_history = lbx_history_details.curselection()

#
# clear_flag
#
def clear_top_flag():
    """Clears topmost (top priority) flag."""
    global flags # Connect with the global variable

    # Clear the topmost flag
    for idx in range(len(flags)):
        if flags[idx] == True:
            flags[idx] = False
            flags_give_msg[idx] = True
            return # Exit b/c only want to clear one flag at most

#
# clear_all_flags
#
def clear_all_flags():
    """Clears all flags."""
    global flags # Connect with the global variable

    # Clear the topmost flag
    for idx in range(len(flags)):
        if flags[idx] == True:
            flags[idx] = False
            flags_give_msg[idx] = True
    
    lbl_flags_beacon.config(background="white")


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
    global lbl_voltage          # Levels
    global lbl_current
    global lbl_flags_beacon     # Flags
    global flags_details
    global lbx_flags_details
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
        command=start_collection)
    btn_stop = tk.Button(
        frm_levels,
        text="Stop",
        width=15, 
        relief=tk.GROOVE, 
        borderwidth=2, 
        bg="#c9c9c9",
        command=stop_collection)
    # Pack widgets
    lbl_levels_header.pack(side=tk.LEFT)
    btn_stop.pack(side=tk.RIGHT)
    btn_start.pack(side=tk.RIGHT)

    # Setup device levels frame (details) --------------
    # Create widgets
    lbl_voltage = tk.Label(
        frm_levels_details, 
        text="{0:.2f} V".format(volts), 
        width=16, height=2, 
        bg="white", 
        font=("Arial", 25), 
        relief=tk.SUNKEN, 
        borderwidth=5)
    lbl_current = tk.Label(
        frm_levels_details, 
        text="{0:.2f} A".format(amps), 
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
    btn_clear_flag = tk.Button(
        frm_flags,
        text="Clear flag",
        width=15,
        relief=tk.RIDGE,
        borderwidth=2,
        bg="#c9c9c9",
        command=clear_top_flag)
    # Pack widgets
    lbl_flags_header.pack(side=tk.LEFT)
    lbl_flags_beacon.pack(side=tk.RIGHT)
    btn_clear_flag.pack(side=tk.RIGHT)

    # Setup flags frame (details) ----------------------
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
    # Create widgets
    lbx_history_details = tk.Listbox(
        frm_history_details,
        listvariable=history_details,
        bg="white",
        height=21
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

    # Additional window configuration ------------------
    # Action bindings
    job_window.bind('<ButtonPress-1>', deselect_item)

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
    global cmb_com_port
    
    # Init as tk var types (create local copy)
    com_port_local = tk.StringVar(value=com_port)
    shunt_resistor_local = tk.StringVar(value=shunt_resistor)
    decimation_local = tk.IntVar(value=decimation)
    flag_trigger_local = tk.StringVar(value=flag_trigger)

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
        # Read DATAQ
        global hooked_ports
        global hooked_port
        global dec_count
        global ser

        # Some setup before accepting new settings -----
        # End all processes related to active data collection
        collection_teardown()

        # Connect globals to locals
        com_port = com_port_local
        shunt_resistor = shunt_resistor_local
        decimation = decimation_local
        flag_trigger = flag_trigger_local

        # Extract settings -----------------------------
        # TODO: fortify validation(?)

        # Get index value of selected COM port
        com_idx = cmb_com_port.current()

        # Extract values from tk vars
        com_port = com_port.get()
        shunt_resistor = shunt_resistor.get()
        decimation = decimation.get()
        flag_trigger = flag_trigger.get()

        # Input validation
        if com_port == "" or com_port not in active_com_ports:
            retry_settings("Please select a valid COM port.")
            return
        if shunt_resistor == "":
            retry_settings("Please enter a valid shunt resistor value.")
            return
        if decimation == 0:
            retry_settings("Please enter a valid decimation factor.")
            return
        if flag_trigger == "":
            retry_settings("Please enter a valid flag trigger.")
            return

        # Setup the COM port
        hooked_port = hooked_ports[com_port]
        open_com_port(com_idx) # Hook the COM port to read from it

        # Convert tk.StringVar --> float
        shunt_resistor = float(shunt_resistor)
        flag_trigger = float(flag_trigger)

        # update dec_count with user input for decimation
        dec_count = decimation

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
        
        initial_setup = 1 # Completed at least one setup

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
    frm_okcancel = tk.Frame(
        master=settings_window,
        relief=tk.GROOVE,
        borderwidth=2,
        padx=5, pady=5) 

    # Setup com port frame -----------------------------
    # TODO: prevent deselecting COM port when selecting shunt resistor
    # Create widgets
    lbl_com_port = tk.Label(
        frm_com_port,
        text="COM Port",
        anchor="w",
        width=25)
    cmb_com_port = ttk.Combobox(
        frm_com_port,
        textvariable=com_port_local,
        values=active_com_ports,
        width=13)
    # Pack widgets
    lbl_com_port.pack(side=tk.LEFT)
    cmb_com_port.pack(side=tk.LEFT)

    # Setup shunt resistor frame -----------------------
    # Create widgets
    lbl_shunt_resistor = tk.Label(
        frm_shunt_resistor,
        text="Shunt Resistor Value",
        anchor="w",
        width=25)
    cmb_shunt_resistor = ttk.Combobox(
        frm_shunt_resistor,
        textvariable=shunt_resistor_local,
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
        textvariable=decimation_local,
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
        textvariable=flag_trigger_local,
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
    frm_okcancel.rowconfigure(0, weight=1)
    frm_okcancel.columnconfigure(0, weight=1)
    frm_okcancel.columnconfigure(1, weight=1)
    frm_okcancel.columnconfigure(2, weight=1)
    # Create widgets
    btn_ok = tk.Button(
        frm_okcancel,
        text="Ok",
        relief=tk.GROOVE,
        borderwidth=2,
        width=15,
        bg="#c9c9c9",
        command=close_okay)
    btn_cancel = tk.Button(
        frm_okcancel,
        text="Cancel",
        relief=tk.GROOVE,
        borderwidth=2,
        width=15,
        bg="#c9c9c9",
        command=settings_window.destroy)
    # Pack widgets
    btn_ok.grid(row=0, column=0, sticky="e")
    btn_cancel.grid(row=0, column=2, sticky="w")

    # Pack frames in window
    frm_com_port.pack(fill=tk.X)
    frm_shunt_resistor.pack(fill=tk.X)
    frm_decimation.pack(fill=tk.X)
    frm_flag_trigger.pack(fill=tk.X)
    frm_okcancel.pack(fill=tk.BOTH)


# # ============= Run setup and enter event loop
if __name__ == '__main__':
    setup_job_window()
    get_settings()
    job_window.after(200, check_conditions)
    job_window.after(200, update_flag_beacon)
    job_window.after(1000, update_flags_details)
    job_window.after(1000, update_com_ports)
    job_window.mainloop()