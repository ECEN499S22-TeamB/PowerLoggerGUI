import tkinter as tk

window = tk.Tk()
#Set the size of the window
window.geometry('1280x720')

for i in range(3):
    window.columnconfigure(1, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)

    for j in range(0, 3):
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=i, column=j, padx=5, pady=5)
            label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
            label.pack(padx=10, pady=10)
            

window.mainloop()