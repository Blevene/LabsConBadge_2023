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

class cards:
    def __init__(self, group, dpad):
        self.group=group
        self.dpad=dpad

        self.header=label.Label(terminalio.FONT,text="cards", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        card_sheet, palette = adafruit_imageload.load("assets/cards.bmp",bitmap=displayio.Bitmap, palette=displayio.Palette)
        self.card_grid = displayio.TileGrid(card_sheet, pixel_shader=palette,
            width=11, height=3,
            tile_width=12, tile_height=16)
        card_group=displayio.Group(y=15)
        card_group.append(self.card_grid)
        self.group.append(card_group)

        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True
        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))
        self.detaillabel=label.Label(terminalio.FONT,text="About", color=WHITE, x=4, y=8)
        self.details.append(self.detaillabel)
        self.group.append(self.details)

        for i in range(3): self.card_grid[i,0]=1
        for i in range(5): self.card_grid[i,1]=3
        for i in range(4): self.card_grid[i,2]=5
        self.x=2
        self.y=2

    def update(self):
        self.card_grid[self.x,self.y]=self.y*2+1
        if self.dpad.u.fell:
            if self.y==0: return "trade"
            self.y -=1
        if self.dpad.d.fell:
            if self.y==2: return "sleep"
            self.y +=1
        if self.dpad.l.fell:
            if self.x==0: return "home"
            self.x -=1
        if self.dpad.r.fell:
            #todo change this to max # cards in the row
            if self.x==2: return "settings"
            self.x+=1
        if self.dpad.x.fell: self.details.hidden=not self.details.hidden
        self.card_grid[self.x,self.y]=self.y*2+2
        self.detaillabel.text="details of card\n at [" + str(self.x) + "," + str(self.y) + "]"
        return "cards"
