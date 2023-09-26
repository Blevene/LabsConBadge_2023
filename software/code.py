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

from leds import ledcontrol
from home import home
from clues import clues
from alibis import alibis
from settings import settings
from trade import trade
from sleep import sleep
from game import gamedata

BLACK=0x000000
WHITE=0xFFFFFF

#display, dpad, and leds wrap access to physical I/O
display=sh1106ui()
dpad=FiveWayPad()
leds=ledcontrol()

#instantiate home first, since it manages OOB.
homepage=home(display.homegroup,dpad)
#next, load game data since we know we have a username
game=gamedata(0)
#finally, create the other view pages, most of which need to access
#a single display group, dpad state, and game data
cluespage=clues(display.cluesgroup,dpad,game)
settingspage=settings(display.settingsgroup,dpad,game,leds)
alibispage=alibis(display.alibisgroup,dpad,game)
tradepage=trade(display.tradegroup,dpad,game)
sleeppage=sleep(display,dpad)

#start out on the home page
page="home"
lastpage="home"

SLEEPTIMEOUT=90
while True:
    #update leds and display
    leds.animate()
    if page!=0: display.show(page)

    #scan inputs
    dpad.update()

    #sleep if it's been a while - except trade page
    if dpad.duration() > SLEEPTIMEOUT and page != "trade":
        page=sleeppage.update()

    #if a button is pressed, handle it
    if not dpad.pressed():
        time.sleep(0.001)
    elif page == "home":
        lastpage=page
        page=homepage.update()
    elif page == "settings":
        lastpage=page
        page=settingspage.update()
    elif page == "alibis":
        lastpage=page
        page=alibispage.update()
    elif page == "clues":
        lastpage=page
        page=cluespage.update()
    elif page == "trade":
        page=tradepage.update()
    elif page == "sleep":
        page=sleeppage.update()
    else: page=lastpage