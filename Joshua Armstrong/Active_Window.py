import tkinter as tk

window = tk.Tk()
test_window = tk.Tk()

test_window.title("Testing")

lbl_flags_beacon = None # Make this widget global
flag = False

DUT = []

def toggle_flag():
    """Toggles the flag for testing purposes."""
    global flag # Connect with the global variable
    flag = not flag

#
# change_color
#
#def flash_beacon():
    """Enable or disable the flashing beacon."""
#    if flag:
#       change_color()
#    else:
#        lbl_flags_beacon.config(bg="white") # If no flag, make bg white
#    window.after(200, flash_beacon)         # Run every 200 ms

#
# change_color
#
#def change_color():
    """Change the color of the flags beacon box."""
    #current_color = lbl_flags_beacon.cget("background")
    #if current_color == "red":
    #    next_color = "white"  
    #else:
    #    next_color = "red"
    #lbl_flags_beacon.config(background=next_color)



def active_DUT():
    global lbl_flags_beacon 

    frm_row_settings = tk.Frame(
        window,
        relief= tk.SUNKEN,
        borderwidth=2
        )    

    #for i in DUT:
     
    btn_DUT = tk.Button(
        frm_row_settings,
        text=f"Job #",
        command=donothing,
        width=20,
        height=2,
        relief= tk.SOLID,
        borderwidth=1,
        )

    lbl_voltage = tk.Label(
        frm_row_settings,
        text="Voltage = #",
        width=20,
        height=2,
        relief= tk.SOLID,
        borderwidth=1,
        )

    lbl_current = tk.Label(
        frm_row_settings,
        text="current = #",
        relief= tk.SOLID,
        width=20,
        height=2,
        borderwidth=1
        )

    lbl_flag = tk.Label(
        frm_row_settings,
        text="Flag",
        width=20,
        height=2,
        relief= tk.SOLID,
        borderwidth=1
        )

    global lbl_flags_beacon # Connect with the global variable
    lbl_flags_beacon = tk.Label(
        frm_row_settings,  
        width=10, 
        height=2,
        relief=tk.SUNKEN,
        borderwidth=2,
        bg="white")
 
    frm_row_settings.pack(side=tk.TOP)

    btn_DUT.pack(padx=0, side=tk.LEFT)
    lbl_voltage.pack(padx=0, side=tk.LEFT)
    lbl_current.pack(padx=0, side=tk.LEFT)
    lbl_flag.pack(padx=0, side=tk.LEFT)
    lbl_flags_beacon.pack(side=tk.LEFT)


def add_DUT():
    add_button = tk.Button(
        test_window,
        text="Testing Button",
        height=5,
        width=12,
        command=active_DUT
        )

    add_button.pack()


def donothing():
    x = 0

def add_to_DUT():
    y = 0
    DUT.append(y)
    y += 1

add_DUT()
#active_DUT()
toggle_flag()
#flash_beacon()
#change_color()


window.mainloop()