import tkinter as tk
from random import randint
from tkinter import messagebox

#get the System time
from time import strftime

#RTSxx(year)-Jxxxx(job number)
#Example: RTS21-J0123
#Year 2021, Job 123

window = tk.Tk()
window.title("Power Logger")

#Set the size of the window
#window.geometry('1280x720')

#set row and column. needs reworking
window.columnconfigure(1, weight= 1, minsize=75)
window.rowconfigure(4, weight= 1, minsize=50)

def core():
    Newbutton = tk.Button(text= "New Project", width=11, height=3 , command=Data)
    loadbutton = tk.Button(text= "Load Project", width=11, height=3 , command=Data)
    Settingbutton = tk.Button(text= "System Setting", width=11, height=3 , command=Data)
    Quitbutton = tk.Button(text= "Quit", width=10, height=3 , command=window.quit)
    Newbutton.grid(row=0, column=0, padx=50, pady=30,)
    loadbutton.grid(row=0, column=1, padx=50, pady=30,)
    Settingbutton.grid(row=1, column=0, padx=50, pady=30,)
    Quitbutton.grid(row=1, column=1, padx=50, pady=30,)

#set inital Voltage and Current texts
Voltnum = randint(0,5)
Currentnum = randint(0,5)

Voltage = tk.StringVar()
Voltage.set(f"Voltage = 5 V\n \n dV/dt = {Voltnum} V")

Current = tk.StringVar()
Current.set(f"Current = 5 A\n \n dC/dt = {Currentnum} A")

#side = tk.LEFT

def Data():
    Data = tk.Toplevel(window)
    Data.title("Data window")

    time = strftime('%H:%M:%S %p')

    Voltage_label = tk.Label(Data, textvariable=Voltage)
    Voltage_label.grid(row=0, column=0, padx=20, pady=20)

    Current_label = tk.Label(Data, textvariable=Current)
    Current_label.config(text=Current.get())
    Current_label.grid(row=0, column=1, padx=20, pady=20,)

    Flag_label = tk.Label(Data, text="Flags")
    Flag_label.grid(row=1, column=0, padx=20, pady=5,)
    Flagbox = tk.Listbox(Data, relief=tk.SUNKEN, width=33, height=3)
    Flagbox.grid(row=2, column=0, sticky='n')

    Flagbox.insert(1, f"An error has occurred at {time}")

    
    if Currentnum == 3:
        #change this back to 0 after Testing
        i = 1 
        i += 1
        print(Currentnum)
        Flagbox.insert(i, f"An error has occurred at {time}")

    Flagbox.update()


    Resister_label = tk.Label(Data, text="Resister")
    Resister_label.grid(row=1, column=1, padx=20, pady=10, sticky='n')
    Resister_entry = tk.Entry(Data, bd=5)
    Resister_entry.grid(row=2, column=1, sticky='n')

    Sampling_label = tk.Label(Data, text="Sampling")
    Sampling_label.grid(row=3, column=1, padx=20, pady=3, sticky='n')
    Sampling_entry = tk.Entry(Data, bd=5)
    Sampling_entry.grid(row=4, column=1, sticky='n')

    menubar = tk.Menu(Data)
    filemenu = tk.Menu(Data, menubar, tearoff=0)
    filemenu.add_command(label="Open Main menu", command=core)
    menubar.add_cascade(label="File", menu=filemenu)

    Data.config(menu=menubar)

#update the data or Voltage and current
def update():
    Voltnum = randint(0,5)
    Currentnum = randint(0,5)
    Voltage.set(f"Voltage = 5 V\n \n dV/dt = {Voltnum} V")
    Current.set(f"Current = 5 A\n \n dC/dt = {Currentnum} A")
    window.after(1000, update)

#test function
def donothing():
    messagebox.showinfo('Error', 'No function.')

#setting for flag window
def flag_Window():
    Flags = tk.Toplevel(window)
    Flags.geometry("250x250")
    Flags.title("Flag Setting")

#setting for Sampling Window
def Sampling_Window():
    Sampling = tk.Toplevel(window)
    Sampling.geometry("250x250")
    Sampling.title("Sapling Setting")
    #The Sampling in the label set ownership to the new window
    text = tk.Label(Sampling, text="Text")
    text.grid(row = 0, column = 0)
    entry = tk.Entry(Sampling, bd = 5)
    entry.grid(row = 0, column = 1)

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

#runs the update
menu()
update()
core()

window.mainloop()