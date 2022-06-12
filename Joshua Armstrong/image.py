import tkinter as tk

# init tk
window = tk.Tk()

# create canvas
myCanvas = tk.Canvas(window, bg="white", height=300, width=300)

# draw arcs
coord = 10, 10, 300, 300
arc = myCanvas.create_arc(coord, start=0, extent=150, fill="red")
arv2 = myCanvas.create_arc(coord, start=150, extent=215, fill="green")

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

text1.pack()
text2.pack()
testbutton.pack()


# add to window and show
myCanvas.pack()
window.mainloop()