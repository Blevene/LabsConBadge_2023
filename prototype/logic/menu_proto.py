import board
import digitalio
import busio
import adafruit_ssd1306
import time


#------------------------------------------------------
# Global Variables and Init Stuff
#------------------------------------------------------

# iInitialize the display
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


# Map the 5 way switch to pins
up_button = digitalio.DigitalInOut(board.D0)
up_button.direction = digitalio.Direction.INPUT
up_button.pull = digitalio.Pull.UP

down_button = digitalio.DigitalInOut(board.D2)
down_button.direction = digitalio.Direction.INPUT
down_button.pull = digitalio.Pull.UP

left_button = digitalio.DigitalInOut(board.D1)
left_button.direction = digitalio.Direction.INPUT
left_button.pull = digitalio.Pull.UP

right_button = digitalio.DigitalInOut(board.D9)
right_button.direction = digitalio.Direction.INPUT
right_button.pull = digitalio.Pull.UP

select_button = digitalio.DigitalInOut(board.D7)
select_button.direction = digitalio.Direction.INPUT
select_button.pull = digitalio.Pull.UP

# We need to introduce a DEBOUNCE delay, otherwise the buttons will read inputs REALLY quickly.
DEBOUNCE_TIME = 0.2  # 200 milliseconds, adjust as needed

# main menu and clues menu
# Note: clues menu will have to read from the recieved clues file in flash storage
main_menu = ["Send", "Receive", "Show All Clues", "Send Answer", "Clear Answers"]
clues_menu = ["1", "2", "3", "4", "5"]

#when the user is creating their answer key this list will store it
selected_clues = []

# By default, we start in the main menu
menu = main_menu
is_in_main_menu = True

# The position we are highlighting in our current menu
current_position = 0

#------------------------------------------------------
# Functions that we frequently call
#------------------------------------------------------
# Debounce function
def debounce(button):
    """Wait for the button to be released and then wait for DEBOUNCE_TIME"""
    while button.value:  # Wait for the button to be released
        time.sleep(0.01)  # Sleep for 10 milliseconds
    time.sleep(DEBOUNCE_TIME)  # Wait for the debounce period to expire

# Build and Display our Menu on the OLED
def draw():
    display.fill(0)
    for i, option in enumerate(menu):
        y = 10 + i*10
        if i == current_position:
            display.text('> ' + option, 0, y, 1)
        else:
            display.text('  ' + option, 0, y, 1)
    display.show()

# Main Loop
# Note: ADD DEBOUNCE, its Polling the Button presses WAY too quickly
while True:
    if not up_button.value:  # move up
        current_position = (current_position - 1) % len(menu)
        draw()
        debounce(up_button)
        

    elif not down_button.value:  # move down
        current_position = (current_position + 1) % len(menu)
        draw()
        debounce(down_button)

    elif not select_button.value:  # select
        if is_in_main_menu:
            if menu[current_position] == "Show All Clues":
                menu = clues_menu
                current_position = 0
                is_in_main_menu = False
            elif menu[current_position] == "Send Answer":
                # Print our selected clues to console
                print("Selected clues: ", selected_clues)
            elif menu[current_position] == "Clear Answers":
                selected_clues.clear()
                print("Answers cleared")
            else:
                print("Selected: ", menu[current_position])
        else:
            selected_clue = menu[current_position]
            if selected_clue not in selected_clues:
                selected_clues.append(selected_clue)
            print("Selected clue: ", selected_clue)


    elif not left_button.value:
        if not is_in_main_menu:
            menu = main_menu
            current_position = 0
            is_in_main_menu = True
        draw()
        debounce(left_button)
    
    elif not right_button.value:  # do nothing, here for future use
        pass
        debounce(right_button)