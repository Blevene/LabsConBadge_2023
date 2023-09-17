from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF


class alibis:
    def __init__(self, group, dpad):
        self.group=group
        self.dpad=dpad

        self.header=label.Label(terminalio.FONT,text="alibis", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        self.details=displayio.Group(x=8,y=4)
        self.details.hidden=True
        self.group.append(self.details)

        self.details.append(box(112,56,WHITE,0,0))
        self.details.append(box(110,54,BLACK,1,1))

        self.det=label.Label(terminalio.FONT,text="details", color=WHITE, x=4, y=8)
        self.details.append(self.det)


        self.alibilist=["@securelyfitz","@blevene","@oscontext","@4","@5","@6"]
        self.x=0
        self.y=0

    def update(self):
        if self.dpad.u.fell:
            if self.x==0: return "trade"
            self.x -=1
        if self.dpad.d.fell:
            if self.x==0: return "sleep"
            self.x +=1
        if self.dpad.l.fell:
            if self.y==0: return "settings"
            self.y -=1
        if self.dpad.r.fell:
            if self.y==0: return "home"
            self.y+=1
        if self.dpad.x.fell: self.details.hidden=not self.details.hidden
        return "alibis"
