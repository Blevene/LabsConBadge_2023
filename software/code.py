import time
import gc
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
from clues import clues
from alibis import alibis
from settings import settings
from trade import trade
from sleep import sleep
from game import gamedata

BLACK=0x000000
WHITE=0xFFFFFF

display=sh1106ui()
dpad=FiveWayPad()

game=gamedata(1)
#musttodo advance game numbers

#musttodo oob experience
#if not (load name and current game from file)
    #"Welcome to the Attribution Game!"
    #"Meet people and trade clues to attribute the attack"
    #"You don't have a handle yet"
    #"Your handle will be shared with people you meet"
    #" ^v to choose characters > for next"
    #"welcome to the game @user"
    #"press ^ and point your badge at someone else to trade"
    #"the combo with no alibi is the solution."
    #"have fun!"
#load game data from file
#load contacts from file

#musttodo add nepoixels

homepage=home(display.homegroup,dpad)
cluespage=clues(display.cluesgroup,dpad,game)
settingspage=settings(display.settingsgroup,dpad)
alibispage=alibis(display.alibisgroup,dpad,game)
tradepage=trade(display.tradegroup,dpad,game)
sleeppage=sleep(display,dpad)

page="sleep"
lastpage="home"
SLEEPTIMEOUT=90
while True:
    gc.collect()
    #scan inputs
    dpad.update()
    if page!=0: display.show(page)
    #if dpad.duration() > SLEEPTIMEOUT and page != "trade": 
    #    page=sleeppage.update()
    #if a button is pressed, handle it
    if not dpad.pressed():
        time.sleep(0.001)
    elif page == "home":
        lastpage=page
        page=homepage.update()
    elif page == "about":
        page=aboutpage.update()
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
