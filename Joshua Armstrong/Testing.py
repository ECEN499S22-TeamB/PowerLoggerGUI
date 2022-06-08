import tkinter
import tkinter as tk

window = tkinter.Tk()
text1 = tk.Label(text="Hello World")
text2 = tk.Label(
    text="next line",
    foreground="white",
    background="blue",
    height= 10,
    width= 20)

testbutton = tk.Button(
    text= "Don't touch",
    width=10,
    height=5,
    fg="black",
    bg="red",
    )

frame = tk.Frame()
frame_label=tk.Label(
    master=frame,
    text="frame 1",
    relief=tk.RAISED)
frame_label.pack()
#frame.pack() order of pack for a frame matter.


text1.pack()
text2.pack()
frame.pack()
testbutton.pack()

window.mainloop()