import board
import digitalio
from adafruit_debouncer import Debouncer

# this module combines all 5 buttons into a single class and debounces all buttons
#
#to use:
#from five_way_pad import FiveWayPad
#dpad=FiveWayPad()
#while True:
#  dpad.update
#  if dpad.u.fell: print ("u") # debounced, only once
#  if not dpad.d.value: print ("d") # repeats as long as pressed
#


class FiveWayPad:
    #create all 5 debounced buttons. Defaults are what are used on prototype and production badges
    def __init__(self,l=board.D10,r=board.D9,u=board.D1,d=board.D2,x=board.D3):
        self.u=self.initbtn(u)
        self.d=self.initbtn(d)
        self.l=self.initbtn(l)
        self.r=self.initbtn(r)
        self.x=self.initbtn(x)

    #helper to configure a pin and debounce it
    def initbtn(self,pin):
        tmp = digitalio.DigitalInOut(pin)
        tmp.direction=digitalio.Direction.INPUT
        tmp.pull=digitalio.Pull.UP
        return Debouncer(tmp)
        
    #update all buttons
    def update(self):
        self.u.update()
        self.d.update()
        self.l.update()
        self.r.update()
        self.x.update()

    #return true if any button is pressed (pulled down)
    def pressed(self):
        return not (self.u.value and self.d.value and self.l.value and self.r.value and self.x.value)
