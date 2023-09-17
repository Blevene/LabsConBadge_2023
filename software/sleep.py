from sh1106_ui import sh1106ui

class sleep:
    def __init__(self, display, dpad):
        self.dpad=dpad
        self.display=display

    def update(self):
        #self.display.header.text="sleep"
        if self.dpad.x.fell:
            self.display.maingroup.hidden=False
            return 0 # will return to last normal page
        elif self.dpad.u.fell:
            self.display.maingroup.hidden=False
            return "trade"
        self.display.maingroup.hidden=True
        return "sleep"
