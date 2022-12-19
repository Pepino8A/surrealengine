from tkinter import *
#from tkinter import ttk
import keyboard
import datetime
from copy import deepcopy
from math import atan2, degrees, sin, cos, sqrt, pow
from PIL import ImageTk, Image
import simpleaudio as sa 
import json

Image.MAX_IMAGE_PIXELS = 300000001

# TODO remove all +10 and -10 attributes in the players collision system and make them dynamically sized

root = Tk()
root.geometry("1280x720")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title("Chainsaw Bazooka")



canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))

mapimg = ImageTk.PhotoImage(Image.open("img/Real-Mapv2.png"))
canvas.create_image(0,0, image= mapimg, tags= "other", anchor="nw")

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
        self.shoot_cooldown = 100
        self.hp = 5
        self.iframes = 30
        self.heart = ImageTk.PhotoImage(Image.open("img/herz.png"))
        self.blackheart = ImageTk.PhotoImage(Image.open("img/herzschwarz.png"))

    def move(self, xMovement, yMovement, acceleration = 1.5):
        
        if self.shoot_cooldown != 0:
            self.shoot_cooldown -= 1
        if self.iframes != 0:
            self.iframes -= 1
        
        if self.hp <= 0:
            return
        #acceleration = 1.5
        maxspeed = 15
        fadeout = 0.8
        
        match xMovement:
            case -1:
                if -maxspeed < self.xSpeed:
                    self.xSpeed -= acceleration
            case 1:
                if maxspeed > self.xSpeed:
                    self.xSpeed += acceleration
            case 0:
                self.xSpeed *= fadeout
        self.xPos += self.xSpeed

        match yMovement:
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

            if tag[0] == "zombie" and self.iframes == 0:
                self.hp -= 1
                self.iframes = 30
                hurtsound = sa.WaveObject.from_wave_file("sounds/Protagonistdamagesound.wav")
                hurtsound.play()

        
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

        yoffset = 950
        
        match self.hp:
            case 1:
                canvas.create_image(xcenter-100,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter-50,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter+50,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter+100,yoffset, image= self.blackheart, tags="player")
            case 2:
                canvas.create_image(xcenter-100,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter-50,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter+50,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter+100,yoffset, image= self.blackheart, tags="player")
            case 3:
                canvas.create_image(xcenter-100,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter-50,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter+50,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter+100,yoffset, image= self.blackheart, tags="player")
            case 4:
                canvas.create_image(xcenter-100,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter-50,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter+50,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter+100,yoffset, image= self.blackheart, tags="player")
            case 5:
                canvas.create_image(xcenter-100,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter-50,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter+50,yoffset, image= self.heart, tags="player")
                canvas.create_image(xcenter+100,yoffset, image= self.heart, tags="player")
            case _ :
                canvas.create_image(xcenter-100,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter-50,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter+50,yoffset, image= self.blackheart, tags="player")
                canvas.create_image(xcenter+100,yoffset, image= self.blackheart, tags="player")
                self.raw_image = Image.open("img/Player_Tod.png")
                canvas.create_text(xcenter, 350, text="You Loose!", fill = "red", tags="player")

    def shoot(self):
        if self.shoot_cooldown == 0:
            bullets.append(Bullet("img/Blade.png",25))
            self.shoot_cooldown = 100
            shotsound = sa.WaveObject.from_wave_file("sounds/Shotsound.wav")
            shotsound.play()

class Camera():
    def __init__(self, x, y):
        self.xPos = x
        self.yPos = y

    def move(self, xPlayer, yPlayer):
        scalar = 0.2 # wert zwischen 0-1, der bestimmt, wie sehr die Kamera hinterherhinkt (0 sehr viel, 1 gar nicht)
        
        xDistance = (xPlayer - self.xPos) *scalar
        yDistance = (yPlayer - self.yPos) *scalar

        for x in canvas.find_all():
            canvas.move(x,-xDistance,-yDistance)

        spieler.xPos -= xDistance
        spieler.yPos -= yDistance

        for obj in zombies:
            obj.xPos -= xDistance
            obj.yPos -= yDistance
        for obj in bullets:
            obj.xPos -= xDistance
            obj.yPos -= yDistance

class Zombie():
    def __init__(self, x, y, imagepath,deadimagepath):
        self.xPos = x
        self.yPos = y
        self.width = 100
        self.height = 100
        self.raw_image = Image.open(imagepath)
        self.deadtimage = Image.open(deadimagepath)
        self.xMovement = 0
        self.yMovement = 0
        self.decay = 0
        self.direction = 0

    def move(self):
        scalar = 6
        try:
            self.direction = atan2(self.yPos - spieler.yPos, self.xPos - spieler.xPos)
        except:
            print("divison by 0")
            return
        self.xMovement = cos(self.direction) * -scalar
        self.yMovement = sin(self.direction) * -scalar

        self.xPos += self.xMovement
        self.yPos += self.yMovement

    def drawimage(self):
        img_direction = degrees(self.direction) - 180
        rotated_image = self.raw_image.rotate(-img_direction)
        rendered_rotated_image = ImageTk.PhotoImage(rotated_image)
        canvas.create_image(self.xPos,self.yPos, image=rendered_rotated_image,tags="zombie")
        imagebuffer.append(rendered_rotated_image)

    def collisionchecker(self):
        collision_objects = canvas.find_overlapping(self.xPos+self.width/2, self.yPos+self.height/2, self.xPos-self.width/2,self.yPos-self.height/2)
        for x in collision_objects:
            tag = canvas.gettags(x)

            match tag[0]:
                case "wall":
                    bounding_box = canvas.bbox(x)
                    wallx1, wally1, wallx2, wally2 = bounding_box

                    self.xPos -= (self.xMovement * 1.01)
                    self.yPos -= (self.yMovement * 1.01)

                case "zombie":
                    bounding_box = canvas.bbox(x)
                    wallx1, wally1, wallx2, wally2 = bounding_box

                    xCenter = ((wallx2 - wallx1) / 2) + wallx1
                    yCenter = ((wally2 - wally1) / 2) + wally1

                    if abs(xCenter - self.xPos) <= 1: #sich selbst nicht auswählen
                        return
                    
                    xDistance = self.xPos - xCenter
                    yDistance = self.yPos - yCenter
                    self.xPos += (xDistance * 0.05)
                    self.yPos += (yDistance * 0.05)

                case "bullet":
                    self.raw_image = self.deadtimage
                    self.decay = 1
                    zombietod = sa.WaveObject.from_wave_file("sounds/Zombietodsound.wav")
                    zombietod.play()
                    


    def tick(self):
        if sqrt(pow((self.xPos - spieler.yPos),2) + pow((self.yPos-spieler.yPos),2)) > 1500:
            return
        if self.decay == 0:
            self.move()
            self.collisionchecker()
            self.drawimage()
        else:
            self.decay += 1
            self.drawimage()

class Bullet():
    def __init__(self, imagepath, s):
        self.xPos = deepcopy(spieler.xPos)
        self.yPos = deepcopy(spieler.yPos)
        self.raw_image = Image.open(imagepath)
        self.mousecoords = deepcopy(mouse_input())
        self.direction = atan2(self.mousecoords[1] - self.yPos, self.mousecoords[0] - self.xPos)
        self.deg_steigung = degrees(atan2(self.mousecoords[1] - self.yPos, self.mousecoords[0] - self.xPos))
        self.scalar = s
        self.stuck = 0
        try:
            self.width = cos(atan2(self.mousecoords[1] - self.yPos, self.mousecoords[0] - self.xPos)) * 100
            self.height = sin(atan2(self.mousecoords[1] - self.yPos, self.mousecoords[0] - self.xPos)) * 100
        except:
            self.width = 100
            self.height = 100

    def imagerender(self):
            
        rotated_image = self.raw_image.rotate(-self.deg_steigung)
        rendered_rotated_image = ImageTk.PhotoImage(rotated_image)
        canvas.create_image(self.xPos,self.yPos, image=rendered_rotated_image,tags="bullet")
        imagebuffer.append(rendered_rotated_image)

    def move(self):

        collision_objects = canvas.find_overlapping(self.xPos+self.width/2, self.yPos+self.height/2, self.xPos-self.width/2,self.yPos-self.height/2)
        for x in collision_objects:
            tag = canvas.gettags(x)

            match tag[0]:
                case "wall":
                    self.stuck += 1
                    print(self.stuck)
                    return

        xMovement = cos(self.direction) * self.scalar
        yMovement = sin(self.direction) * self.scalar

        self.xPos += xMovement
        self.yPos += yMovement

    def tick(self):
        if sqrt(pow((self.xPos - spieler.yPos),2) + pow((self.yPos-spieler.yPos),2)) > 1500:
            self.stuck += 1
            pass
        else:
            self.move()
            self.imagerender()



screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
xcenter = screenwidth/2
ycenter = screenheight/2
print(xcenter,ycenter)

spieler = Player(14500,10100,"img/player-2.png")
kamera = Camera(xcenter,ycenter)



def gameloop():
    #delete everything
    #check input
    #move/re-place player
    #move camera
    #wait for 16-rendertime ms
    start_time = datetime.datetime.now() 
    global zombies
    global imagebuffer

    imagebuffer.clear()

    canvas.delete("zombie")
    for obj in zombies:
        if obj.decay > 120: #how long should the deathmodel stay in frames
            del obj
        else:
            obj.tick()

    canvas.delete("bullet")
    for obj in bullets:
        if obj.stuck > 120: #how long should the blade be stuck in frames
            del obj
        else:
            obj.tick()

    canvas.delete("player")
    keyboard_input()

    spieler.collsionchecker()
    spieler.imagerenderer()

    kamera.move(spieler.xPos, spieler.yPos)

    global mainthemeplayer
    if mainthemeplayer.is_playing():
        pass
    else:
        maintheme = sa.WaveObject.from_wave_file("sounds/Chainsaw-BazookaOSTv1.wav")
        mainthemeplayer = maintheme.play()

        

    end_time = datetime.datetime.now() #NO CODE BEYOND THIS CODE
    execution_time = (end_time - start_time).total_seconds() * 1000
    wait_time = 16 - round(execution_time)
    if wait_time <= 0:
        wait_time = 0
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
        spieler.shoot()
    
    spieler.move(x,y)

def mouse_input():
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    return x,y

#imported_objects = [{"type" : "zombie", "x": 500, "y" : 300, "image": "img/Standardzombie2.png", "deadimage": "img/Standardzombie2-Tod.png"},{"type" : "zombie", "x": 900, "y" : 400, "image": "img/testarrow.png", "deadimage": "img/Standardzombie2-Tod.png"},{"type" : "zombie", "x": 550, "y" : 200, "image": "img/Standardzombie2.png", "deadimage": "img/Standardzombie2-Tod.png"}]

f = open("data.json")
imported_objects = json.load(f)
zombies = list()
bullets = list()
walls = list()


def initialize():
    global maintheme
    global mainthemeplayer
    for obj in imported_objects:
        if obj["type"] == "zombie":
            zombies.append(Zombie(obj["x"],obj["y"],obj["image"],obj["deadimage"]))
        if obj["type"] == "wall":
            canvas.create_rectangle(obj["x1"],obj["y1"],obj["x2"],obj["y2"],fill="",outline= "",tags= "wall")
    kamera.move(14500,10100)
    maintheme = sa.WaveObject.from_wave_file("sounds/Chainsaw-BazookaOSTv1.wav")
    mainthemeplayer = maintheme.play()

initialize()
gameloop()
root.mainloop()

