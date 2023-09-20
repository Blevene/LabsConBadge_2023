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

import neopixel
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
import adafruit_led_animation.color as color

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

class ledcontrol:
    pixel_pin = board.NEOPIXEL
    num_pixels = 10
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3)
    ledpatterns=[]
    currentpattern=0

    def __init__(self):
        self.ledpatterns.append(RainbowComet(self.pixels,0.1,ring=True))
        self.ledpatterns.append(Rainbow(self.pixels,0.1))
        for c in [color.RED,color.ORANGE,color.YELLOW,color.GREEN,color.BLUE,color.PURPLE,color.WHITE]:
            self.ledpatterns.append(Comet(self.pixels,0.1,c,tail_length=5,ring=True))
            self.ledpatterns.append(Solid(self.pixels,c))
            self.ledpatterns.append(Pulse(self.pixels,0.03,c))

    def nextpattern(self):
        self.currentpattern=(self.currentpattern+1)%len(self.ledpatterns)
        return self.ledpatterns[self.currentpattern].__qualname__

    def animate(self):
        self.ledpatterns[self.currentpattern].animate()

        
leds=ledcontrol()

game=gamedata(1)
#musttodo advance game numbers
#musttodo add nepoixels
homepage=home(display.homegroup,dpad)
cluespage=clues(display.cluesgroup,dpad,game)
settingspage=settings(display.settingsgroup,dpad,game,leds)
alibispage=alibis(display.alibisgroup,dpad,game)
tradepage=trade(display.tradegroup,dpad,game)
sleeppage=sleep(display,dpad)

page="sleep"
lastpage="home"
SLEEPTIMEOUT=90
while True:
    leds.animate()
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
