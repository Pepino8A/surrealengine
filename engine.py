from tkinter import *
from tkinter import ttk
from math import sqrt

def savePosn(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

def move(event):
    global lastx, lasty
    movex = event.x - lastx #movex 
    movey = event.y - lasty

    for x in canvas.find_all(): #selects all canvas items
        canvas.move(x, movex, movey)
    #canvas.move(poly, dx, dy)
    savePosn(event)



root = Tk()
root.geometry("1000x600")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.bind("<Button-1>", savePosn)
canvas.bind("<B1-Motion>", move)
canvas.create_polygon(10, 10, 200, 50, 90, 150, 50, 80, 120, 55, fill='red', outline='blue')
canvas.create_rectangle(40,30,110,50)

 
root.mainloop()