from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF

class home:
    def __init__(self, group, dpad):
        self.group=group
        self.dpad=dpad

        self.header=label.Label(terminalio.FONT,text="Home - LABScon 2023", color=BLACK, x=8, y=8)
        self.group.append(self.header)
        self.header=label.Label(terminalio.FONT,text="< - > change view\n^ - V to trade", scale=1, color=WHITE, x=8, y=42)
        self.group.append(self.header)

        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True

        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))

        self.detailtext=label.Label(terminalio.FONT,text="about", color=WHITE, x=3, y=8)
        self.details.append(self.detailtext)

        self.group.append(self.details)

    def update(self):
        if self.dpad.u.fell: return "trade"
        if self.dpad.d.fell: return "sleep"
        if self.dpad.l.fell: return "alibis"
        if self.dpad.r.fell: return "clues"
        if self.dpad.x.fell: self.details.hidden=not self.details.hidden
        return "home"
