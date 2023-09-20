from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF

class home:
    currentstring=0
    #musttodo: fix strings, add sponsors
    #todo: sponsor images

    strings=[
            "< - > change view\n^ - v to trade\nPress for more",
            "Page 2",
            "Thank you sponsors",
            "how to play",
            "",
            ]

    def __init__(self, group, dpad):
        self.group=group
        self.dpad=dpad

        self.header=label.Label(terminalio.FONT,text="LABScon 2023", color=BLACK, x=24, y=8)
        self.group.append(self.header)
        self.contents=label.Label(terminalio.FONT,text=self.strings[0], scale=1, color=WHITE, x=8, y=24)
        self.contents.hidden=False
        self.group.append(self.contents)

        try:
            with open("data/myname.txt",'r') as file:
                name=file.readline().rstrip()
        except OSError:
            name=""
        
        if name=="":
            self.showandwait("        The\n    Attribution\n       Game!      v")
            self.showandwait("Meet people & trade\n clues to attribute \n the attack       v")
            self.showandwait("You don't have\n a handle yet!\n                  v")
            self.showandwait("Your handle \nwill be shared with\n people you meet  v")
            self.showandwait(" ^v to choose chars\n > for next\n > > when done    v")
            #musttodo add name entry
            self.showandwait("welcome\n to the game\n"+name+"!")
            self.showandwait("press '^' & point @\n another to trade \n contacit & clues v")
            self.showandwait("The combo w/o alibi\n is the solution!\n                  v")
            self.showandwait("Have fun!\n\n                  v")

    def showandwait(self,mystring):
        self.contents.text=mystring
        self.dpad.update()
        while not self.dpad.d.fell:
            self.dpad.update()


    def update(self):
        self.contents.hidden=False
        #todo: make display auto-advance
        #todo: don't sleep till done?
        if self.dpad.u.fell: 
            self.contents.hidden=True
            return "trade"
        if self.dpad.d.fell: 
            self.contents.hidden=True
            return "sleep"
        if self.dpad.l.fell: 
            self.contents.hidden=True
            return "alibis"
        if self.dpad.r.fell: 
            self.contents.hidden=True
            return "clues"
        if self.dpad.x.fell: 
            self.currentstring=(self.currentstring+1)%(len(self.strings))
            print(self.strings[self.currentstring])
            self.contents.text=self.strings[self.currentstring]
        return "home"
