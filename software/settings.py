from adafruit_display_text import label
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF


class settings:
    def __init__(self, display, group, dpad):
        self.display=display
        self.group=group
        self.dpad=dpad
        self.header=label.Label(terminalio.FONT,text="settings", color=BLACK, x=8, y=8)
        self.group.append(self.header)
        self.details=displayio.Group()
        self.details.hidden=True
        self.group.append(self.details)

    def update(self):
        if self.dpad.u.fell: return "trade"
        if self.dpad.d.fell: return "sleep"
        if self.dpad.l.fell: return "cards"
        if self.dpad.r.fell: return "contacts"
        #if self.dpad.x.fell: self.display.details.hidden=not self.display.details.hidden
        return "settings"
