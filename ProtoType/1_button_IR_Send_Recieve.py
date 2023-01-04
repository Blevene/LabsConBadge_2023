'''
Thanks ChatGPT, we need to change the Pins as none of the stuff is built into the board
'''
import board
import pulseio
import digitalio
import time

# create pulsein and pulseout objects to read and write IR pulses
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
pulseout = pulseio.PulseOut(board.IR_TX)

# set up button
button = digitalio.DigitalInOut(board.BUTTON)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# set up LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

while True:
    # wait for button press
    while not button.value:
        pass

    # blink LED while sending and receiving data
    while True:
        led.value = True
        pulseout.send(b'Hello')
        led.value = False
        time.sleep(0.002)  # blink LED every 2ms

        # read incoming message
        pulses = pulsein.read(10)  # read up to 10 pulses

        if pulses:  # if a message was received
            # decode message
            message = pulseio.decode_bits_to_bytes(pulses)
            print(message)
            break  # exit inner loop