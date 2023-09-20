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

        #for i to len(t,a,v)= blank card
        self.cluecounts=[len(self.game.threats),len(self.game.attacks),len(self.game.victims)]
        for j, cluetype in enumerate([self.game.threats,self.game.attacks,self.game.victims]):
        #for j in range(len(self.cluecounts)):
            for i in range(self.cluecounts[j]):
                self.clue_grid[i,j]=7
                #print(cluetype[i][3])
                if cluetype[i][3] != "": self.clue_grid[i,j]=j*2+1
        self.x=0
        self.y=0
        self.clue_grid[self.x,self.y]+=1

    def update(self):
        self.clue_group.hidden=False
        self.clue_grid[self.x,self.y]-=1
        if self.dpad.u.fell:
            if self.y==0: 
                self.clue_group.hidden=True
                return "trade"
            self.y -=1
            self.x=min(self.x,self.cluecounts[self.y]-1)
        if self.dpad.d.fell:
            if self.y==2: 
                self.clue_group.hidden=True
                return "sleep"
            self.y +=1
            self.x=min(self.x,self.cluecounts[self.y]-1)
        if self.dpad.l.fell:
            if self.x==0:
                self.clue_group.hidden=True
                return "home"
            self.x -=1
        if self.dpad.r.fell:
            #todo change this to max # clues in the row
            if self.x==self.cluecounts[self.y]-1:
                self.clue_group.hidden=True
                return "settings"
            self.x+=1
        if self.dpad.x.fell: self.details.hidden=not self.details.hidden
        self.clue_grid[self.x,self.y]+=1
        if self.y==0:
            if self.game.threats[self.x][3] == "":
                self.detaillabel.text="Could've been\n"+self.game.threats[self.x][1]
            else:
                self.detaillabel.text=self.game.threats[self.x][4]+"\n  said it wasn't\n"+self.game.threats[self.x][1]
        elif self.y==1:
            if self.game.attacks[self.x][3] == "":
                self.detaillabel.text="Could've been\n"+self.game.attacks[self.x][1]
            else:
                self.detaillabel.text=self.game.attacks[self.x][4]+"\n  said it wasn't\n"+self.game.attacks[self.x][1]
        elif self.y==2:
            if self.game.victims[self.x][3] == "":
                self.detaillabel.text="Could've been\n"+self.game.victims[self.x][1]
            else:
                self.detaillabel.text=self.game.victims[self.x][4]+"\n  said it wasn't\n"+self.game.victims[self.x][1]
        return "clues"
