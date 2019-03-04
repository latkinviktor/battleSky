import tkinter as T
import random
#GLOBALS
WIDTH = 30
HEIGHT = 18
CELL = 40
marker = None
activePlane = None

class Sprites:#collection of sprites
  __jetRight = [
    -CELL//4  , -CELL//20 ,
    -CELL//5  , -CELL//20 ,
    -CELL//3  , -CELL//20 ,
    -CELL//3  , -CELL//10 ,
    -CELL//5  , -CELL//10 ,
    -CELL//4  , -CELL//10 ,
    -CELL//4  , -CELL//4  ,
          0   , -CELL//10 ,
    CELL//4   , -CELL//20 ,
    CELL//2   ,        0  ,
    CELL//4   , CELL//20  ,
    0         , CELL//10  ,
    -CELL//4  ,  CELL//4  ,
    -CELL//4  , CELL//10  ,
    -CELL//5  , CELL//10  ,
    -CELL//3  , CELL//10  ,
    -CELL//3  , CELL//20  ,
    -CELL//5  , CELL//20  ,
    -CELL//4  , CELL//20  ,
    ]
  __jetLeft  = [-1*elem for elem in __jetRight]
  __jetDown = list()
  for i in range(0,len(__jetRight),2):
    __jetDown.append(__jetRight[i+1])
    __jetDown.append(__jetRight[i])

  __jetUp = [-1*elem for elem in __jetDown]

  __jets = {
    "right": __jetRight,
    "left" : __jetLeft,
    "up"   : __jetUp,
    "down" : __jetDown
    }
  def jet(self, direction):
    return self.__jets[direction]



  __markerRight = [
                  -CELL//3, -CELL//10,
                  -CELL//3, CELL//10,
                  -CELL//2, CELL//20,
                  -CELL//3,       0,
                  -CELL//2, -CELL//20,
                ]
  __markerLeft = [-elem for elem in __markerRight]
  __markerDown = list()
  for i in range(0, len(__markerRight), 2):
    __markerDown.append(__markerRight[i+1])
    __markerDown.append(__markerRight[i])
  __markerUp = [-elem for elem in __markerDown]
  __markers = {
          "right" : __markerRight,
          "left"  : __markerLeft,
          "up"    : __markerUp,
          "down"  : __markerDown
    }
  def marker(self, direction):
    return self.__markers[direction]


def polygon(position,sprite):
  """function calculates polygon in Oxy coordinates system;
      func's name: 'polygon';
      func's arguments: [a,b] - coordinates in game field bitween (1,1) and (WIDTH-1, HEIGHT-1);
                        [dx0, dy0, dx1, dy1...] - list of vertex Oxy coordinate differences by anchor point
      func's returning: [x0, y0, x1, y1...] - list of vertex Oxy coordinates
                        bitween (CELL*1, CELL*1) and (CELL*(WIDTH-1), CELL*(HEIGHT-1)) 
  """
  x, y = position
  x *= CELL
  y *= CELL
  length = len(sprite)
  poly = [0]*length
  for i in range(0, length, 2):
    poly[i]   = x+sprite[i]
    poly[i+1] = y+sprite[i+1]
  return poly

def handleKeyPress(event):
  global activePlane, sky
  if activePlane == None: return
  btUp    = { "left"  : activePlane.turnUp,
              "right" : activePlane.turnUp,
              "down"  : activePlane.crash,
              "up"    : activePlane.moveUp}
  btRight = { "up"    : activePlane.turnRight,
              "down"  : activePlane.turnRight,
              "left"  : activePlane.crash,
              "right" : activePlane.moveRight}
  btDown  = { "left"  : activePlane.turnDown,
              "right" : activePlane.turnDown,
              "up"    : activePlane.crash,
              "down"  : activePlane.moveDown}
  btLeft  = { "up"    : activePlane.turnLeft,
              "down"  : activePlane.turnLeft,
              "right" : activePlane.crash,
              "left"  : activePlane.moveLeft}
  def setHandler():
    sky.canv.bind("<KeyPress>",handleKeyPress)
  sky.canv.bind("<KeyPress>",lambda arg: arg)
  sky.root.after(200, setHandler)
  code = event.keycode
  bts = [0]*88
  bts[38] = bts[87] = btUp
  bts[40] = bts[83] = btDown
  bts[37] = bts[65] = btLeft
  bts[39] = bts[68] = btRight
  try: bts[code][activePlane.direction]()
  except: print('error: wrong key has been pressed')



#sky
class Sky:
  def __init__(self):
    self.w = WIDTH
    self.h = HEIGHT
    self.cell = CELL
  def draw(self):
    root = T.Tk()
    root.title("BattleSky")
    w, h = WIDTH*CELL, HEIGHT*CELL
    root.minsize(w, h)
    root.maxsize(w, h)
    self.root = root
    canv = T.Canvas(root, width=w, height=h, bg="#50C0F0")
    self.canv = canv
    canv.pack()
  
    for x in range(CELL, w, CELL):
      canv.create_line(x,0, x, h, fill="#2080A0")
    for y in range(CELL, h, CELL):
      canv.create_line(0,y, w, y, fill="#2080A0")
    canv.focus_set()
    canv.bind("<KeyPress>",handleKeyPress)
    
#plane
class Plane:
  def __init__(self,canv, x0, y0, player, direction="random"):
    self.player = player
    self.color = {"red":"#FF5050", "blue":"#5050FF"}[player]
    self.coords = x0, y0
    self.direction = ["down","up", "left", "right"][random.randint(0,3)] if direction=="random" else direction
    self.canv = canv
    self.draw()
  def draw(self):
    canv = self.canv
    x,y = self.coords
    x *= CELL
    y *= CELL
    jSprite = sprites.jet(self.direction)
    length = len(jSprite)
    coords = [0]*length
    for i in range(0,length,2):
      coords[i]   = x + jSprite[i]
      coords[i+1] = y + jSprite[i+1]
    
    self.pointer = canv.create_polygon(
      *coords,
      fill=self.color,
      #fill = "grey80",
      outline="black",
      tag='plane',
      )
    canv.tag_bind(self.pointer, "<Button-1>", self.select)

  def select(self, event):
    global activePlane, marker
    activePlane = self
    if marker == None:
      marker = Marker()
    marker.followPlane()

  def refreshSprite(self):  
    poly = polygon(self.coords, sprites.jet(self.direction))
    self.canv.coords(self.pointer,*poly)
    marker.followPlane()  
  def turnLeft(self):
    self.direction = "left"
    self.refreshSprite()
  def turnRight(self):
    self.direction = "right"
    self.refreshSprite()
  def turnDown(self):
    self.direction = "down"
    self.refreshSprite()
  def turnUp(self):
    self.direction = "up"
    self.refreshSprite()
  def crash(self):
    self.direction = None
    self.canv.delete(self.pointer)
    self.canv.delete("marker")
    global marker
    marker = None
  def moveUp(self):
    x,y = self.coords
    if y==1: self.crash()
    else:
      self.coords = x, y-1
      self.canv.move(self.pointer,     0, -CELL  )
      marker.followPlane()
  def moveDown(self):
    x,y = self.coords
    if y == HEIGHT-1: self.crash()
    else:
      self.coords = x, y+1
      self.canv.move(self.pointer,     0, CELL  )
      marker.followPlane()
  def moveLeft(self):
    x,y = self.coords
    if x == 1: self.crash()
    else:
      self.coords = x-1, y
      self.canv.move(self.pointer, -CELL, 0      )
      marker.followPlane()
  def moveRight(self):
    x,y = self.coords
    if x == WIDTH-1: self.crash()
    else:
      self.coords = x+1, y
      sky.canv.move(self.pointer,  CELL, 0      )
      marker.followPlane()
  
#marker
class Marker:
  def __init__(self):
    poly = polygon(activePlane.coords, sprites.marker(activePlane.direction))
    self.pointer = sky.canv.create_polygon(*poly, fill="#F04040", outline="yellow", tag='marker')
    self.followPlane()
  def followPlane(self):
    poly = polygon(activePlane.coords, sprites.marker(activePlane.direction))
    sky.canv.coords(self.pointer,*poly)
    
class Base:
  def __init__(self, x1, y1, x2, y2, player, plane, direction="random"):
##    sprite = [x1, y1, x2, y1, x2, y2, x1, y2]#local
##    poly =
    for x in range(x1, x2+1):
      for y in range(y1, y2+1):
        poly = polygon([x, y], [-CELL//2, -CELL//2, CELL//2, -CELL//2, CELL//2, CELL//2, -CELL//2, CELL//2])
        sky.canv.create_polygon(*poly, fill="#505050", outline="black", width=2)
    self.planes=[]
    for x in range(x1, x2+1):
      for y in range(y1, y2+1):
        self.planes.append(Plane(sky.canv,x,y, player, direction))
    

sky = Sky()
sky.draw()
sprites = Sprites()
baseOne = Base(x1=4,y1=5, x2=6, y2=8,
               direction="right", player="red", plane="bomb")
baseTwo = Base(x1=24,y1=10,x2=26,y2=13,
               direction="left", player="blue", plane="jet")
baseThree = Base(x1=15, x2=18, y1=1, y2=3,
                 direction = "down", player="red", plane="bomb")
baseFour = Base(x1=12, x2=15, y1=15, y2=17,
                direction = "up", player="blue", plane="jet")
##planes = list()
##for i in range(1,11):
##  planes.append(Plane(sky.canv,i,1))


sky.root.mainloop()
