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
     for i in range(0x00,0xf):
     #for i in [0x00,0x55,0xaa,0xff]:
         #print("tx",i,"[",i|85,",",(((i<<1)|85)%256),"]")
         print(i,i|85,i<<1|85%256)
         uart.write(bytes([0,0]))
         for j in range (1): 
            #uart.write(bytes([i]))
            uart.write(bytes([i|85]))
            uart.write(bytes([i<<1|85]))
            #uart.write(bytes([i|85,(((i<<1)|85)%256)]))
         #print("tx:",i,"{:08b}".format(i),"rx:","1111""{:08b}".format(int.from_bytes(uart.read(1),"big")),"1111") # time consuming
         uart.reset_input_buffer()
         time.sleep(1)

