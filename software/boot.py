# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
import storage

# switch is connected to the up direction on the d-pad
switch = digitalio.DigitalInOut(board.D1)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
# usbpower is connected to the output of the usb 3.3v regulator
usbpower = digitalio.DigitalInOut(board.D0)
usbpower.direction = digitalio.Direction.INPUT
usbpower.pull = digitalio.Pull.DOWN

# true: usb write
# false: circuitpython write
# usb write when usb power connected (=true) AND switch is not pressed (=true)
# circuitpython write when no usb power (=false)
# circuitpyton write when switch pressed (=false)
storage.remount("/", usbpower.value and switch.value)
