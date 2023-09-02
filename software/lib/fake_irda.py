import board
import digitalio

class FakeIRDA:
    def __init__(self,uart=board.UART(),sd=board.D8):
        self.uart=uart
        self.uart.baudrate=400000
        self.shutdown=digitalio.DigitalInOut(sd)
        self.shutdown.switch_to_output()
        self.shutdown.value=1

    # reads two bytes from uart and repacks it into one byte of data and returns it
    def readbyte(self):
        self.enablePHY()
        rxval=self.uart.read(2)
        if rxval is not None:
            return rxval[0] & (rxval[1]>>1|128)

    # calls readbyte N times, reading 2*N bytes
    def readbytes(self,count):
        bytesread=[]
        for i in range(count)
            bytesread.append(readbyte())
        return bytesread

    # takes one byte, expands it to two bytes interleved with '1's and transmits both
    def writebyte(self,txval):
        self.enablePHY()
        self.uart.write(bytes([txval|85,(((txval<<1)|85)%256)]))

    # calls writebyte N times, writing 2N bytes total
    def writebytes(self,byteswrite):
        for i in byteswrite
            writebyte(i)
        return bytesread

    # set shutdown pin to 0 to wake up phy 
    def enablePHY(self):
        self.shutdown.value=0

    #set shutdown pint to 1 to shut down phy and save power
    def disablePHY(self):
        self.shutdown.value=1

    #return true if uart has enough bytes waiting.
    def ready(self):
        return self.uart.in_waiting > 1

