from tkinter import *
#from tkinter import ttk
from PIL import ImageTk, Image
from math import sqrt,pow

class TestImage:

    def __init__(self, xPos, yPos, rawImagePath): #konstruktor
        self.xPos = xPos
        self.yPos = yPos
        try:
            #self.rawImage = Image.open(rawImagePath)
            self.processedImage = ImageTk.PhotoImage(Image.open(rawImagePath))
        except:
            print("~~~~Bild konnten nicht geladen werden. Prüfe den Pfad und stelle sicher, das PIL installiert ist~~~~")
        canvas.create_image(self.xPos,self.yPos, image = self.processedImage)

    


def savePosn(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

def move(event):
    global lastx, lasty
    movex = event.x - lastx #movex 
    movey = event.y - lasty

    for x in canvas.find_all(): #selects all canvas items
        canvas.move(x, movex, movey)

    savePosn(event)


""" zoomlevel = 0 //scrapped zoom
def zoom(event):
    # event.delta ist +-120

    global zoomlevel
    minzoom = 25
    maxzoom = -15

    zoomin_multiplier = 10/9
    zoomout_mulitplier = 1/(10/9)

    if maxzoom < zoomlevel < minzoom: #normaler zoom
        match event.delta:
            case 120: #reinzoomen
                zoomer(zoomin_multiplier,event.x,event.y)
                zoomlevel += 1
            case -120: #rauszoomen
                zoomer(zoomout_mulitplier,event.x,event.y)
                zoomlevel -= 1
            case _:
                raise ValueError("Mausinput macht komische dinge")

    if zoomlevel == maxzoom and event.delta == 120: #limit beim kompletten reinzoomen
        zoomer(zoomin_multiplier,event.x,event.y)
        zoomlevel += 1
    if zoomlevel == minzoom and event.delta == -120: #anderes limit
        zoomer(zoomout_mulitplier,event.x,event.y)
        zoomlevel -= 1
    print(zoomlevel)

def zoomer(zoomamount,eventx,eventy):
    for x in canvas.find_all(): # selects all canvas items
        #print(f"{x} canvas coords", canvas.coords(x)) # gibt einen dict zurück
        newcoords = []
        for y in range(len(canvas.coords(x))): #geht durch die *länge* der liste an koordinaten, die eine Figur ausmacht

            if y % 2 == 0: # alle koordinatenpaare | canvas.coords(x)[y] (x koord) und canvas.coords(x)[y+1] (y koord) um auf das aktuelle Koordinatenpaar zuzugreifen
                dx = canvas.coords(x)[y] - eventx #Kathethen des Dreiecks zwischen der Maus und einem Punkt
                dy = canvas.coords(x)[y+1] - eventy

                u = sqrt((dx**2) + (dy**2)) #satz des pythagoras / Hypothenuse
                u2 = u * zoomamount # neue länge der hypothenuse
                y2 = (u2/u) * dy  #strahlensätze
                x2 = (y2/dy) * dx  #x2 ist die neue länge

                realx = eventx + x2 #x2 und y2 sind offsets vom mauspunkt
                realy= eventy +y2

                newcoords.append(realx)
                newcoords.append(realy)

        s = f"canvas.coords({x}"
        for z in newcoords:
            s += f",{z}"
        s += ")"
        exec(s)
        #canvas.coords(x,x0,y0,x1,y1) mit einer unbekannten Menge an Punkten """

def placeImage(event):
    print("yay")
    # global photobuffer
    global classes
    global testbuffer
    # img = photobuffer["testbild"]
    # canvas.create_image(event.x, event.y, image = img)
    classes.append(TestImage(event.x,event.y, "testbild.png"))


photobuffer_raw = {}
photobuffer = {}
testbuffer = []


root = Tk()
root.geometry("1280x720")
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root, bg="white")
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.bind("<Button-1>", savePosn)
canvas.bind("<Button-3>", placeImage) #Btn1 = links, btn2 = mitte, btn3 = rechts
canvas.bind("<B1-Motion>", move)
#canvas.bind("<MouseWheel>", zoom)
canvas.create_polygon(10, 10, 200, 50, 90, 150, 50, 80, 120, 55, fill='red', outline='blue')
canvas.create_rectangle(40,30,110,50)

photobuffer_raw["testbild"] = Image.open("testbild.png")
photobuffer["testbild"] = ImageTk.PhotoImage(photobuffer_raw["testbild"])

classes = []
classes.append(TestImage(0,0,"testbild.png"))
classes.append(TestImage(300,300,"testbild.png"))

#canvas.create_image(classes[1].xPos,classes[1].yPos,image = classes[1].processedImage)

print(classes)

sidebar = Frame(root, bg="RED")
sidebar.grid(column=1, row=0)


testlabel = Label(sidebar, text = "test", bg="Red")
testlabel.grid(column=0 , row=1)

undobutton = Button(sidebar,text= "undo", command = lambda: classes.pop())
undobutton.grid(column = 0, row = 0)


root.mainloop()



