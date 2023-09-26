import board
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

    #creates all the animations
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

    #steps through brightness levels and applies
    def nextbrightness(self):
        self.pixels.brightness=self.brightnesslevels[(self.brightnesslevels.index(self.pixels.brightness) + 1) % len(self.brightnesslevels)]
        bright = int(self.pixels.brightness*100)
        return str(bright)+"%"

    #sets the current pattern to be displayed
    def nextpattern(self):
        self.currentpattern=(self.currentpattern+1)%len(self.ledpatterns)
        return self.ledpatterns[self.currentpattern].__qualname__[0:10]

    #chooses the next color, and then recreates all the animations with that color
    def nextcolor(self):
        self.color=self.colors[(self.colors.index(self.color) + 1) % len(self.colors)]
        self.initcolors()
        return self.color_name[self.colors.index(self.color)]

    #displays the currently selected animation
    def animate(self):
        self.ledpatterns[self.currentpattern].animate()