import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import messagebox
from random import randint

#get the System time
from time import strftime

import serial
import serial.tools.list_ports
import keyboard
import time

""" 
Example slist for model DI-1100
0x0000 = Analog channel 0, ±10 V range
0x0001 = Analog channel 1, ±10 V range
0x0002 = Analog channel 2, ±10 V range
0x0003 = Analog channel 3, ±10 V range
"""
slist = [0x0000,0x0001,0x0002,0x0003]

ser=serial.Serial()

"""
Since model DI-1100 cannot scan slower that 915 Hz at the protocol level, 
and that rate or higher is not practical for this program, define a decimation 
factor to slow scan rate to a practical level. It defines the number of analog readings to average
before displaying them. By design, digital input values display instantaneously
without averaging at the same rate as decimated analog values.
Averaging n values on each analog channel is more difficult than simply using
every nth value, but is recommended since it reduces noise by a factor of n^0.5 
'decimation_factor' must be an integer value greater than zero. 
'decimation_factor' = 1 disables decimation and attemps to output all values.
"""
# Define a decimation factor variable
decimation_factor = 1000

# Contains accumulated values for each analog channel used for the average calculation
achan_accumulation_table = list(())

# Define flag to indicate if acquiring is active 
acquiring = False

""" Discover DATAQ Instruments devices and models.  Note that if multiple devices are connected, only the 
device discovered first is used. We leave it to you to ensure that it's a DI-1100."""
def discovery():
    # Get a list of active com ports to scan for possible DATAQ Instruments devices
    available_ports = list(serial.tools.list_ports.comports())
    # Will eventually hold the com port of the detected device, if any
    hooked_port = "" 
    for p in available_ports:
        # Do we have a DATAQ Instruments device?
        if ("VID:PID=0683" in p.hwid):
            # Yes!  Dectect and assign the hooked com port
            hooked_port = p.device
            break

    if hooked_port:
        print("Found a DATAQ Instruments device on",hooked_port)
        ser.timeout = 0
        ser.port = hooked_port
        ser.baudrate = '115200'
        ser.open()
        return(True)
    else:
        # Get here if no DATAQ Instruments devices are detected
        print("Please connect a DATAQ Instruments device")
        input("Press ENTER to try again...")
        return(False)

                # Decimation loop NOT finished and NOT first slist position
                # Nothing to do except add the value to the accumlator
                achan_accumulation_table[achan_number] = result + achan_accumulation_table[achan_number]
                achan_number += 1

            # Get the next position in slist
            slist_pointer += 1

            if (slist_pointer + 1) > (len(slist)):
                # End of a pass through slist items
                if dec_count == 1:
                    # Get here if decimation loop has finished
                    dec_count = decimation_factor
                    # Reset analog channel accumulators to zero
                    achan_accumulation_table = [0] * len(achan_accumulation_table)
                    # Append digital inputs to output string
                    output_string = output_string + "{: 3d}, ".format(dig_in)
                    print(output_string.rstrip(", ") + "           ", end="\r") 
                    output_string = ""
                else:
                    dec_count -= 1             
                slist_pointer = 0
                achan_number = 0
ser.close()
SystemExit







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
    Newbutton = tk.Button(text= "New Project", width=11, height=3 , command=new_project)
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

#DAQVoltage = ----

Voltage = tk.IntVar()
Voltage.set(f"Voltage = 5 V\n \n dV/dt = {Voltnum} V")

Current = tk.IntVar()
Current.set(f"Current = 5 A\n \n dI/dt = {Currentnum} A")

def Data():
    Data = tk.Toplevel(window)
    Data.columnconfigure(2, weight= 1, minsize=75)
    Data.rowconfigure(5, weight= 1, minsize=50)

    Data.title("Data window")

    time = strftime('%H:%M:%S %p')

    Voltage_label = tk.Label(Data, textvariable=Voltage)
    Voltage_label.grid(row=0, column=0, padx=20, pady=20)

    Current_label = tk.Label(Data, textvariable=Current)
    Current_label.grid(row=0, column=1, columnspan=2, padx=20, pady=20,)

    Flag_label = tk.Label(Data, text="Flags")
    Flag_label.grid(row=1, column=0, padx=20, pady=5,)
    Flagbox = tk.Listbox(Data, relief=tk.SUNKEN, width=35, height=3)
    Flagbox.grid(row=2, column=0,  sticky='n')

    Flagbox.insert(1, f"An error has occurred at {time}")
    
    if Currentnum == 3:
        #change this back to 0 after Testing
        i = 1 
        i += 1
        print(Currentnum)
        Flagbox.insert(i, f"An error has occurred at {time}")

    Flagbox.update()

    Resister_label = tk.Label(Data, text="Resistor (Ohms)")
    Resister_label.grid(row=1, column=1, columnspan=2, padx=20, pady=10, sticky='n')

    R = tk.IntVar()

    Resister_value = ttk.Combobox(Data, text = R)
    Resister_value['values'] = (
        1,
        10,
        100,
        1000,
        10000,
        'Other'
        )

    if R == 100:
        donothing()
    
    print(R)

    Resister_value.current()
    Resister_value.grid(row=2, column=1, columnspan=1, padx=10, sticky='n')

    Sampling_label = tk.Label(Data, text="Sampling (Hz)")
    Sampling_label.grid(row=3, column=1, columnspan=2, padx=20, pady=3, sticky='n')
    Sampling_entry = tk.Entry(Data, bd=5)
    Sampling_entry.grid(row=4, column=1, columnspan=2, padx=20, pady=1, sticky='n')
   
    statusbar = ttk.Progressbar(Data, orient=HORIZONTAL, length= 100, mode='indeterminate')
    statusbar.grid(row=5, column=0, columnspan=1)

    Sampling_button = tk.Button(Data, text="Submit", command=statusbar.start(10))
    Sampling_button.grid(row=4, column=2, padx= 20)
    Sampling_rate = tk.Label(Data, text=f"Current Sample Rate: ")
    Sampling_rate.grid(row=4, column=1, columnspan=2, pady=25, sticky="s")

    menubar = tk.Menu(Data)
    filemenu = tk.Menu(Data, menubar, tearoff=0)
    filemenu.add_command(label="Open Main menu", command=core)
    menubar.add_cascade(label="File", menu=filemenu)

    Data.config(menu=menubar)


def new_project():
    nProject = tk.Toplevel(window)
    nProject.title("New Project")
    nProject.geometry('400x200')
    name = tk.Label()


def load_prject():
    lProject = tk.Toplevel(window)
    lProject.title("Load Project")
    lProject.geometry('400x200')
      


#update the data or Voltage and current
def update():
    Voltnum = randint(0,5)
    Currentnum = randint(0,5)
    Voltage.set(f"Voltage = 5 V\n \n dV/dt = {Voltnum} V")
    Current.set(f"Current = 5 A\n \n dI/dt = {Currentnum} A")
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