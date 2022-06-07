# Imports
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import HORIZONTAL, ttk
from tkinter import messagebox
from random import randint

# Get the System time
from time import strftime

#RTSxx(year)-Jxxxx(job number)
#Example: RTS21-J0123
#Year 2021, Job 123


# ============= Top level setup
window = tk.Tk()
window.title("Power Logger")

#Set the size of the window
#window.geometry('1280x720')

#set row and column. needs reworking
window.columnconfigure(1, weight= 1, minsize=75)
window.rowconfigure(4, weight= 1, minsize=50)

<<<<<<< HEAD
=======
def core():
    Newbutton = tk.Button(text= "New Project", width=11, height=3 , command=new_project)
    loadbutton = tk.Button(text= "Load Project", width=11, height=3 , command=load_project)
    Settingbutton = tk.Button(text= "System Setting", width=11, height=3 , command=Data)
    Quitbutton = tk.Button(text= "Quit", width=10, height=3 , command=window.quit)
    Newbutton.grid(row=0, column=0, padx=50, pady=30,)
    loadbutton.grid(row=0, column=1, padx=50, pady=30,)
    Settingbutton.grid(row=1, column=0, padx=50, pady=30,)
    Quitbutton.grid(row=1, column=1, padx=50, pady=30,)
>>>>>>> origin/master

# ============= Globals
#set inital Voltage and Current texts
Voltnum = randint(0,5)
Currentnum = randint(0,5)

#DAQVoltage = ----

Voltage = tk.IntVar()
Voltage.set(f"Voltage = 5 V\n \n dV/dt = {Voltnum} V")

Current = tk.IntVar()
Current.set(f"Current = 5 A\n \n dI/dt = {Currentnum} A")


# ============= Event handlers
#
# core
#
def core():
    """Creates the contents of the main menu window."""
    Newbutton = tk.Button(text= "New Project", width=11, height=3 , command=Data)
    loadbutton = tk.Button(text= "Load Project", width=11, height=3 , command=Data)
    Settingbutton = tk.Button(text= "System Setting", width=11, height=3 , command=Data)
    Quitbutton = tk.Button(text= "Quit", width=10, height=3 , command=window.quit)
    Newbutton.grid(row=0, column=0, padx=50, pady=30,)
    loadbutton.grid(row=0, column=1, padx=50, pady=30,)
    Settingbutton.grid(row=1, column=0, padx=50, pady=30,)
    Quitbutton.grid(row=1, column=1, padx=50, pady=30,)

#
# Data
#
def Data():
    """Creates the contents of the data window (project window)."""
    Data = tk.Toplevel(window)
    Data.columnconfigure(2, weight= 1, minsize=75)
    Data.rowconfigure(5, weight= 1, minsize=50)

    Data.title("Data window")

    time = strftime('%H:%M:%S %p')

    Project_name = tk.Label(Data, text= "Project Name")
    Project_name.grid(row=0, column=0, columnspan=3, sticky='n')

    Vframe =tk.Frame(Data,)
    Vframe.columnconfigure(0, weight=1)
    Vframe.grid(row=0, column=0, padx=20, pady=20)

    Voltage_label = tk.Label(Vframe, textvariable=Voltage)
    Voltage_label.grid(row=0, column=0, padx=20, pady=20)

    #relief=tk.SUNKEN, borderwidth= 2, height= 15, width=30,

    Cframe =tk.Frame(Data)
    Cframe.columnconfigure(0, weight=1)
    Cframe.grid(row=0, column=1, padx=20, pady=20)

    Current_label = tk.Label(Cframe, textvariable=Current)
    Current_label.grid(row=0, column=1, columnspan=2, padx=20, pady=20,)
    
    Fframe =tk.Frame(Data)
    Fframe.grid(row=1, rowspan=3, column=0, padx=20, pady=20)

    Flag_label = tk.Label(Fframe, text="Flags")
    Flag_label.grid(row=1, column=0, padx=20, pady=5,)
    Flagbox = tk.Listbox(Fframe, relief=tk.SUNKEN, width=35, height=3)
    Flagbox.grid(row=2, column=0,  sticky='n')

    def change_color():
        current_color = Flagbox_light.cget("background")
        if current_color == "red":
            next_color = "white"  
        else:
            next_color = "red"
        Flagbox_light.config(background=next_color)
        window.after(200, change_color)

    Flagbox_light = tk.Label(Fframe, background="red", width=4, relief=tk.SUNKEN)
    Flagbox_light.grid(row=1, column=0, sticky='e', padx=0, pady=0)

    change_color()

    Log_button = tk.Button(Fframe, text="Log", command=donothing, width=4,)
    Log_button.grid(row=3, column=0, sticky='w')

    clear_error = tk.Button(Fframe, text="Clear Error", command=donothing,)
    clear_error.grid(row=3, column=0, sticky='e')

    Flagbox.insert(1, f"An error has occurred at {time}")
<<<<<<< HEAD

=======
    
>>>>>>> origin/master
    if Currentnum == 3:
        #change this back to 0 after Testing
        i = 1 
        i += 1
        print(Currentnum)
        Flagbox.insert(i, f"An error has occurred at {time}")

    Flagbox.update()

<<<<<<< HEAD
    Resister_label = tk.Label(Data, text="Resister")
    Resister_label.grid(row=1, column=1, padx=20, pady=10, sticky='n')
    Resister_entry = tk.Entry(Data, bd=5)
    Resister_entry.grid(row=2, column=1, sticky='n')
=======
    RSframe =tk.Frame(Data)
    RSframe.grid(row=1, rowspan=4, column=1, columnspan=2, padx=20, pady=20)

    Resister_label = tk.Label(RSframe, text="Resistor (Ohms)")
    Resister_label.grid(row=1, column=1, columnspan=2, padx=20, pady=10, sticky='n')
>>>>>>> origin/master

    R = tk.IntVar()

    Resister_value = ttk.Combobox(RSframe, text = R)
    Resister_value['values'] = (
        1,
        10,
        100,
        1000,
        10000,
        'Other'
        )

    Resister_value.current()
    Resister_value.grid(row=2, column=1, columnspan=2, padx=10, sticky='n')

    Sampling_label = tk.Label(RSframe, text="Sampling (Hz)")
    Sampling_label.grid(row=3, column=1, columnspan=2, padx=20, pady=3, sticky='n')
    Sampling_entry = tk.Entry(RSframe, bd=5)
    Sampling_entry.grid(row=4, column=1, columnspan=2, padx=20, pady=1, sticky='n')
    
    barFrame = tk.Frame(Data)
    barFrame.grid(row=5, column=0, columnspan=1)

    statusbar = ttk.Progressbar(barFrame, orient=HORIZONTAL, length= 100, mode='indeterminate')
    statusbar.pack(anchor=tk.E, fill='x')

    Sampling_button = tk.Button(RSframe, text="Submit", command=statusbar.start(10))
    #Sampling_button.grid(row=4, column=2, pady=2, sticky='e')
    Sampling_rate = tk.Label(RSframe, text=f"Current Sample Rate: ")
    Sampling_rate.grid(row=4, column=1, columnspan=2, pady=25, sticky="s")

    menubar = tk.Menu(Data)
    filemenu = tk.Menu(Data, menubar, tearoff=0)
    systemMenu = tk.Menu(Data, menubar, tearoff=0)
    logmenu = tk.Menu(Data, menubar, tearoff=0)
    filemenu.add_command(label="Open Main menu", command=core)
    systemMenu.add_command(label="System Setting", command=donothing)
    systemMenu.add_command(label="Log", command=donothing)
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="System", menu=systemMenu)

    Data.config(menu=menubar)

<<<<<<< HEAD
#
# update
#
=======
def new_project():
    nProject = tk.Toplevel(window)
    nProject.columnconfigure(1, weight= 1, minsize=75)
    nProject.rowconfigure(1, weight= 1, minsize=50)

    nProject.title("New Project")
    nProject.geometry('400x200')
    name_label = tk.Label(nProject, text="Project name")
    name_label.grid(column=0, row=0)

    name = tk.StringVar()

    name_entry = tk.Entry(nProject, textvariable=name, width=33)
    name_entry.grid(column=1, row=0, padx=10, pady=10)

    port_Labet = tk.Label(nProject,  text= "COM Number")
    Com_number = tk.StringVar()

    Com_value = ttk.Combobox(nProject, width=30, text = Com_number)
    Com_value['values'] = (
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5"
        )

    port_Labet.grid(column=0, row=1, padx=10, pady=10)
    Com_value.grid(column=1, row=1, padx=10, pady=10)

    ok_button = tk.Button(nProject, text="OK", width= 5, command=lambda:[Data(), close()])
    ok_button.grid(column=1, row=2, sticky='w', padx=10, pady=10)

    cancel_button = tk.Button(nProject, text="Cancel", command=nProject.destroy)
    cancel_button.grid(column=1, row=2, sticky='n', padx=10, pady=10)

    def close():
        nProject.destroy
    

def load_project():
    #file_types = ('text files', '*.txt')
    file_name = fd.askopenfilename(
        title= "Open Project",
        initialdir='/',
        )
        #filetypes= file_types)


#update the data or Voltage and current
>>>>>>> origin/master
def update():
    """Update the data or Voltage and current"""
    Voltnum = randint(0,5)
    Currentnum = randint(0,5)
    Voltage.set(f"Voltage = 5 V\n \n dV/dt = {Voltnum} V")
    Current.set(f"Current = 5 A\n \n dI/dt = {Currentnum} A")
    window.after(1000, update)

#
# donothing
#
def donothing():
    """Test function."""
    messagebox.showinfo('Error', 'No function.')

#
# flag_window
#
def flag_Window():
    """Setting for flag window"""
    Flags = tk.Toplevel(window)
    Flags.geometry("250x250")
    Flags.title("Flag Setting")

#
# Sampling_Window
#
def Sampling_Window():
    """Setting for Sampling Window"""
    Sampling = tk.Toplevel(window)
    Sampling.geometry("250x250")
    Sampling.title("Sapling Setting")
    #The Sampling in the label set ownership to the new window
    text = tk.Label(Sampling, text="Text")
    text.grid(row = 0, column = 0)
    entry = tk.Entry(Sampling, bd = 5)
    entry.grid(row = 0, column = 1)

#
# menu
#
def menu():
    """Setting for File menu"""
    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    #setting for sampling menu
    #samplingmenu = tk.Menu(menubar, tearoff=0)
    #samplingmenu.add_command(label="Sampling Rates", command=Sampling_Window)
    #menubar.add_cascade(label="Sampling", menu=samplingmenu)

    #setting for flag menu
    #flagmenu = tk.Menu(menubar, tearoff=0)
    #flagmenu.add_command(label="Flags Settings", command=flag_Window)
    #menubar.add_cascade(label="Flags", menu=flagmenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    menubar.add_cascade(label="Help", menu=helpmenu)

    #Pack the menu
    window.config(menu=menubar)


<<<<<<< HEAD
# ========= Perform setup, then enter the main program loop
=======

#runs the update
>>>>>>> origin/master
menu()
update()
core()

window.mainloop()