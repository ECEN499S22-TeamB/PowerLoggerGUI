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
        256-916-8954
        austinlang748@gmail.com
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
import os
import subprocess





# ============= Globals
# Windows
main_window = None
job_info_window = None

# File management
dir_path = os.path.dirname(os.path.realpath(__file__))

# Job management
year = None
job_num = None





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
    # Helper functions ---------------------------------
    def close_okay():
        """Extract the year, job_num ints and close the window."""
        global job_num          # Connect to the global variables
        global year             #
        global job_info_window  # 
        
        job_num = job_num.get()
        year = year.get()
        job_info_window.destroy()
        # print(f"job num: {job_num}") # DEBUG
        subprocess.Popen(
            ['python', dir_path+'\job_window.py', str(year), str(job_num)])
        # TODO: Improve cross-platform compatibility?

    # Connect to globals -------------------------------
    global job_info_window
    global year
    global job_num

    # Convert to tk var types
    job_num = tk.IntVar(value=0)
    year = tk.IntVar(value=0)

    # Create window ------------------------------------
    job_info_window = tk.Toplevel(main_window)
    # Configure the window -----------------------------
    job_info_window.title("Job Information")
    job_info_window.attributes('-topmost', True)
    job_info_window.geometry('400x100+10+10') # Place in upper left screen
    job_info_window.resizable(False, False)
    # Configure the window grid
    job_info_window.rowconfigure(0, weight=1)
    job_info_window.rowconfigure(1, weight=1)
    job_info_window.columnconfigure(0, weight=1)
    job_info_window.columnconfigure(1, weight=1)

    # Create frames ------------------------------------
    frm_year = tk.Frame(job_info_window, padx=5, pady=5)
    frm_job_num = tk.Frame(job_info_window, padx=5, pady=5)
    frm_okcancel = tk.Frame(job_info_window, padx=5, pady=5)

    # Configure frame grids ----------------------------
    # year entry
    frm_year.rowconfigure(0, weight=1)
    frm_year.rowconfigure(1, weight=1)
    frm_year.columnconfigure(0, weight=1)
    # job number entry
    frm_job_num.rowconfigure(0, weight=1)
    frm_job_num.rowconfigure(1, weight=1)
    frm_job_num.columnconfigure(0, weight=1)
    # ok/cancel buttons
    frm_okcancel.rowconfigure(0, weight=1)
    frm_okcancel.columnconfigure(0, weight=1)
    frm_okcancel.columnconfigure(1, weight=1)
    # Pack frames
    frm_year.grid(row=0, column=0, sticky="nsew")
    frm_job_num.grid(row=0, column=1, sticky="nsew")
    frm_okcancel.grid(row=1, column=0, sticky="nsew", columnspan=2)

    # Create widgets -----------------------------------
    # year entry
    # TODO: prevent the user from inputing a number greater than 4 digits
    lbl_year_prompt = tk.Label(
        frm_year,
        text="Please enter a job year.")
    ent_year = tk.Entry(
        frm_year,
        textvariable=year,
        relief=tk.GROOVE,
        borderwidth=2,
        width=10)
    # job number entry
    # TODO: prevent the user from inputing a number greater than 4 digits
    lbl_job_num_prompt = tk.Label(
        frm_job_num,
        text="Please enter a job number.")
    ent_job_num = tk.Entry(
        frm_job_num,
        textvariable=job_num,
        relief=tk.GROOVE,
        borderwidth=2,
        width=10)
    # okay/cancel buttons
    btn_okay = tk.Button(
        frm_okcancel,
        text="Okay",
        relief=tk.GROOVE,
        borderwidth=2,
        width=10,
        bg="#c9c9c9",
        command=close_okay)
    btn_cancel = tk.Button(
        frm_okcancel,
        text="Cancel",
        relief=tk.GROOVE,
        borderwidth=2,
        width=10,
        bg="#c9c9c9",
        command=job_info_window.destroy)

    # Pack widgets into respective frames --------------
    # year widgets
    lbl_year_prompt.grid(row=0, column=0, sticky='sew', pady=5)
    ent_year.grid(row=1, column=0, sticky='n')
    # job num widgets
    lbl_job_num_prompt.grid(row=0, column=0, sticky='sew', pady=5)
    ent_job_num.grid(row=1, column=0, sticky='n')
    # okay/cancel widgets
    btn_okay.grid(row=0, column=0, sticky="e", padx=5)
    btn_cancel.grid(row=0, column=1, sticky="w", padx=5)





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
    menu_file.add_command(label="New", command=donothing)
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