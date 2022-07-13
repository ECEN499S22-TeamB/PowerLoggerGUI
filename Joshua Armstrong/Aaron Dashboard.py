"""
dashboard.py
This script will launch the Power Logger dashboard.
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
from tkinter import messagebox
from tkinter import filedialog
import os
import subprocess


# ============= Globals
# Windows
main_window = None
job_num_window = None

# File management
dir_path = os.path.dirname(os.path.realpath(__file__))

# Job management
job_num = None

# File Path
file_path = None


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
    """Confirm the user wants to close the main window."""
    if messagebox.askokcancel(
        message="Are you sure you want to close the window?", 
        icon='warning', title="Please confirm."):
        main_window.destroy()

#
# create_job
#
def create_job():
    """Prompt the user for the job number, then open a new job."""
    # Connect to globals -------------------------------
    global job_num_window
    # global job_num # Connect to the global variable
    # Convert to tk var types
    # job_num = tk.IntVar(value=0)

    # Prompt for a file path
    file_path = filedialog.askopenfilename()
    subprocess.Popen(
            ['python', dir_path+'\GUI(Austin ver).py', str(file_path)])

def dashboard():
    subprocess.Popen(
            ['python', dir_path+'\Dashboard.py', str(file_path)])


    # Helper functions ---------------------------------
    def close_okay():
        """Extract the job_num int and close the window."""
        global job_num          # Connect to the global variables
        global job_num_window   # 
        
        job_num_window.destroy()
        # print(f"job num: {job_num}") # DEBUG
        
        # TODO: Improve cross-platform compatibility?

    # Create window ------------------------------------
     #job_num_window = tk.Toplevel(main_window)
    # Configure the window -----------------------------
    # job_num_window.title("Enter a job number.")
    # job_num_window.attributes('-topmost', True)
    # job_num_window.geometry('300x75+10+10') # Place in upper left screen
    # job_num_window.resizable(False, False)
    # # Configure the window grid
    # job_num_window.rowconfigure(0, weight=1)
    # job_num_window.rowconfigure(1, weight=1)
    # job_num_window.rowconfigure(2, weight=1)
    # job_num_window.columnconfigure(0, weight=1)

    # # Create frame -------------------------------------
    # frm_okcancel = tk.Frame(job_num_window, padx=5, pady=5)
    # # Configure frame grid
    # frm_okcancel.rowconfigure(0, weight=1)
    # frm_okcancel.columnconfigure(0, weight=1)
    # frm_okcancel.columnconfigure(1, weight=1)
    # frm_okcancel.columnconfigure(2, weight=1)
    # # Pack frame
    # frm_okcancel.grid(row=2, column=0, sticky='nsew')

    # # Create widgets -----------------------------------
    # # TODO: prevent the user from inputing a number greater than 4 digits
    # lbl_prompt = tk.Label(
    #     job_num_window,
    #     text="Please enter a job number.")
    # ent_job_num = tk.Entry(
    #     job_num_window,
    #     textvariable=job_num,
    #     relief=tk.GROOVE,
    #     borderwidth=2,
    #     width=15)
    # btn_okay = tk.Button(
    #     frm_okcancel,
    #     text="Okay",
    #     relief=tk.GROOVE,
    #     borderwidth=2,
    #     width=15,
    #     bg="#c9c9c9",
    #     command=close_okay)
    # btn_cancel = tk.Button(
    #     frm_okcancel,
    #     text="Cancel",
    #     relief=tk.GROOVE,
    #     borderwidth=2,
    #     width=15,
    #     bg="#c9c9c9",
    #     command=job_num_window.destroy)
    # # Pack widgets
    # lbl_prompt.grid(row=0, column=0, sticky='sew')
    # ent_job_num.grid(row=1, column=0, sticky='n')
    # btn_okay.grid(row=0, column=0, sticky='e')
    # btn_cancel.grid(row=0, column=2, sticky='w')


# ============= Setup visuals
# 
# setup
#
def setup_main_window():
    """Setup the main_window GUI."""
    global main_window # Connect to the global variable
    # Configure the main_window
    main_window.title("Power Logger: Main Menu")
    main_window.geometry('600x200+10+10')
    main_window.resizable(False, False)  # Don't window resizable

    # Configure the main_window grid
    main_window.columnconfigure(0, minsize=300, weight=1)
    main_window.columnconfigure(1, minsize=300, weight=1)
    main_window.rowconfigure(0, minsize=100, weight=1)
    main_window.rowconfigure(1, minsize=100, weight=1)

    # Create button widgets
    btn_new = tk.Button(main_window, text="New Job", relief=tk.RIDGE, borderwidth=10, command=create_job)
    btn_load = tk.Button(main_window, text="Load Job", relief=tk.RIDGE, borderwidth=10)
    btn_settings = tk.Button(main_window, text="System Settings", relief=tk.RIDGE, borderwidth=10)
    btn_quit = tk.Button(main_window, text="Quit", relief=tk.RIDGE, borderwidth=10, command=ask_close)

    # Place button widgets on grid
    btn_new.grid(row=0, column=0, sticky="nsew")
    btn_load.grid(row=0, column=1, sticky="nsew")
    btn_settings.grid(row=1, column=0, sticky="nsew")
    btn_quit.grid(row=1, column=1, sticky="nsew")

    # Create the File menu widget
    menubar = tk.Menu(main_window)   # Create the menubar
    menu_file = tk.Menu(menubar, tearoff=0)
    menu_file.add_command(label="New", command=dashboard)
    menu_file.add_command(label="Open", command=donothing)
    menu_file.add_command(label="Save", command=donothing)
    menu_file.add_separator()
    menu_file.add_command(label="Exit", command=ask_close)
    menubar.add_cascade(label="File", menu=menu_file)

    # Create the Help menu widget
    menu_help = tk.Menu(menubar, tearoff=0)
    menu_help.add_command(label="Help Index", command=donothing)
    menu_help.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=menu_help)

    # Pack the menu widgets
    main_window['menu'] = menubar

    # Intercept the close button
    main_window.protocol("WM_DELETE_WINDOW", ask_close)


# ============= Run setup and enter event loop
if __name__ == '__main__':
    main_window = tk.Tk() # Create a new main_window
    setup_main_window()
    main_window.mainloop()