from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF


class settings:
    settings=["LED Style","LED Color","LED Brightness", "Clear Name","Clear Clues","Clear Contacts","LEDs Off","Advance Game"]

    def __init__(self, group, dpad, game, leds):
        self.group=group
        self.dpad=dpad
        self.game=game
        self.leds=leds

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
                    self.settings[self.x]="Style: "+ self.leds.nextpattern()
                elif self.x==1:
                    #advance to next led color
                    self.settings[self.x]="Color: "+ self.leds.nextcolor()
                elif self.x==2:
                    #advance to next brightness
                    self.settings[self.x]="Brightness: "+ self.leds.nextbrightness()
                elif self.x==3:
                    #change name by setting to "" and forcing power cycle
                    self.det.text="Wipe your name?\n'<' cancel\n'>' wipe"
                    self.details.hidden=False
                    while self.details.hidden==False:
                        self.dpad.update()
                        if self.dpad.l.fell:
                            self.details.hidden=True
                        if self.dpad.r.fell:
                            self.game.wipe_name()
                            self.det.text="Name Wiped!\n Power cycle\n to continue"
                            while True:
                                pass
                elif self.x==4:
                    #clear clues
                    self.det.text="Wipe ALL clues?\n'<' cancel\n'>' wipe"
                    self.details.hidden=False
                    while self.details.hidden==False:
                        self.dpad.update()
                        if self.dpad.l.fell:
                            self.details.hidden=True
                        if self.dpad.r.fell:
                            self.game.wipe_clues()
                            self.det.text="Clues Wiped!\n'<' to return"
                elif self.x==5:
                    #clear contacts
                    self.det.text="Wipe all Alibis?\n'<' cancel\n'>' wipe"
                    self.details.hidden=False
                    while self.details.hidden==False:
                        self.dpad.update()
                        if self.dpad.l.fell:
                            self.details.hidden=True
                        if self.dpad.r.fell:
                            self.game.wipe_alibis()
                            self.det.text="Alibis Wiped!\n'<' to return"
                elif self.x==6:
                    #leds off
                    self.leds.currentpattern=0
                elif self.x==7:
                    #advance game
                    self.game.gamenum=(self.game.gamenum+1)%8
                    self.game.gamefile="data/game"+str(self.game.gamenum)+".csv"
                    self.settings[self.x]="Game #"+str(self.game.gamenum)
                    self.game.read_clues()
                    self.game.newclue=-1
        return "settings"
