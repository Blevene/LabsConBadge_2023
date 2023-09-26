from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF

#alibis manage the alibi list. This persists across games. since one alibi can give
#you multiple clues, there's a litte more work to add that list of clues
class alibis:
    def __init__(self, group, dpad, game):
        self.group=group
        self.dpad=dpad
        self.game=game

        #black text on  white header
        self.header=label.Label(terminalio.FONT,text="Alibis", color=BLACK, x=8, y=8)
        self.group.append(self.header)
        #white text on the contents display
        self.contents=label.Label(terminalio.FONT, scale=1, color=WHITE, x=8, y=24)
        self.contents.hidden=True
        self.group.append(self.contents)
        #white text in the black details box
        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True
        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))
        self.det=label.Label(terminalio.FONT,text="details", color=WHITE, x=4, y=8)
        self.details.append(self.det)
        self.group.append(self.details)

        self.x=0

    def update(self):
        #there are 3 lines displayed. The middle line is the 'selected' one
        #and has a > in front

        #line 1 blank when at the top of the list, otherwise x-1
        newtext="" if self.x == 0 else self.game.alibis[self.x-1]
        #line 2 has a '>'
        newtext+="\n> "+self.game.alibis[self.x]+"\n"
        #line 3 blank when at the end of the list, otherwise x+1
        newtext+= "" if self.x == len(self.game.alibis)-1 else self.game.alibis[self.x+1]
        self.contents.text=newtext
        self.contents.hidden=False

        #not much to show on the details yet
        self.det.text=self.game.alibis[self.x]+"\n\nNothing else to see here"

        #u and d scroll through the list. l and r navigate. x toggles details
        if self.dpad.u.fell:
            self.x =(self.x-1)%len(self.game.alibis)
        if self.dpad.d.fell:
            self.x =(self.x+1)%len(self.game.alibis)
        if self.dpad.l.fell:
            self.contents.hidden=True
            self.details.hidden=True
            return "settings"
        if self.dpad.r.fell:
            self.contents.hidden=True
            self.details.hidden=True
            return "home"
        if self.dpad.x.fell:
            self.details.hidden=not self.details.hidden
        return "alibis"
