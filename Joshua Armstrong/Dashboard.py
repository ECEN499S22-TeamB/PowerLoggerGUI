import tkinter as tk
import os
import subprocess
from tkinter import filedialog as fd

# ============= Globals
# Windows
main_window = None
job_num_window = None
daq_list =[]
daq_details = None
lbl_output = None

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
    """Open a file for editing."""
    filepath = fd.askopenfilename(
        filetypes=[('Text Files', "*.txt"), ("All Files", "*.*")],
    )

def active_window():
        subprocess.Popen(
            ['python', dir_path+'\Active_Window.py'])
        # TODO: Improve cross-platform compatibility?
        # TODO: change file name to the correct file.


def widget():
    # Create widgets
    global daq_details
    global lbl_output

    frm_output = tk.Frame(window, relief=tk.GROOVE, borderwidth=2)
    lbl_output = tk.Listbox(frm_output, bg="white", listvariable=daq_details) 
    frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(frm_buttons, width= 12, height=3, text="New Project", command=create_job)
    btn_save = tk.Button(frm_buttons, width= 12, height=3, text="Load Project", command= load_project)
    btn_active = tk.Button(frm_buttons, width= 12, height=3,  text="Active Window", command=active_window)
    bar_output = tk.Scrollbar(lbl_output, orient=tk.VERTICAL)
    bar_output.config(command=lbl_output.yview)
    lbl_output.config(yscrollcommand = bar_output.set)

    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=20)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=20)
    btn_active.grid(row=2, column=0, sticky="ew", padx=5, pady=20)
    lbl_output.pack(side=tk.TOP, anchor="nw", fill='both', expand=1)
    bar_output.pack(side="right", fill="y")

    frm_buttons.grid(row=0, column=0, sticky="ns")
    frm_output.grid(row=0, column=1, sticky="nsew")

# TODO: Replace with real logging code
# For Testing
#-----------------------------------------------------------------------
def log_history(i=0):
    """Update the flags details listbox."""
    global daq_list        # Connect to the global variables
    global daq_details     #
    global lbl_output #

    # Update the listbox
    daq_list.append(f"ERROR{i}\n") # DEBUG
    i += 1 # DEBUG
    if not daq_details:
        daq_details = tk.StringVar(value=daq_list)
    else:
        daq_details.set(daq_list)
    lbl_output['listvariable'] = daq_details # Update the widget

    # Decide how to focus the listbox
    lbl_output.see("end") # Keep latest output in view
    # If user has made a selection, keep it visible
    idxs = lbl_output.curselection()
    if len(idxs)==1:
            idx = lbl_output.curselection()
            lbl_output.selection_set(idx)
            lbl_output.see(idx)
    window.after(1000, log_history, i)
    #-----------------------------------------------------------------------


def menu():
    #setting for File menu
    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    #Pack the menu
    window.config(menu=menubar)

def donothing():
    """Test function that does nothing."""
    x = 0

def setup():
    window.title("Dashboard")
    window.geometry('960x750+0+0') 
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.resizable(False, False) 

    menu()


if __name__ == '__main__':
    window = tk.Tk()
    setup()
    widget()
    window.after(1000, log_history)
    window.mainloop()