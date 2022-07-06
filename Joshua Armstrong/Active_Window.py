import csv
import tkinter as tk

test_window = tk.Tk()

test_window.title("Testing")

lbl_flags_beacon = None # Make this widget global
flags = False

DUT = []

#def toggle_flag():
#    """Toggles the flag for testing purposes."""
#    global flag # Connect with the global variable
#    flag = not flag

job_num_list = []
volt_list = []
current_list = []
flags_list = []

with open(r"C:\Users\aqua_\Documents\Codeing Project\CVS testing.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} - {row[1]} - {row[2]} - {row[3]}.')
            job_num_list.append(row[0])
            volt_list.append(row[1])
            current_list.append(row[2])
            flags_list.append(row[3]) 
            line_count += 1

print(job_num_list)
print(volt_list)
print(current_list)
print(flags_list)

def active_DUT(job_num, voltage, current, flags):
    global lbl_flags_beacon 

    #Funtion to remove job listing
    def destroy_job():
        #goes through all the widget in a frame and destroy them
        for widget in frm_row_settings.winfo_children():
            widget.destroy()
        frm_row_settings.destroy()

    frm_row_settings = tk.Frame(
        active_window,
        relief=tk.SUNKEN,
        borderwidth=2
        )
    
    frm_volt_and_current = tk.Frame(
        frm_row_settings,
        #relief=tk.SOLID,
        borderwidth=0
        )

    frm_flag = tk.Frame(
        frm_row_settings,
        relief=tk.SOLID,
        borderwidth=1 
        )

    #for i in DUT:
     
    btn_DUT = tk.Button(
        frm_row_settings,
        text=f"Job {job_num}",
        command=destroy_job,
        width=20,
        height=2,
        relief= tk.SOLID,
        borderwidth=1,
        )

    lbl_voltage = tk.Label(
        frm_volt_and_current,
        text=f"Voltage = {voltage}",
        width=20,
        height=2,
        relief= tk.SOLID,
        borderwidth=1,
        )

    lbl_current = tk.Label(
        frm_volt_and_current,
        text=f"Current = {current}",
        relief= tk.SOLID,
        width=20,
        height=2,
        borderwidth=1
        )

    lbl_flag = tk.Label(
        frm_flag,
        text="Collecting",
        width=12,
        height=2,
        #relief= tk.SOLID,
        borderwidth=1
        )

    lbl_flags_beacon = tk.Label(
        frm_flag,  
        width=12, 
        height=2,
        relief=tk.SUNKEN,
        borderwidth=2,
        bg="white")
 
    frm_row_settings.pack(side=tk.TOP)

    btn_DUT.pack(padx=0, side=tk.LEFT)
    frm_volt_and_current.pack(side=tk.LEFT)
    lbl_voltage.pack(pady=0, side=tk.LEFT)
    lbl_current.pack(pady=0, side=tk.LEFT)
    frm_flag.pack(side=tk.LEFT)
    lbl_flag.pack(padx=0, side=tk.LEFT)
    lbl_flags_beacon.pack(side=tk.LEFT)

    #For Testing will move laater
    #-----------------------------------------------------
    def update_flag_beacon():
        """Change the color of the flags beacon box,
        depending of the top priority flag."""
        # Get the current beacon color
        current_color = lbl_flags_beacon.cget("background")
        next_color = "green"
        
        # Decide on the next color
        if current_color == "white":
            if flags == 0:
                next_color = "red"
            elif flags == 1:
                next_color = "orange"
            elif flags == 2:
                next_color = "yellow"
        elif any(flags):
            next_color = "white"
        else: 
            next_color = "green"

        # Change the beacon color
        lbl_flags_beacon.config(background=next_color)

        active_window.after(200, update_flag_beacon)
    #-----------------------------------------------------

    update_flag_beacon()

def testing_button():
    global job_num_list
    add_button = tk.Button(
        test_window,
        text="Testing Button",
        height=5,
        width=12,
        command=testing_add
        )

    add_button.pack()

def testing_add():
    global job_num_list
    job_num_list.append("Adding")
    print(job_num_list)


def donothing():
    x = 0

def active_list():
    global job_num_list
    global volt_list
    global current_list
    global flags_list

    number = len(job_num_list)
    print(number)

    for i in range(number):
        active_DUT(job_num_list[i], volt_list[i], current_list[i], flags_list[i])
        i += 1

   #active_window.after(5000, active_list)
        


if __name__ == '__main__':
    active_window = tk.Tk()
    testing_button()
    active_list()
    #active_DUT()
    active_window.after(1000)
    active_window.mainloop()


