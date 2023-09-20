# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
import storage

# EDIT ME the toggle switch pin goes here!
switch = digitalio.DigitalInOut(board.D1)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
usbpower = digitalio.DigitalInOut(board.D0)
usbpower.direction = digitalio.Direction.INPUT
usbpower.pull = digitalio.Pull.UP

# If the switch pin is connected to ground CircuitPython can write to the drive
# true: usb write
# false: circuitpython write
# usb write when usb power and and switch is not pressed (true)
# circuitpython write when no usb power (false)
# circuitpyton write when switch pressed (false)
storage.remount("/", usbpower.value and switch.value)
