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
from sh1106_ui import sh1106ui, box
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

homepage=home(display.homegroup,dpad)
cardspage=cards(display.cardsgroup,dpad)
settingspage=settings(display.settingsgroup,dpad)
contactspage=contacts(display.contactsgroup,dpad)
tradepage=trade(display.tradegroup,dpad)
sleeppage=sleep(display,dpad)

page="sleep"
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
        time.sleep(0.001)
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
