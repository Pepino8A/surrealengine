from tkinter import *
from tkinter import ttk
import keyboard

#TODO fix camera

root = Tk()
root.geometry("1280x720")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.create_rectangle(10,10,40,40, fill="red")

class Player():
    def __init__(self,x,y):
        self.xPos = x
        self.yPos = y
        self.xSpeed = 0
        self.ySpeed = 0
    def move(self, xAcceleration,yAcceleration):

        acceleration = 3
        maxspeed = 40
        fadeout = 0.8

        match xAcceleration:
            case -1:
                if -maxspeed < self.xSpeed:
                    self.xSpeed -= acceleration
            case 1:
                if maxspeed > self.xSpeed:
                    self.xSpeed += acceleration
            case 0:
                self.xSpeed *= fadeout
        self.xPos += self.xSpeed

        match yAcceleration:
            case -1:
                if -maxspeed < self.ySpeed:
                    self.ySpeed -= acceleration
            case 1:
                if maxspeed > self.ySpeed:
                    self.ySpeed += acceleration
            case 0:
                self.ySpeed *= fadeout
        self.yPos += self.ySpeed
    
class Camera():
    def __init__(self, x, y):
        self.xPos = x
        self.yPos = y

    def move(self, xPlayer, yPlayer):
        scalar = 0.1
        
        xDistance = (xPlayer - self.xPos) * scalar
        yDistance = (yPlayer - self.yPos) * scalar

        print(xDistance, yDistance)
        for x in canvas.find_all():
            canvas.move(x,xDistance,yDistance)
        self.xPos += xDistance
        self.yPos += yDistance
        spieler.xPos += xDistance
        spieler.yPos += yDistance

spieler = Player(500,500)
kamera = Camera(500,500)

def gameloop():
    #delete everything
    #check input
    #move/re-place player
    #move camera
    #wait


    canvas.delete("player")
    keyboard_input()
    canvas.create_rectangle(spieler.xPos-10,spieler.yPos-10,spieler.xPos+10,spieler.yPos+10,tags="player")
    


    mouse = mouse_input()
    canvas.create_line(spieler.xPos,spieler.yPos,mouse[0],mouse[1],tags="player")

    kamera.move(spieler.xPos, spieler.yPos)
    canvas.after(16, gameloop)

def keyboard_input():
    x = 0
    y = 0
    if keyboard.is_pressed("w"):
        y -= 1
    if keyboard.is_pressed("a"):
        x -= 1
    if keyboard.is_pressed("s"):
        y += 1
    if keyboard.is_pressed("d"):
        x += 1
    if keyboard.is_pressed("space"):
        print("space")
    
    spieler.move(x,y)

def mouse_input():

    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    return x,y
    

gameloop()
root.mainloop()

