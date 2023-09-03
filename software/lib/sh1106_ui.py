import displayio
import board
import busio
import adafruit_displayio_sh1106

BLACK=0x000000
WHITE=0xFFFFFF

class sh1106ui:
    WIDTH = 130
    HEIGHT = 64
    BORDER = 10

    #initialize display; if already initialized, pass the device. If not, then initialize the default
    def __init__(self,display=None):

        #initialize display
        if display is None:
            displayio.release_displays()
            #i2c = busio.I2C(board.SCL1, board.SDA1)
            i2c=board.I2C()
            display_bus=displayio.I2CDisplay(i2c,device_address=60)
            self.display = adafruit_displayio_sh1106.SH1106(display_bus, width=self.WIDTH, height=self.HEIGHT)
        else:
            self.display=display


        #todo: use a single palette

        # Make maingroup to hold stuff
        self.maingroup = displayio.Group()
        self.maingroup.hidden=True
        self.display.show(self.maingroup)

        # make a background in the back of header
        color_bitmap = displayio.Bitmap(self.WIDTH, 16, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = WHITE

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        self.maingroup.append(bg_sprite)
        
        #make pagegroups that contains a separate group for each page
        self.pagegroup = displayio.Group()
        self.pagegroup.x = -260
        self.maingroup.append(self.pagegroup)
        self.settingsgroup = displayio.Group()
        self.settingsgroup.x=0
        self.pagegroup.append(self.settingsgroup)
        self.contactsgroup = displayio.Group()
        self.contactsgroup.x=130
        self.pagegroup.append(self.contactsgroup)
        self.homegroup = displayio.Group()
        self.homegroup.x=260
        self.pagegroup.append(self.homegroup)
        self.cardsgroup = displayio.Group()
        self.cardsgroup.x=390
        self.pagegroup.append(self.cardsgroup)

        # make trade group overlay
        self.tradegroup = displayio.Group()
        self.tradegroup.y=-64
        self.tradegroup.x=16
        self.maingroup.append(self.tradegroup)
