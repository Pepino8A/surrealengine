from tkinter import *
#from tkinter import ttk
import keyboard
import datetime
from math import ceil, atan2, degrees
from PIL import ImageTk, Image

# TODO remove all +10 and -10 attributes in the players collision system and make them dynamically sized

root = Tk()
root.geometry("1280x720")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.create_rectangle(10,10,40,40, fill="red", tags="wall")
canvas.create_rectangle(500,500,400,-350, fill= "blue", tags="wall")
canvas.create_text(450,290, text = "100", tags= "other")
canvas.create_rectangle(410,500,300,350, fill="yellow", tags="wall")
img = ImageTk.PhotoImage(Image.open("testbild.png"))
canvas.create_image(0, 600, image= img, tags="wall")

imagebuffer = []

class Player():
    def __init__(self,x,y,imagepath):
        self.xPos = x
        self.yPos = y
        self.xSpeed = 0
        self.ySpeed = 0
        self.width = 100
        self.height = 100
        self.raw_image = Image.open(imagepath)

    def move(self, xAcceleration, yAcceleration):

        acceleration = 1.5
        maxspeed = 25
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

    def collsionchecker(self):
        collision_objects = canvas.find_overlapping(self.xPos+self.width/2, self.yPos+self.height/2, self.xPos-self.width/2,self.yPos-self.height/2)
        for x in collision_objects:
            tag = canvas.gettags(x)

            if tag[0] == "wall":
                bounding_box = canvas.bbox(x)
                wallx1, wally1, wallx2, wally2 = bounding_box

                xoverlap = max(0, min(wallx2, self.xPos+self.width/2) - max(wallx1, self.xPos-self.width/2)) # Checks the x-Axis -> y-Axis collision detection
                yoverlap = max(0, min(wally2, self.yPos+self.height/2) - max(wally1, self.yPos-self.height/2)) # Checks the y-Axis -> x-Axis collision detection


                """ if abs(xoverlap - yoverlap) <= 4:
                    print(abs(xoverlap - yoverlap))

                    if round(self.xSpeed) > 0:
                        self.xPos -= (xoverlap + 1)
                    if round(self.xSpeed) < 0:
                        self.xPos += (xoverlap + 1)
                    self.xSpeed = 0

                    if round(self.ySpeed) > 0:
                        self.yPos -= (yoverlap + 1)
                    if round(self.ySpeed) < 0:
                        self.yPos += (yoverlap + 1)
                    self.ySpeed = 0
                    self.xPos -= self.xSpeed
                    self.yPos -= self.ySpeed
                    self.xSpeed, self.ySpeed = 0,0 """

                    #return

                if xoverlap < yoverlap:
                    #print(xoverlap,yoverlap)
                    if self.xSpeed > 0:
                        self.xPos -= (xoverlap + 1)
                    else: 
                        self.xPos += (xoverlap + 1)
                    self.xSpeed = 0

                else:
                    #print(xoverlap, yoverlap)
                    if self.ySpeed > 0:
                        self.yPos -= (yoverlap + 1)
                    else: 
                        self.yPos += (yoverlap + 1)
                    self.ySpeed = 0
        
    def imagerenderer(self):
        mousecoords = mouse_input()
        try:
            deg_steigung = degrees(atan2(mousecoords[1] - self.yPos, mousecoords[0] - self.xPos)) # delta y / delta x
        except:
            print("division by 0")
            return
            
        rotated_image = self.raw_image.rotate(-deg_steigung)

        rendered_rotated_image = ImageTk.PhotoImage(rotated_image)

        canvas.create_image(self.xPos,self.yPos, image=rendered_rotated_image,tags="player")
        imagebuffer.append(rendered_rotated_image)

        

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

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
xcenter = screenwidth/2
ycenter = screenheight/2
print(xcenter,ycenter)

spieler = Player(xcenter,ycenter,"img/player-scheie100.png")
kamera = Camera(xcenter,ycenter)

def gameloop():
    #delete everything
    #check input
    #move/re-place player
    #move camera
    #wait for 16-rendertime ms
    start_time = datetime.datetime.now() 

    imagebuffer.clear

    canvas.delete("player")
    canvas.delete("other")
    keyboard_input()
    #canvas.create_rectangle(spieler.xPos-(spieler.width/2),spieler.yPos-(spieler.height/2),spieler.xPos+(spieler.width/2),spieler.yPos+(spieler.height/2),tags="player")
    
    spieler.collsionchecker()
    spieler.imagerenderer()
    kamera.move(spieler.xPos, spieler.yPos)

    
    debugstuff()


    end_time = datetime.datetime.now() #NO CODE BEYOND THIS CODE
    execution_time = (end_time - start_time).total_seconds() * 1000
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
    global debugtext
    debugtext = canvas.create_text(1,1, text= "s",tags="debug", anchor= "nw")
    info = f"Spieler: x: {round(spieler.xPos)} y: {round(spieler.yPos)}"
    canvas.itemconfigure(debugtext, text= info)
    canvas.delete("debug")

gameloop()
root.mainloop()

