from adafruit_display_text import label
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF

class home:
    def __init__(self, group, dpad):
        self.dpad=dpad
        self.group=group

        self.header=label.Label(terminalio.FONT,text="Home - LABScon 2023", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        self.header=label.Label(terminalio.FONT,text="< - > change view", scale=1, color=WHITE, x=8, y=25)
        self.group.append(self.header)

        self.header=label.Label(terminalio.FONT,text="^ - V to trade", scale=1, color=WHITE, x=8, y=42)
        self.group.append(self.header)

        self.details=displayio.Group()
        self.details.hidden=False
        self.group.append(self.details)

    def update(self):
        if self.dpad.u.fell: return "trade"
        if self.dpad.d.fell: return "sleep"
        if self.dpad.l.fell: return "contacts"
        if self.dpad.r.fell: return "cards"
        if self.dpad.x.fell: return "about" #self.details.hidden=not self.details.hidden
        return "home"
