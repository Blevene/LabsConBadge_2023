import board
import digitalio
import busio
import adafruit_ssd1306

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


# main menu and clues menu
# Note: clues menu will have to read from the recieved clues file in flash storage
main_menu = ["Send", "Receive", "Show All Clues", "Send Answer"]
clues_menu = ["1", "2", "3", "4", "5"]

# By default, we start in the main menu
menu = main_menu
is_in_main_menu = True

# The position we are highlighting in our current menu
current_position = 0

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
        

    elif not down_button.value:  # move down
        current_position = (current_position + 1) % len(menu)
        draw()

    elif not select_button.value:  # select
        if is_in_main_menu and menu[current_position] == "Show All Clues":
            menu = clues_menu
            current_position = 0
            is_in_main_menu = False
        # Do The Needful Based on the value of menu[current_position]
        #elif is_in_main_menu and menu[current_position] == "Send":
            #do the send thing
        #elif is_in_main_menu and menu[current_position] == "Recieve":
             #do the recieve thing
        #elif is_in_main_menu and menu[current_position] == "Send Answer":
            #send the guess
        else:
            print("Selected: ", menu[current_position])
            pass


    elif not left_button.value:
        if not is_in_main_menu:
            menu = main_menu
            current_position = 0
            is_in_main_menu = True
        draw()
    
    elif not right_button.value:  # do nothing, here for future use
        pass