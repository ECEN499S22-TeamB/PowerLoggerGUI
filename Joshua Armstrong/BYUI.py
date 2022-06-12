import tkinter as tk
from PIL import Image,ImageTk

#Create an instance of tkinter frame
window = tk.Tk()

#Set the geometry of tkinter frame
window.geometry("800x800")

#Create a canvas
canvas= tk.Canvas(window, width= 800, height= 800)
canvas.pack()

#Load an image in the script
img= ImageTk.PhotoImage(Image.open(r"C:\Users\aqua_\Pictures\BYUI.png"))

#Add image to the Canvas Items
canvas.create_image(10,10,anchor=tk.NW,image=img)

window.mainloop()