import displayio
import board
import busio
import adafruit_displayio_sh1106
import terminalio
from adafruit_display_text import label
import time


class sh1106ui:
    WIDTH = 130
    HEIGHT = 64
    BORDER = 10

    #initialize display; if already initialized, pass the device. If not, then initialize the default
    def __init__(self,display=None):
        if display is None:
            displayio.release_displays()
            #i2c = busio.I2C(board.SCL1, board.SDA1)
            i2c=board.I2C()
            display_bus=displayio.I2CDisplay(i2c,device_address=60)
            self.display = adafruit_displayio_sh1106.SH1106(display_bus, width=self.WIDTH, height=self.HEIGHT)
        else:
            self.display=display

        # Make the display context
        self.splash = displayio.Group()
        self.splash.hidden=True
        self.display.show(self.splash)

        color_bitmap = displayio.Bitmap(self.WIDTH, self.HEIGHT, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0xFFFFFF  # White

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        self.splash.append(bg_sprite)
        
        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(self.WIDTH, self.HEIGHT - self.BORDER, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = 0x000000  # Black
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=0, y=self.BORDER
        )
        self.splash.append(inner_sprite)

        # Draw a label
        self.header = label.Label(terminalio.FONT, text="home", color=0x000000, x=10, y=5)
        self.splash.append(self.header)
        self.details = label.Label(terminalio.FONT, text="details", color=0xFFFFFF, x=self.BORDER*2, y=self.HEIGHT // 2 + 1)
        self.details.hidden=True
        self.splash.append(self.details)


    def drawtext(self,text="Hello LABSCON"):
        self.text_area.text=text
