'''
Labscon 2023 Badge Code

Key things:
1) An empty file called my_clue and a file containing all individual clues beyond the 4 winning ones called clues_collection 
    must be created in the root of the storage drive (same place as boot.py and main.py)
2) We need to have a reciever badge or device of some sort to recieve, decode, and validate our answers
3) We will need to seed each badge with a third file, clue_set, this will be used to compare incoming rx against our generated clues
   the goal is to eliminate all but 4 clues, aka our answer!

'''

import board
import digitalio
import busio
import adafruit_ssd1306
import time
import pulseio

#------------------------------------
# Global Variables and Init Stuff   |
#------------------------------------

# iInitialize the display
#i2c = busio.I2C(board.SCL, board.SDA)
i2c = busio.I2C(board.D5, board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Map the 5 way switch to pins
up_button = digitalio.DigitalInOut(board.D1)
up_button.direction = digitalio.Direction.INPUT
up_button.pull = digitalio.Pull.UP

down_button = digitalio.DigitalInOut(board.D2)
down_button.direction = digitalio.Direction.INPUT
down_button.pull = digitalio.Pull.UP

left_button = digitalio.DigitalInOut(board.D10)
left_button.direction = digitalio.Direction.INPUT
left_button.pull = digitalio.Pull.UP

right_button = digitalio.DigitalInOut(board.D9)
right_button.direction = digitalio.Direction.INPUT
right_button.pull = digitalio.Pull.UP

select_button = digitalio.DigitalInOut(board.D3)
select_button.direction = digitalio.Direction.INPUT
select_button.pull = digitalio.Pull.UP

# Map a shutdown button used to control IRDA power on/off
shutdown_button = digitalio.DigitalInOut(board.D8)
shutdown_button.direction = digitalio.Direction.INPUT
shutdown_button.pull = digitalio.Pull.UP

# Initilize IR Pins, note: the library used will *probably* change
ir_tx = pulseio.PulseOut(board.D6, frequency=38000, duty_cycle=2 ** 15)
ir_rx = pulseio.PulseIn(board.D7, maxlen=120, idle_state=True)

# We need to introduce a DEBOUNCE delay, otherwise the buttons will read inputs REALLY quickly.
DEBOUNCE_TIME = 0.2  # 200 milliseconds, adjust as needed

# main menu 
main_menu = ["Send", "Receive", "Show My Answer", "Show All Clues", "Send Answer", "Clear Answers"]

#when the user is creating their answer key this list will store it
selected_clues = []

# By default, we start in the main menu
menu = main_menu
is_in_main_menu = True

# The position we are highlighting in our current menu
current_position = 0

#---------------------------------------
# Functions tthat we frequently call   |
#--------------------------------------
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

#Thanks ChatGPT, we can use this function to read all recieved clues into a list
def read_clues_collection(filename):
    lines = []
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]
    except OSError:
        print("Error reading from file:", filename)
    return lines

# We'll call this function when we recieve a new clue from ir_recieve
def append_to_clues_collection(filename, text):
    try:
        with open(filename, 'a') as file:  # 'a' stands for append mode
            file.write(text + "\n")  # add a newline after the text
    except OSError:
        print("Error writing to file:", filename)

# Placeholder to encode our clue and translate it to a form that can be used for IRDA
# Call this with my_clue to prep our local clue for tx
# Call this with selected_clues to prep the answer list for tx
def encode(clue):

    return

# Placeholder to decode our clue after we recieve it
def decode(clue):
    # Do the Encode
    return

# Placeholder for transmission
def ir_transmit(clue):
    #Do the Transmit

    return

#Placeholder for recieve
def ir_recieve():
    #Do the Recieve
    rx_clue = #Raw Buffer from IRDA
    decoded_rx_clue = decode(rx_clue)
    append_to_clues_collection("/collected_clues", decoded_rx_clue)

    return 

# Send our answer as an encoded list, we need to have a reciever badge or device of some sort to recieve, decode, and validate
def send_answer(list_of_clues):
    sorted_answer = list_of_clues.sort()
    encoded_answer = encode(sorted_answer)
    ir_transmit(encoded_answer)
    

def check_clue_store(clue):
    clues_collection = read_clues_collection("/clues_collection")
    check_string = clue
    if check_string in clues_collection:
        print("Clue is not part of winning combo!") #This is just a debug thing
        # Remove the string from the underlying file so the clue is no longer there
    else:
        pass

# Clues Menu
# on the local filesystem of the badge, there will be a "collected_clues" file which we expect to contain one clue per line
# clues_menu = ["1", "2", "3", "4", "5"]
clues_menu = read_clues_collection("/collected_clues")

# Lets setup our local clue that we'll send
my_clue = read_clues_collection("/my_clue")
my_clue = my_clue[0]

#------------------------------------
# Main Loop                         |
#------------------------------------

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
            elif menu[current_position] == "Send":
                print("SENDING") #comment out
                #ir_transmit(my_clue)
            elif menu[current_position] == "Recieve":
                print("RECIEVING") #comment out 
                #ir_recieve()
            elif menu[current_position] == "Send Answer":
                print("SENDING ANSWER") #Comment Out
                #send_answer(selected_clues)
            elif menu[current_position] == "Show My Answer":
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