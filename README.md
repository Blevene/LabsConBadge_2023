# LabsConBadge_2023
LabsConBadge 2023

The 2023 Labscon Badge is designed for playing the Attribution Game. Similar to the board game Clue or some versions of Carmen Sandiego, you need to figure out who the threat actor, attack tool, and victim are for each round of the game. You do this by trading 'cards' or 'clues' (as well as your contact information) with others at the conference.

Each badge has one card, and you are an alibi for that card. As you 'trade' cards with others, you rule out all the actors, tools, and victims that have alibis until you can attribute the whole attack.

We believe the game is cryptographically protected against a malicious attendee cheating or otherwise spoiling the game, and we eagerly await challenges to that expectation.

This repository contains the hardware and software made to implement the badge and game. We hope it is useful for those who wish to hack the badges and game, anyone who wants to use the badge to learn some circuitpython, as well as others who might like to reuse some or all of it for other projects.

# Using the Badge
## Setup
When you first power on your bage it will give you a brief intro to the badge and the game, then it will ask you for your contact info. This could be a handle, email address, or any other string that will be shared with everyone you interact with. Use the up and down buttons to choose letters, left and right to move through the string, and press the button to set your name. (it can be changed later)
## Navigating
-Left and Right switches between:
 -Home page
 - Contacts page, which shows all the people you've traded contact info with
 - Cards page, which shows all the cards you've collected so far
 - Settings, which allow you to change badge features
- Up takes you to trade mode, described below
- Down puts the badge to sleep, which also happens automatically after a few seconds
- Pressing the button usually gives you more details about whatever you're highlighting.
## Trading
Your badge has an infrared transciever. Press the 'up' button to enter trade mode. The badge will:
- transmit your 'card' as well as your contact information
- listen to recieve someone elses card and contact info
- tell you the result of the trade.
After the trade, you should be able to see the information in your Contacts an Cards pages.
## Winning
The real prize isn't attribution but the contacts and friends we made along the way. If you happen to have collected enough info to attribute the attack, your badge will tell you. Find a game organizer to validate your win.
## Multiple rounds
The first round of the game will be pretty easy with only a few trades needed to attribute. Once a game is complete, the game controller will transmit a packet to advance the game to the next round, which will propogate to everyone when they trade clues. Each round will have a different set of cards/clues and a different attack to attribute.

# After the conference
This badge can work as a simple circuitpython learning platform. The best source of information about circuitpython is available on Adafruit, including a [Welcome to CircuitPython guide](https://learn.adafruit.com/welcome-to-circuitpython/overview)

The best place to start tinkering is probably with some neat light animations on the 10 RGB LEDs on the badge. Adafruit [has an example](https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Welcome_to_CircuitPython/code.py) on how to use these RGB LEDs.

For working interactively with a python CLI, plug your badge in with a USB cable, and connect to the serial port that shows up.

For writing your own circuitpython programs, you need to modify the code.py file you can find on the drive that shows up when you plug in the USB cable. Every time you save the file, the board will reset and start running your code.

If you've somehow messed up your badge, you can follow the process below to flash a fresh copy of circuitypython and/or the game code.

# Working with the badge
## Installing CircuitPython
When the RP2040 boots, it checks for valid data in the spi flash. If it doesn't, it boots into USB bootloader mode and shows up as a drive labeled RPI-RP2. [Download and copy the .UF2 file](https://circuitpython.org/board/seeeduino_xiao_rp2040/) to the drive and it will reboot into CircuitPython.
If you need to reinstall for any reason, short the 'BOOT' test pads while resetting the RP2040 and it will go back to the booloader mode.
## Installing The Attribution Game
Once CircuitPython is installed, when the badge is plugged in it will show both a serial port and a drive labeled CIRCUITPY. Copy the entire contents of /software/ in this repository to that drive. the bage will reboot and run the code.
## Provisioning the game data
The /software/ directory contains some text files with data specific to the game. These will be copied along with the rest of the code:
- card_names includes all the strings of all the cards in the deck including
- cards starts blank and only contains the encrypted cards you collected by trading
- contacts starts blank and will contain the contact info of people you traded with
- key contains the game public key which can be used to authenticate the encrypted cards you recieve. This is generated by the controller and is included here for convenience
In addition, each badge needs a unique my_cards file that contains the encrypted version of one card for each round of the game. This is the card that is traded when a trade happens. This file is different for every badge. These are generated by the game controller. These need to be copied individually to different badges. There should totally be a script to do this.

## Hardware
/hardware/ contains the kicad board design files and full details about design and manufacturing. The hardware on the badge includes:
- Raspberry Pi 2040, derived from the seeed xiao 2040
- 16MB spi flash for code and files
- 128x64 OLED dislay with SH1106 controller over I2C
- IRDA PHY used directly on uart.
- 5-way d-pad for input
- 10 neopixel LEDs
- AAA battery plus boost voltage converter
- USB-C connector plus vreg for usb power
- power switch to switch between USB and Battery power
- testpoints for reset, boot, and swd

## Software
- /software/ contains the code on the badge
- /prototype/ contains prototypes and experiments used to develop all the features used in /software
- /controller/ contains the code that runs on the special controller badge that will manage the game

### Architecture
Most functions are wrapped inside classes with the priority to make the top level code more clean and readable versus sticking to a clean object model.

All functions should be non-blocking and quick to make sure the UI doesn't get frozen and button presses don't get missed. This means stuff like checking for enough uart valid data before reading it, and scheduling timed actions based on timestamps instead of sleep() calls

### Dependencies
- core circuitpython libraries: time,board,busio,pulseio,digitalio,displayio,terminalio
- additional adafruit libraries in /software/lib/: debouncer, ticks, displayio_ssh1106, imageload, display_text

### Support modules
- Fake_IRDA.py wraps the UART interface, handles enabling/disabling the IRDA enable pin, and stuffing/unstuffing the bytes that are transmitted to work with the IRDA phy in the nonstandard way we use it
- Five_Way_Dpad.py wraps the dpad with the Adafruit Debouncer including all setup and a few helper functions for checking all buttons at once. The non-blocking update() function needs to be run periodically to capture all button presses.
- sh1106_ui.py wraps the I2C display interface, handles the overall display view, and creates a separate group for each of the navigation pages. The non-blocking show() function should be called periodically to make sure the correct view is displayed and to manage the transition animations
- tbd.py wraps the functionality of the pages. The class handles initialization, managing the display view, underlying data and operations. Most of this is handled in a non-blocking update() function that returns the next state

## Screen

https://www.arduino.cc/reference/en/libraries/oled-ssd1306-sh1106/
https://docs.circuitpython.org/projects/displayio_sh1106/en/latest/api.html

Driven by: https://docs.circuitpython.org/en/latest/shared-bindings/displayio/


TRADE --------------------------------------

 ^        ^

HOME -> CARDS -> SETTINGS -> CONTACTS -> (ABOUT) -> HOME


