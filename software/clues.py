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

#clues manages the clues display in the game
#it needs access to the display group to drawon, dpad for control
#and game data structure
class clues:
    def __init__(self, group, dpad, game):
        self.group=group
        self.dpad=dpad
        self.game=game

        #Create the title in black text on the existing white header bar
        self.header=label.Label(terminalio.FONT,text="Clues, Game 0", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        #create a layout of all the clues using a sprite table
        clue_sheet, palette = adafruit_imageload.load("assets/clues.bmp",bitmap=displayio.Bitmap, palette=displayio.Palette)
        self.clue_grid = displayio.TileGrid(clue_sheet, pixel_shader=palette,
            width=13, height=3,
            tile_width=12, tile_height=16)
        self.clue_group=displayio.Group(y=15)
        self.clue_group.append(self.clue_grid)
        self.group.append(self.clue_group)

        #create a hidden detail overlay that is shown when the d-pad is pressed
        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True
        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))
        self.detaillabel=label.Label(terminalio.FONT,text="About", color=WHITE, x=4, y=8)
        self.details.append(self.detaillabel)
        self.group.append(self.details)

        #lay out all the cards, and set the initial position 
        self.setcards()
        #highlight the currently selected card
        self.clue_grid[self.x,self.y]+=1


    def setcards(self):
        #update header based on curent game number
        self.header.text="Clues, game # " + str(self.game.gamenum)
        #for each row of clues:
        for j, cluetype in enumerate([self.game.threats,self.game.attacks,self.game.victims]):
            count=0
            last=None
            #clear out any existing cards displayed
            for i in range(13):
                self.clue_grid[i,j]=0
            for i in range(self.game.cluecounts[j]):
                #if the clue has been collected, show the clue type
                if cluetype[i][4] != "":
                    self.clue_grid[i,j]=j*2+1
                    print(cluetype[i][4],"has",cluetype[i][1])
                #otherwise, show a '?' - but keep track of how many
                else:
                    self.clue_grid[i,j]=7
                    last=i
                    count+=1
                    print("not yet:",cluetype[i][1])
            #if there was only 1 unkown clue, it's the solution - mark it '!'
            if count==1:
                self.clue_grid[last,j]=9
                cluetype[last][3]="!"
                print("solved",cluetype[last][1])
        #set initial position
        self.x=0
        self.y=0

    #process inputs and changes to state
    def update(self):
        #show grid
        self.clue_group.hidden=False
        #un-highlight current clue
        self.clue_grid[self.x,self.y]-=1
        #if new clue, go to it
        if self.game.newclue != None:
            #todo: remove if/else short circuit
            if True or self.game.newclue == -1:
                #if newclue=-1, we just need to update the display
               self.setcards()
               self.game.newclue=None
            else:
                #otherwise, set x,y to the newclue and show details
                self.x,self.y=self.game.newclue
                self.details.hidden=False
                self.game.newclue=None
        if self.dpad.u.fell:
            #pressing u at the top of the screen goes to trade
            if self.y==0:
                self.clue_grid[self.x,self.y]+=1
                return "trade"
            #otherwise just moves the cursor up
            self.y -=1
            self.x=min(self.x,self.game.cluecounts[self.y]-1)
        if self.dpad.d.fell:
            #pressing d at the bottom goes to sleep
            if self.y==2:
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "sleep"
            #otherwise just moves the cursor down
            self.y +=1
            self.x=min(self.x,self.game.cluecounts[self.y]-1)
        if self.dpad.l.fell:
            #l at the left goes back to home
            if self.x==0:
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "home"
            self.x -=1
        if self.dpad.r.fell:
            #r and the right goes around to settings
            if self.x==self.game.cluecounts[self.y]-1:
                self.clue_group.hidden=True
                self.details.hidden=True
                self.clue_grid[self.x,self.y]+=1
                return "settings"
            self.x+=1
        if self.dpad.x.fell:
            #x shows or hides details
            self.details.hidden=not self.details.hidden
        #highlight the current selelcted clue
        self.clue_grid[self.x,self.y]+=1
        #get the right clue for printing...
        if self.y==0: clue=self.game.threats[self.x]
        elif self.y==1: clue=self.game.attacks[self.x]
        else: clue=self.game.victims[self.x]
        #...and use it in the details text string
        if clue[3]=="!":
            self.detaillabel.text="Attribution!\nIt was\n"+clue[1]
        elif clue[4]=="":
            self.detaillabel.text="Could've been\n"+clue[1]
        elif clue[4]==self.game.myname:
            self.detaillabel.text="I know it wasn't\n"+clue[1]
        else:
            self.detaillabel.text=clue[4]+"\nknows it wasn't\n"+clue[1]
        return "clues"