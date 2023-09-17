from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF


class settings:
    def __init__(self, group, dpad):
        self.group=group
        self.dpad=dpad
        self.header=label.Label(terminalio.FONT,text="settings", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True
        self.group.append(self.details)

        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))

        self.det=label.Label(terminalio.FONT,text="details", color=WHITE, x=4, y=8)
        self.details.append(self.det)

    def update(self):
        if self.dpad.u.fell: return "trade"
        if self.dpad.d.fell: return "sleep"
        if self.dpad.l.fell: return "clues"
        if self.dpad.r.fell: return "alibis"
        if self.dpad.x.fell: self.details.hidden=not self.details.hidden
        return "settings"
