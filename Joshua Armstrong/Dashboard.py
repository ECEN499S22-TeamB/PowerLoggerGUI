import tkinter as tk
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


#def save_file():
#    """Save the current file as a new file."""
#    filepath = asksaveasfilename(
#        defaultextension=".txt",
#        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
#    )
#    if not filepath:
#        return
#    with open(filepath, mode="w", encoding="utf-8") as output_file:
#        text = txt_edit.get("1.0", tk.END)
#        output_file.write(text)
#    window.title(f"Simple Text Editor - {filepath}")


def widget():

    #testing
    #daq_log = []
    #daq = tk.StringVar(daq_log)
    
    y = 0
    for i in range(0 , 100):
        if i == 100:
            #daq_log.append(f"Daq Data{y} logging...")
            y += 1
            i = 0

    # Create widgets
    lbl_output = tk.Label(window, bg="white",)# text=f"daq")
    frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(frm_buttons, width= 12, height=3, text="New Project", command=create_job)
    btn_save = tk.Button(frm_buttons, width= 12, height=3, text="Load Project",)
    btn_active = tk.Button(frm_buttons, width= 12, height=3,  text="Active Window",)

    # Assign buttons to frame
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=20)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=20)
    btn_active.grid(row=2, column=0, sticky="ew", padx=5, pady=20)

    # Setup window grid layout
    frm_buttons.grid(row=0, column=0, sticky="ns")
    lbl_output.grid(row=0, column=1, sticky="nsew")

    window.after(1000, widget)



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
    window.geometry('960x1080+0+0') 
    window.columnconfigure(1, minsize=800, weight=1)
    window.rowconfigure(0, minsize=800, weight=1)
    window.resizable(False, False) 

    menu()


if __name__ == '__main__':
    window = tk.Tk()
    setup()
    widget()
    window.mainloop()