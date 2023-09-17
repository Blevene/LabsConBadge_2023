from adafruit_display_text import label
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF


class contacts:
    def __init__(self, display, group, dpad):
        self.display=display
        self.group=group
        self.dpad=dpad

        self.header=label.Label(terminalio.FONT,text="contacts", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        self.details=displayio.Group()
        self.details.hidden=True
        self.group.append(self.details)

        self.contactlist=["@securelyfitz","@blevene","@oscontext","@4","@5","@6"]
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
        return "contacts"
