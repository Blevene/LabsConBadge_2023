from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF

class home:
    currentstring=0
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
        self.contents.hidden=True
        self.group.append(self.contents)

    def update(self):
        self.contents.hidden=False
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
