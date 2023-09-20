from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF


class settings:
    settings=["LED pattern","Change Name","Clear Clues","Clear Contacts"]

    def __init__(self, group, dpad, game):
        self.group=group
        self.dpad=dpad
        self.game=game

        self.header=label.Label(terminalio.FONT,text="Settings", color=BLACK, x=8, y=8)
        self.group.append(self.header)
        self.contents=label.Label(terminalio.FONT, scale=1, color=WHITE, x=8, y=24)
        self.contents.hidden=True
        self.group.append(self.contents)

        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True
        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))
        self.det=label.Label(terminalio.FONT,text="details", color=WHITE, x=4, y=8)
        self.details.append(self.det)
        self.group.append(self.details)

        self.x=0

    def update(self):
        newtext= "" if self.x == 0 else self.settings[self.x-1]
        newtext+="\n> "+self.settings[self.x]+"\n"
        newtext+= "" if self.x == len(self.settings)-1 else self.settings[self.x+1]
        self.contents.text=newtext
        self.contents.hidden=False
        self.det.text=self.settings[self.x]
        #musttodo: attach to functions
        if self.dpad.u.fell:
            self.x =(self.x-1)%len(self.settings)
        if self.dpad.d.fell:
            self.x =(self.x+1)%len(self.settings)
        if self.dpad.l.fell:
            return "clues"
        if self.dpad.r.fell:
            return "alibis"
        if self.dpad.x.fell:
            if self.details.hidden==True:
                if self.x==0:
                    #advance to next led mode
                    pass
                elif self.x==1:
                    pass
                    #change name by running oob code
                elif self.x==2:
                    self.det.text="Wipe ALL clues?\n'<' cancel\n'>' wipe"
                    self.details.hidden=False
                    while self.details.hidden==False:
                        self.dpad.update()
                        if self.dpad.l.fell:
                            self.details.hidden=True
                        if self.dpad.r.fell:
                            self.game.wipe_clues()
                            self.det.text="Clues Wiped!\n'<' to return"
                elif self.x==3:
                    self.det.text="Wipe all Alibis?\n'<' cancel\n'>' wipe"
                    self.details.hidden=False
                    while self.details.hidden==False:
                        self.dpad.update()
                        if self.dpad.l.fell:
                            self.details.hidden=True
                        if self.dpad.r.fell:
                            self.game.wipe_alibis()
                            self.det.text="Alibis Wiped!\n'<' to return"
                    #clear contacts
        return "settings"
