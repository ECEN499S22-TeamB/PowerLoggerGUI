from cgi import test
import tkinter as tk

window = tk.Tk()

def new():
    new = tk.Tk()


testbutton = tk.Button(
    text= "Button",
    width=10,
    height=5,
    command=new()
    )

testbutton.pack()

window.mainloop()