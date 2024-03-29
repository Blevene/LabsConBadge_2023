import board
import busio
import digitalio

#todo - add error checking

class FakeIRDA:
    def __init__(self,uart=busio.UART(board.TX, board.RX, baudrate=350000, receiver_buffer_size=64),sd=board.D8):
        self.uart=uart
        #self.uart.baudrate=350000
        self.shutdown=digitalio.DigitalInOut(sd)
        self.shutdown.switch_to_output()
        self.shutdown.value=1
        self.possiblymisaligned=False

    # reads two bytes from uart and repacks it into one byte of data and returns it
    def readbyte(self):
        #self.enablePHY()
        rxval=self.uart.read(2)
        if (rxval is not None) and (len(rxval)==2):
            #print(rxval,rxval[0] & (rxval[1]>>1|128))
            #test for misaligned lead-in of CRs by decoding with [1] and [0] swapped
            if (rxval[1] & (rxval[0]>>1|128))==13:
                if self.possiblymisaligned==False:
                    #if this is the first time, keep track
                    self.possiblymisaligned=True
                    print("possiblymisaligned")
                else:
                    #if this is the second time - shift by one byte
                    rxval=self.uart.read(1)
                    rxval=self.uart.read(2)
            else:
                #otherwise, we're probably fine
                self.possiblymisaligned=False
            return chr(rxval[0] & (rxval[1]>>1|128))

    # calls readbyte N times, reading 2*N bytes
    def readbytes(self,count=None):
        bytesread=""
        if count == None:
            byte = self.readbyte()
            while byte is not None:
                bytesread+=byte
                #print("read",byte,"one more byte?")
                byte = self.readbyte()
                pass
            return bytesread
        for i in range(count):
            bytesread.append(self.readbyte())
        return bytesread

    # takes one byte, expands it to two bytes interleved with '1's and transmits both
    def writebyte(self,txval):
        #self.enablePHY()
        self.uart.write(bytes([txval|85,(((txval<<1)|85)%256)]))
        #print(bytes([txval|85,(((txval<<1)|85)%256)]),txval)
        self.uart.reset_input_buffer()

    # calls writebyte N times, writing 2N bytes total
    def writebytes(self,byteswrite):
        for i in byteswrite:
            self.writebyte(i)

    # set shutdown pin to 0 to wake up phy
    def enablePHY(self):
        self.shutdown.value=0

    #set shutdown pint to 1 to shut down phy and save power
    def disablePHY(self):
        self.shutdown.value=1

    #return true if uart has enough bytes waiting.
    def ready(self,numbytes=1):
        return self.uart.in_waiting >= (numbytes*2)

