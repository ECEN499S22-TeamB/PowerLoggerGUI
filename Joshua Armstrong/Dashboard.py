import tkinter as tk
import tkinter.ttk as ttk
import os
import subprocess
from tkinter import filedialog
import csv

# ============= Globals
# Windows
main_window = None
job_num_window = None
daq_list =[]
daq_details = None
#lbl_output = None
tree_log_history = None
last_line = []
file_list = []

# File management
dir_path = os.path.dirname(os.path.realpath(__file__))

# Job management
job_num = None

def create_job():
    """Prompt the user for the job number, then open a new job."""
    # Connect to globals -------------------------------
    global job_num_window
    global job_num # Connect to the global variable
    # Convert to tk var types
    job_num = tk.IntVar(value=0)

    # Helper functions ---------------------------------
    def close_okay():
        """Extract the job_num int and close the window."""
        global job_num          # Connect to the global variables
        global job_num_window   # 
        
        job_num = job_num.get()
        job_num_window.destroy()
        # print(f"job num: {job_num}") # DEBUG
        subprocess.Popen(
            ['python', dir_path+'\job_window (Josh).py', str(job_num)])
        # TODO: Improve cross-platform compatibility?
        # TODO: change file name to the correct file.

    # Create window ------------------------------------
    job_num_window = tk.Toplevel(main_window)
    # Configure the window -----------------------------
    job_num_window.title("Enter a job number.")
    job_num_window.attributes('-topmost', True)
    job_num_window.geometry('300x75+10+10') # Place in upper left screen
    job_num_window.resizable(False, False)
    # Configure the window grid
    job_num_window.rowconfigure(0, weight=1)
    job_num_window.rowconfigure(1, weight=1)
    job_num_window.rowconfigure(2, weight=1)
    job_num_window.columnconfigure(0, weight=1)

    # Create frame -------------------------------------
    frm_okcancel = tk.Frame(job_num_window, padx=5, pady=5)
    # Configure frame grid
    frm_okcancel.rowconfigure(0, weight=1)
    frm_okcancel.columnconfigure(0, weight=1)
    frm_okcancel.columnconfigure(1, weight=1)
    frm_okcancel.columnconfigure(2, weight=1)
    # Pack frame
    frm_okcancel.grid(row=2, column=0, sticky='nsew')

    # Create widgets -----------------------------------
    lbl_prompt = tk.Label(
        job_num_window,
        text="Please enter a job number.")
    ent_job_num = tk.Entry(
        job_num_window,
        textvariable=job_num,
        relief=tk.GROOVE,
        borderwidth=2,
        width=15)
    btn_okay = tk.Button(
        frm_okcancel,
        text="Okay",
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
        command=job_num_window.destroy)
    # Pack widgets
    lbl_prompt.grid(row=0, column=0, sticky='sew')
    ent_job_num.grid(row=1, column=0, sticky='n')
    btn_okay.grid(row=0, column=0, sticky='e')
    btn_cancel.grid(row=0, column=2, sticky='w')

def load_project():
    global file_list
    global last_line

    """Open a file for editing."""
    filepath = filedialog.askopenfilename()
    file_list.append(filepath)
    last_line.append("V")



def active_window():
        subprocess.Popen(
            ['python', dir_path+'\Active_Window.py'])
        # TODO: Improve cross-platform compatibility?
        # TODO: change file name to the correct file.


# TODO: Replace with real logging code
# For Testing
#-----------------------------------------------------------------------
def log_history(i=0):
    """Update the flags details listbox."""

    global last_line
    global file_list

    number_of_file = 0
    number_of_file = len(file_list)

    for i in range(number_of_file):
        with open(file_list[i], 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)
            # Get the last line of the file
            for line in csv_file:
                pass
            if line != last_line[i]:
                last_line[i] = line
                
                # Split the line into variables
                time_and_data, resister, V1, V2, V3, V4, amp, CSV_flag = last_line[i].split(',')

                voltage = float(V2)
                current = float(amp)

                global tree_log_history
                # Construct the output strings ---------------------
                # DateTime
                #now = datetime.datetime.now()
                #dt_string = now.strftime("%m/%d/%Y %H:%M:%S.%f")[:-3] # mm/dd/YY H:M:S.mS
                # Channel readings
                # TODO: fix text alignment (-'s seem to be the problem)
                ch_string = f"{voltage:>7.3f} V, " 
                # Device levels
                lvls_string =f"{current:>7.3f} A"

                # Format output and add to widget ------------------
                # Find the tag for this entry (for formatting row color)
                tag="acquiring"
                back_color="white"
                text_color="green"

                # Need how to change how Flag value are store
                """
                if CSV_flag == 0:
                    tag="flag0"
                    text_color="red"
                if CSV_flag == 1:
                    tag="flag1"
                    text_color="orange"
                elif CSV_flag == 2:
                    tag="flag2"
                    text_color="yellow"
                """
                job_name = os.path.basename(csv_file.name)
                job_name_wo_ext = os.path.splitext(job_name)[0]

                # Insert values in next row
                tree_log_history.insert('', 'end', text=job_name_wo_ext,
                    values=(time_and_data ,ch_string, lvls_string),
                    tags=[tag])

                # Format row color
                tree_log_history.tag_configure(tag, foreground=text_color, background=back_color)
                csv_file.close()
            else:
                pass

    window.after(1000, log_history)

def menu():
    #setting for File menu
    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)

    #filemenu.add_command(label="New", command=donothing)
    #filemenu.add_command(label="Open", command=donothing)
    #filemenu.add_command(label="Save", command=donothing)
    #filemenu.add_separator()

    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    #helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    #Pack the menu
    window.config(menu=menubar)

def donothing():
    """Test function that does nothing."""
    x = 0

def setup():
    window.title("Dashboard")
    window.geometry('890x780+0+0') 
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.resizable(False, False)

    style = ttk.Style(window)
    style.theme_use('clam')

    if window.getvar('tk_patchLevel')=='8.6.9': #and OS_Name=='nt':
        def fixed_map(option):
            """
            Fix for setting text colour for Tkinter 8.6.9
            From: https://core.tcl.tk/tk/info/509cafafae
            
            Returns the style map for 'option' with any styles starting with
            ('!disabled', '!selected', ...) filtered out.
            
            style.map() returns an empty list for missing options, so this
            should be future-safe.
            """
            return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))  

    # Create widgets
    global daq_details
    #global lbl_output
    global tree_log_history

    frm_output = tk.Frame(
        window,
        relief=tk.GROOVE,
        borderwidth=2)
    tree_log_history = ttk.Treeview(
        frm_output,
        columns=('Job Name', 'Date & Time', 'Voltage', 'Current'),
        height=30)

    tree_log_history.heading('#0', text="Job Name")
    tree_log_history.heading('#1', text="Date & Time")
    tree_log_history.heading('#2', text="Voltage")
    tree_log_history.heading('#3', text="Current")
    tree_log_history.column('#0', minwidth=190, width=190, stretch=False)
    tree_log_history.column('#1', minwidth=226, width=226, stretch=False)
    tree_log_history.column('#2', minwidth=170, width=170, stretch=False)
    tree_log_history.column('#3', minwidth=171, width=171, stretch=False)

    frm_buttons = tk.Frame(
        window,
        relief=tk.RAISED,
        bd=2)
    btn_open = tk.Button(
        frm_buttons,
        width= 12, 
        height=3, 
        text="New Project", 
        command=create_job)
    btn_save = tk.Button(
        frm_buttons, 
        width= 12, 
        height=3, 
        text="Load Project", 
        command= load_project)
    btn_active = tk.Button(
        frm_buttons, 
        width= 12, 
        height=3,  
        text="Active Window", 
        command=active_window)
    """
    btn_scoll_toggle = tk.Button(
        frm_output, 
        width= 14, 
        height=1,  
        text="Toggle Auto Scoll", 
        command=donothing)
    """

    bar_output = tk.Scrollbar(
        tree_log_history, 
        orient=tk.VERTICAL)

    bar_output.config(command=tree_log_history.yview)
    tree_log_history.config(yscrollcommand = bar_output.set)

    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=20)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=20)
    btn_active.grid(row=2, column=0, sticky="ew", padx=5, pady=20)
    #btn_scoll_toggle.pack(side=tk.TOP, anchor='e')
    tree_log_history.pack(side=tk.TOP, anchor="nw", fill='both', expand=1)
    bar_output.pack(side="right", fill="y")

    frm_buttons.grid(row=0, column=0, sticky="ns")
    frm_output.grid(row=0, column=1, sticky="nsew")

    menu()


if __name__ == '__main__':
    window = tk.Tk()
    setup()
    window.after(1000, log_history)
    window.mainloop()