import board
import digitalio
import busio
import time
import pulseio
from five_way_pad import FiveWayPad
from sh1106_ui import sh1106ui

display=sh1106ui()
dpad=FiveWayPad()

while True:
    dpad.update()
    if dpad.u.fell: display.text_area.text="u"
    if dpad.d.fell: display.text_area.text="d"
    if dpad.l.fell: display.text_area.text="l"
    if dpad.r.fell: display.text_area.text="r"
    if dpad.x.fell: display.text_area.text="x"
~
