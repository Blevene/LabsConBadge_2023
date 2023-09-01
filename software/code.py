import board
import digitalio
import busio
import time
import pulseio
from five_way_pad import FiveWayPad
from sh1106_ui import sh1106ui

display=sh1106ui()
dpad=FiveWayPad()

class home:
    def __init__(self, display, dpad):
        self.dpad=dpad
        self.display=display

    def update(self):
        self.display.header.text="home"
        if dpad.u.fell: return "trade"
        if dpad.d.fell: return "sleep"
        if dpad.l.fell: return "contacts"
        if dpad.r.fell: return "cards"
        if dpad.x.fell: display.details.hidden=not display.details.hidden
        return "home"

class cards:
    def __init__(self, display, dpad):
        self.dpad=dpad
        self.display=display

    def update(self):
        self.display.header.text="cards"
        if dpad.u.fell: return "trade"
        if dpad.d.fell: return "sleep"
        if dpad.l.fell: return "home"
        if dpad.r.fell: return "settings"
        if dpad.x.fell: display.details.hidden=not display.details.hidden
        return "cards"

class contacts:
    def __init__(self, display, dpad):
        self.dpad=dpad
        self.display=display

    def update(self):
        self.display.header.text="contacts"
        if dpad.u.fell: return "trade"
        if dpad.d.fell: return "sleep"
        if dpad.l.fell: return "settings"
        if dpad.r.fell: return "home"
        if dpad.x.fell: display.details.hidden=not display.details.hidden
        return "contacts"

class settings:
    def __init__(self, display, dpad):
        self.dpad=dpad
        self.display=display

    def update(self):
        self.display.header.text="settings"
        if dpad.u.fell: return "trade"
        if dpad.d.fell: return "sleep"
        if dpad.l.fell: return "cards"
        if dpad.r.fell: return "contacts"
        if dpad.x.fell: display.details.hidden=not display.details.hidden
        return "settings"

class trade:
    def __init__(self, display, dpad):
        self.dpad=dpad
        self.display=display

    def update(self):
        self.display.header.text="trade"
        if dpad.d.fell: return 0 # will return to last normal page
        if dpad.x.fell: display.details.hidden=not display.details.hidden
        return "trade"

class sleep:
    def __init__(self, display, dpad):
        self.dpad=dpad
        self.display=display

    def update(self):
        #self.display.header.text="sleep"
        if dpad.u.fell:
            display.splash.hidden=False
            return 0 # will return to last normal page
        display.splash.hidden=True
        return "sleep"

homepage=home(display,dpad)
cardspage=cards(display,dpad)
settingspage=settings(display,dpad)
contactspage=contacts(display,dpad)
tradepage=trade(display,dpad)
sleeppage=sleep(display,dpad)
page="sleep"
lastpage="home"

while True:
    #scan inputs
    dpad.update()
    #go to sleep if timeout
    if dpad.duration()>5 : page=sleeppage.update()
    #if a button is pressed, handle it
    elif not dpad.pressed():
        time.sleep(0.01)
    elif page is "home":
        lastpage=page
        page=homepage.update()
    elif page is "settings":
        lastpage=page
        page=settingspage.update()
    elif page is "contacts":
        lastpage=page
        page=contactspage.update()
    elif page is "cards":
        lastpage=page
        page=cardspage.update()
    elif page is "trade": page=tradepage.update()
    elif page is "sleep": page=sleeppage.update()
    else: page=lastpage
