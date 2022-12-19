from tkinter import *
#from tkinter import ttk
from PIL import ImageTk, Image
import json

Image.MAX_IMAGE_PIXELS = 300000001


class CustomImage:
    def __init__(self, xPos, yPos, rawImagePath, deadimagepath): #konstruktor
        self.xPos = xPos
        self.yPos = yPos
        try:
            #self.rawImage = Image.open(rawImagePath)
            self.imagepath = rawImagePath
            self.deadpath = deadimagepath
            self.processedImage = ImageTk.PhotoImage(Image.open(rawImagePath))
            self.deadimage = ImageTk.PhotoImage(Image.open(deadimagepath))
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
    #print(canvas.bbox(origin))



setmode = 0
def placeObject(event):
    print("sucess")

    ogx1, ogy1, ogx2, ogy2 = canvas.bbox(origin)
    ogXoffset = (ogx1 + ogx2) / 2
    ogYoffset = (ogy1 + ogy2) / 2


    global classes
    global exportinfo
    global setmode
    match setmode:
        case 0:
            classes.append(("zombie",CustomImage(event.x,event.y, "img/Standardzombie1.png","img/Standardzombie1-Tod.png")))
            exportinfo.append({"type":"zombie","x": event.x - ogXoffset, "y": event.y - ogYoffset, "image": "img/Standardzombie1.png", "deadimage":"img/Standardzombie1-Tod.png"})
        case 1:
            classes.append(("zombie",CustomImage(event.x,event.y, "img/Standardzombie2.png","img/Standardzombie2-Tod.png")))
            exportinfo.append({"type":"zombie","x": event.x - ogXoffset, "y": event.y - ogYoffset, "image": "img/Standardzombie2.png", "deadimage":"img/Standardzombie2-Tod.png"})
        case 2:
            classes.append(("zombie",CustomImage(event.x,event.y, "img/Wurfzombie.png","img/Wurfzombie-Tod.png")))
            exportinfo.append({"type":"zombie","x": event.x - ogXoffset, "y": event.y - ogYoffset, "image": "img/Wurfzombie.png", "deadimage":"img/Wurfzombie-Tod.png"})
        case 3:
            classes.append(("zombie",CustomImage(event.x,event.y, "img/Schildzombie.png","img/Schildzombie-Tod.png")))
            exportinfo.append({"type":"zombie","x": event.x - ogXoffset, "y": event.y - ogYoffset, "image": "img/Schildzombie.png", "deadimage":"img/Schildzombie-Tod.png"})
        case 4: 
            applytorectangle(event.x,event.y)


def definerectange(x, y):
    applytorectangle()
    pass

exportinfo = []
classes = []

root = Tk()
root.geometry("1280x720")
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.title("Chainsaw Bazooka Editor")

canvas = Canvas(root, bg="white")
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.bind("<Button-1>", savePosn)
canvas.bind("<Button-3>", placeObject) #Btn1 = links, btn2 = mitte, btn3 = rechts
canvas.bind("<B1-Motion>", move)


mapimg = ImageTk.PhotoImage(Image.open("img/Real-Mapv2.png"))
canvas.create_image(0,0, image= mapimg, tags= "other", anchor="nw")


origin = canvas.create_rectangle(1,1,-1,-1)
print(canvas.bbox(origin))


sidebar = Frame(root, bg="white")
sidebar.grid(column=1, row=0)


def mode(event):
    global setmode
    setmode = modeselect.curselection()[0]
    print(setmode)

modeselect_var = StringVar(sidebar,"Zombie1 Zombie2 Wurfzombie Schildzombie Wand")
modeselect = Listbox(sidebar, listvariable=modeselect_var)
modeselect.grid(column=0 , row=1)
modeselect.bind("<<ListboxSelect>>",mode)

def undo():
    classes.pop()
    exportinfo.pop()

undobutton = Button(sidebar,text= "undo", command = undo)
undobutton.grid(column = 0, row = 0)

widthvar = StringVar(sidebar,"100")
widthentry = Entry(sidebar, textvariable= widthvar)
widthentry.grid(column=0, row=2)

heightvar = StringVar(sidebar,"100")
heightentry = Entry(sidebar, textvariable= heightvar)
heightentry.grid(column=1,row=2)

canvas.create_rectangle(10,10,-10,10, tags= "test")

def applytorectangle(x,y):
    canvas.delete("test")
    xPos = x
    yPos = y
    width = int(widthvar.get())
    height = int(heightvar.get())
    x1p = xPos + (width/2)
    y1p = yPos + (height/2)
    x2p = xPos - (width/2)
    y2p = yPos - (height/2)
    canvas.create_rectangle(x1p,y1p,x2p,y2p, tags= "test")


def rectanglesaver():
    global exporterinfo
    coords = canvas.bbox("test")

    classes.append(("wall",(coords[0],coords[1],coords[2],coords[3])))
    canvas.create_rectangle(coords[0],coords[1],coords[2],coords[3],fill = "gray", stipple="gray25")

    ogx1, ogy1, ogx2, ogy2 = canvas.bbox(origin)
    ogXoffset = (ogx1 + ogx2) / 2
    ogYoffset = (ogy1 + ogy2) / 2

    exportinfo.append({"type":"wall","x1":coords[0] - ogXoffset,"y1":coords[1] - ogYoffset,"x2":coords[2]- ogXoffset,"y2":coords[3]-ogYoffset})

saverectange = Button(sidebar,text="save rectangle",command=rectanglesaver)
saverectange.grid(column=0,row=3)

def exporter():
    print(exportinfo)
    print(canvas.bbox(origin))

    #writable_exportinfo = str(exportinfo)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(exportinfo, f, ensure_ascii=False, indent=4)

export_all = Button(sidebar,text="export everything",command=exporter)
export_all.grid(column=1, row=5)


root.mainloop()



