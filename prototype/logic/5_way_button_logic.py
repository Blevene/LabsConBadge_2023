'''
Template code for handling a 5-way button
Pins per Fritzing Diagram.
'''
import board
import digitalio
import time

# set up buttons
up_button = digitalio.DigitalInOut(board.D11)
up_button.direction = digitalio.Direction.INPUT
up_button.pull = digitalio.Pull.UP

down_button = digitalio.DigitalInOut(board.D5)
down_button.direction = digitalio.Direction.INPUT
down_button.pull = digitalio.Pull.UP

left_button = digitalio.DigitalInOut(board.D9)
left_button.direction = digitalio.Direction.INPUT
left_button.pull = digitalio.Pull.UP

right_button = digitalio.DigitalInOut(board.D10)
right_button.direction = digitalio.Direction.INPUT
right_button.pull = digitalio.Pull.UP

select_button = digitalio.DigitalInOut(board.D6)
select_button.direction = digitalio.Direction.INPUT
select_button.pull = digitalio.Pull.UP

# set up LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

while True:
    # check button states
    if not up_button.value:  # up button is pressed
        led.value = True
        time.sleep(0.1)  # debounce delay
    elif not down_button.value:  # down button is pressed
        led.value = False
        time.sleep(0.1)  # debounce delay
    elif not left_button.value:  # left button is pressed
        led.value = not led.value  # toggle LED
        time.sleep(0.1)  # debounce delay
    elif not right_button.value:  # right button is pressed
        led.value = not led.value  # toggle LED
        time.sleep(0.1) # debounce delay
    elif not select_button.value: # select button is pressed
        led.value = not led.value  # toggle LED
        time.sleep(0.1) # debounce delay
