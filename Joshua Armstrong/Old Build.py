import tkinter as tk
from random import randint
from tkinter import messagebox

#RTSxx(year)-Jxxxx(job number)
#Example: RTS21-J0123
#Year 2021, Job 123


window = tk.Tk()

#Set the size of the window
#window.geometry('1280x720')

#set row and column. needs reworking
window.columnconfigure(3, weight= 1, minsize=250)
window.rowconfigure(3, weight= 1, minsize=50)

#master frame
frame = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
    )

#set inital Voltage and Current texts
Voltage = tk.StringVar()
Voltage.set(f"Voltage = 5 V\n \n dV/dt = {randint(0,1000)} V")

Current = tk.StringVar()
Current.set(f"Current = 5 A\n \n dC/dt = {randint(0,1000)} A")


def addList():
    i = 0
    i += 1

    frame = tk.Frame(
        master=window,
        relief=tk.RAISED,
        borderwidth=1
        )

    frame.grid(row=0, column=i, padx=10, pady=10, sticky="n")
    label1 = tk.Label(master=frame, textvariable=Voltage)
    label1.pack(padx=20, pady=20, side = tk.LEFT)

    frame.grid(row=1, column=i, padx=10, pady=10,)
    label2 = tk.Label(master=frame, textvariable=Current)
    label2.pack(padx=20, pady=20, side = tk.RIGHT)

    frame.grid(row=2, column=i,)
    label3 = tk.Label(master=frame, text="Flags")
    label3.pack(padx=20, pady=20, side = tk.BOTTOM)


addList()

#label/frame for Voltage
#frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
#label1 = tk.Label(master=frame, textvariable=Voltage)
#label1.pack(padx=20, pady=20)

#label/frame for Current
#frame.grid(row=1, column=0, padx=10, pady=10,)
#label2 = tk.Label(master=frame, textvariable=Current)
#label2.pack(padx=20, pady=20)

#Label/frame for flags
#frame.grid(row=2, column=0,)
#label3 = tk.Label(master=frame, text="Flags")
#label3.pack(padx=20, pady=20)

#label/frame for + button

frame2 = tk.Frame(
        master=window,
        relief=tk.RAISED,
        borderwidth=1
        )


#label/frame for - button
#frame.grid(row=3, column=3, padx=10, pady=10,)
#testbutton1 = tk.Button(master=frame, text= "-", width=2, height=1,)
#testbutton1.pack(padx=20, pady=20, side = tk.LEFT,)

#update the data or Voltage and current
def update():
    Voltage.set(f"Voltage = 5 V\n \n dV/dt = {randint(0,1000)} V")
    Current.set(f"Current = 5 A\n \n dC/dt = {randint(0,1000)} A")
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
samplingmenu = tk.Menu(menubar, tearoff=0)
samplingmenu.add_command(label="Sampling Rates", command=Sampling_Window)
menubar.add_cascade(label="Sampling", menu=samplingmenu)


#setting for flag menu
flagmenu = tk.Menu(menubar, tearoff=0)
flagmenu.add_command(label="Flags Settings", command=flag_Window)
menubar.add_cascade(label="Flags", menu=flagmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

frame2.grid(row=3, column=3, padx=10, pady=10,)
testbutton1 = tk.Button(master=frame2, text= "+", width=2, height=1, command= addList)
testbutton1.pack(padx=20, pady=20, side = tk.RIGHT)

#Pack the menu
window.config(menu=menubar)

#runs the update
update()

window.mainloop()