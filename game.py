from tkinter import *
#from tkinter import ttk
import keyboard
import datetime

from PIL import ImageTk, Image

# TODO remove all +10 and -10 attributes in the players collision system and make them dynamic

root = Tk()
root.geometry("1280x720")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.create_rectangle(10,10,40,40, fill="red", tags="wall")
canvas.create_rectangle(500,500,400,350, fill= "blue", tags="wall")
img = ImageTk.PhotoImage(Image.open("testbild.png"))
canvas.create_image(0, 600, image= img, tags="wall")


class Player():
    def __init__(self,x,y):
        self.xPos = x
        self.yPos = y
        self.xSpeed = 0
        self.ySpeed = 0
    def move(self, xAcceleration, yAcceleration):

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

    def collisiondetection(self):
        collision_objects = canvas.find_overlapping(self.xPos+10, self.yPos+10, self.xPos-10,self.yPos-10)
        for x in collision_objects:
            tag = canvas.gettags(x)

            if tag[0] == "wall":
                bounding_box = canvas.bbox(x)
                wallx1, wally1, wallx2, wally2 = bounding_box
                print(wallx1,wally1,wallx2,wally2)
                print(self.xPos,self.yPos)


                self.xPos -= self.xSpeed
                self.xSpeed = 0
                self.yPos -= self.ySpeed
                self.ySpeed = 0

    
class Camera():
    def __init__(self, x, y):
        self.xPos = x
        self.yPos = y

    def move(self, xPlayer, yPlayer):
        scalar = 0.3 # wert zwischen 0-1, der bestimmt, wie sehr die Kamera hinterherhinkt (0 sehr viel, 1 gar nicht)
        
        xDistance = (xPlayer - self.xPos) *scalar
        yDistance = (yPlayer - self.yPos) *scalar

        for x in canvas.find_all():
            canvas.move(x,-xDistance,-yDistance)

        spieler.xPos -= xDistance
        spieler.yPos -= yDistance


xcenter = 640
ycenter = 360
print (xcenter,ycenter)

spieler = Player(xcenter,ycenter)
kamera = Camera(xcenter,ycenter)

def gameloop():
    #delete everything
    #check input
    #move/re-place player
    #move camera
    #wait for 16-rendertime ms

    start_time = datetime.datetime.now() 

    canvas.delete("player")
    keyboard_input()
    canvas.create_rectangle(spieler.xPos-10,spieler.yPos-10,spieler.xPos+10,spieler.yPos+10,tags="player")
    
    spieler.collisiondetection()


    kamera.move(spieler.xPos, spieler.yPos)

    mouse = mouse_input()


    global debugtext
    canvas.delete("debug")
    debugtext = canvas.create_text(1,1, text= "s",tags="debug", anchor= "nw")
    debugstuff()


    end_time = datetime.datetime.now() #NO CODE BEYOND THIS CODE
    difference_time = (end_time - start_time)
    execution_time = difference_time.total_seconds() * 1000
    wait_time = 16 - round(execution_time)
    #print(wait_time)
    canvas.after(wait_time, gameloop)

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

def debugstuff():
    info = f"Spieler: x: {round(spieler.xPos)} y: {round(spieler.yPos)}"
    canvas.itemconfigure(debugtext, text= info)

gameloop()
root.mainloop()

