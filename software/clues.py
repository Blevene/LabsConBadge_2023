import time
import board
import busio
import pulseio
import digitalio
import displayio
import terminalio
import adafruit_imageload
import adafruit_displayio_sh1106
from fake_irda import FakeIRDA
from sh1106_ui import box
from five_way_pad import FiveWayPad
from adafruit_display_text import label
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

BLACK=0x000000
WHITE=0xFFFFFF

class clues:
    def __init__(self, group, dpad, game):
        self.group=group
        self.dpad=dpad
        self.game=game

        self.header=label.Label(terminalio.FONT,text="clues", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        clue_sheet, palette = adafruit_imageload.load("assets/clues.bmp",bitmap=displayio.Bitmap, palette=displayio.Palette)
        self.clue_grid = displayio.TileGrid(clue_sheet, pixel_shader=palette,
            width=11, height=3,
            tile_width=12, tile_height=16)
        self.clue_group=displayio.Group(y=15)
        self.clue_group.append(self.clue_grid)
        self.group.append(self.clue_group)

        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True
        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))
        self.detaillabel=label.Label(terminalio.FONT,text="About", color=WHITE, x=4, y=8)
        self.details.append(self.detaillabel)
        self.group.append(self.details)

        self.setcards()
        self.clue_grid[self.x,self.y]+=1


    def setcards(self):
        for j, cluetype in enumerate([self.game.threats,self.game.attacks,self.game.victims]):
            for i in range(self.game.cluecounts[j]):
                self.clue_grid[i,j]=7
                if cluetype[i][3] != "": self.clue_grid[i,j]=j*2+1
        self.x=0
        self.y=0


    def update(self):
        #show grid
        self.clue_group.hidden=False
        #un-highlight current clue
        self.clue_grid[self.x,self.y]-=1
        #if new clue, go to it
        if self.game.newclue != None:
            if self.game.newclue == -1:
               self.setcards()
               self.game.newclue=None
            else:
                self.x,self.y=self.game.newclue
                self.details.hidden=False
                self.game.newclue=None
        if self.dpad.u.fell:
            if self.y==0: 
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "trade"
            self.y -=1
            self.x=min(self.x,self.game.cluecounts[self.y]-1)
        if self.dpad.d.fell:
            if self.y==2: 
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "sleep"
            self.y +=1
            self.x=min(self.x,self.game.cluecounts[self.y]-1)
        if self.dpad.l.fell:
            if self.x==0:
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "home"
            self.x -=1
        if self.dpad.r.fell:
            if self.x==self.game.cluecounts[self.y]-1:
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "settings"
            self.x+=1
        if self.dpad.x.fell: self.details.hidden=not self.details.hidden
        self.clue_grid[self.x,self.y]+=1
        if self.y==0: clue=self.game.threats[self.x] 
        elif self.y==1: clue=self.game.attacks[self.x]
        else: clue=self.game.victims[self.x]
        #print(clue)
        if clue[3]=="":
            self.detaillabel.text="Could've been\n"+clue[1]
        elif clue[4]==self.game.myname:
            self.detaillabel.text="I know it wasn't\n"+clue[1]
        else:
            self.detaillabel.text=clue[4]+"\nknows it wasn't\n"+clue[1]
        return "clues"
