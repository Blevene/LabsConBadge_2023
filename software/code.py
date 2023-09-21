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
    colors = [color.RED,color.ORANGE,color.YELLOW,color.GREEN,color.BLUE,color.PURPLE,color.WHITE]
    color_name = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "White"]
    color = colors[0]
    brightnesslevels = [0.02, 0.15, 0.3, 0.5]
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3)
    ledpatterns=[]
    currentpattern=0

    def __init__(self):
        self.initcolors()

    def initcolors(self):
        self.ledpatterns = [
            Solid(self.pixels,color.BLACK),
            RainbowComet(self.pixels,0.1,ring=True),
            Rainbow(self.pixels,0.1),
            Chase(self.pixels,0.1,self.color),
            Comet(self.pixels,0.1,self.color,tail_length=4,ring=True),
            Solid(self.pixels,self.color),
            Pulse(self.pixels,0.03,self.color),
        ]

    def nextbrightness(self):
        self.pixels.brightness=self.brightnesslevels[(self.brightnesslevels.index(self.pixels.brightness) + 1) % len(self.brightnesslevels)]
        bright = int(self.pixels.brightness*100)
        return str(bright)+"%"

    def nextpattern(self):
        self.currentpattern=(self.currentpattern+1)%len(self.ledpatterns)
        return self.ledpatterns[self.currentpattern].__qualname__[0:10]

    def nextcolor(self):
        self.color=self.colors[(self.colors.index(self.color) + 1) % len(self.colors)]
        self.initcolors()
        return self.color_name[self.colors.index(self.color)]

    def animate(self):
        self.ledpatterns[self.currentpattern].animate()


leds=ledcontrol()

homepage=home(display.homegroup,dpad)
game=gamedata(0)
cluespage=clues(display.cluesgroup,dpad,game)
settingspage=settings(display.settingsgroup,dpad,game,leds)
alibispage=alibis(display.alibisgroup,dpad,game)
tradepage=trade(display.tradegroup,dpad,game)
sleeppage=sleep(display,dpad)

page="home"
lastpage="home"
SLEEPTIMEOUT=90
while True:
    # GC before animation smooths out animations
    gc.collect()
    leds.animate()
    #scan inputs
    dpad.update()
    if page!=0: display.show(page)
    if dpad.duration() > SLEEPTIMEOUT and page != "trade":
        page=sleeppage.update()
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
