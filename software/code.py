import time
import board
import busio
import pulseio
import digitalio
import displayio
import terminalio
import adafruit_imageload
import adafruit_displayio_sh1106
from fake_irda import FakeIRDA
from sh1106_ui import sh1106ui
from five_way_pad import FiveWayPad
from adafruit_display_text import label
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

from home import home
from clues import cards
from alibis import contacts
from settings import settings
from trade import trade
from sleep import sleep

BLACK=0x000000
WHITE=0xFFFFFF

display=sh1106ui()
dpad=FiveWayPad()

class about:
    def __init__(self, group, dpad):
        self.dpad=dpad
        self.group=group

        self.group.append(display.box(116,48,WHITE,0,0))
        self.group.append(display.box(114,31,BLACK,1,16))

        self.header=label.Label(terminalio.FONT,text="About", color=BLACK, x=24, y=8)
        self.group.append(self.header)

        self.details=label.Label(terminalio.FONT,text="Hack the Planet", color=WHITE, x=12, y=32)
        self.group.append(self.details)

    def update(self):
        #show trade page
        self.group.y=8

        while True:

            # process keypresses
            # if dpad.u.fell: self.group.y=-64
            # if dpad.d.fell: self.group.y=-64
            # if dpad.l.fell: self.group.y=-64
            # if dpad.r.fell: self.group.y=-64
            if dpad.x.fell or dpad.r.fell or dpad.l.fell or dpad.d.fell or dpad.u.fell: 
                self.group.y=-64 #return "about" #self.details.hidden=not self.details.hidden
                print("X")
                return "home"
            return "about"

homepage=home(display.homegroup,dpad)
cardspage=cards(display, display.cardsgroup,dpad)
settingspage=settings(display, display.settingsgroup,dpad)
contactspage=contacts(display, display.contactsgroup,dpad)
tradepage=trade(display, display.tradegroup,dpad)
aboutpage=about(display.aboutpopupgroup,dpad)
sleeppage=sleep(display,dpad)

page="home"
lastpage="home"
SLEEPTIMEOUT=90
while True:
    #scan inputs
    # print("update loop:",page)
    #time.sleep(1)
    dpad.update()
    display.show(page)
    #go to sleep if timeout
    if dpad.duration() > SLEEPTIMEOUT and page != "trade": page=sleeppage.update()
    #if a button is pressed, handle it
    elif not dpad.pressed():
        time.sleep(0.01)
    elif page == "home":
        lastpage=page
        page=homepage.update()
    elif page == "about":
        page=aboutpage.update()
    elif page == "settings":
        lastpage=page
        page=settingspage.update()
    elif page == "contacts":
        lastpage=page
        page=contactspage.update()
    elif page == "cards":
        lastpage=page
        page=cardspage.update()
    elif page == "trade":
        page=tradepage.update()
    elif page == "sleep":
        page=sleeppage.update()
    else: page=lastpage
