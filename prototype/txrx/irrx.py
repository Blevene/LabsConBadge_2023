import board
import digitalio
import busio
import time
import pulseio
import displayio
import adafruit_displayio_sh1106
displayio.release_displays()
i2c=board.I2C()
display_bus=displayio.I2CDisplay(i2c,device_address=60)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=130, height=64)


# sd=0 enables irda phy
sd = digitalio.DigitalInOut(board.D8)
sd.switch_to_output()
sd.value=0

uart = board.UART()
uart.baudrate=350000
while True:
    if uart.in_waiting > 1:
        rxval=uart.read(2)
        print("rx",rxval[0] & (rxval[1]>>1|128),"[",rxval[0],",",rxval[1],"]")
        #print("big","{:08b}".format(int.from_bytes(uart.read(1),"big")))
        #print(int.from_bytes(uart.read(1)))

while True:
    if uart.in_waiting > 0:
        rxval=uart.read(1)
        print(rxval[0])#,rxval[0]&85,(rxval[0]>>1)&85)
    
