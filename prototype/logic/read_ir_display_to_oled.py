'''
Example code to recieve IR input and print it to an OLED display.
It will populate a string of the transmitted value so we need to decode "value"
'''
import board
import pulseio
import digitalio
import time
import adafruit_ssd1306

# create pulsein object to read IR pulses
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)

# set up OLED display
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
oled.fill(0)  # clear display
oled.show()

while True:
    # read incoming message
    pulses = pulsein.read(10)  # read up to 10 pulses

    if pulses:  # if a message was received
        # decode message
        value = pulseio.decode_bits_to_bytes(pulses)

        # display value on OLED
        oled.fill(0)  # clear display
        oled.text('Value:', 0, 0)
        oled.text(str(value), 0, 10)
        oled.show()
