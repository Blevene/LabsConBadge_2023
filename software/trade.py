import time
from adafruit_ticks import ticks_ms, ticks_add, ticks_less
from adafruit_display_text import label
from fake_irda import FakeIRDA
from sh1106_ui import box
import terminalio
import displayio
import binascii
import board
import busio

BLACK=0x000000
WHITE=0xFFFFFF

#this manages the trading of data with others. Unlike the other views,
#this one is blocking during RX (though this coul probabable be fixed).
#This class manages the crc check to ensure valid data is tx/rx, but 
#game.check_clue does the data structure validation and update
class trade:
    state="transmitting"
    timeout=0

    def __init__(self, group, dpad, game):
        self.group=group
        self.dpad=dpad
        self.ir=FakeIRDA()
        self.game=game

        #draw a box over the screen with black text on top and white below
        self.group.append(box(112,64,WHITE,0,0))
        self.group.append(box(110,47,BLACK,1,16))
        self.header=label.Label(terminalio.FONT,text="trade", color=BLACK, x=4, y=8)
        self.group.append(self.header)
        self.details=label.Label(terminalio.FONT,text="transmitting", color=WHITE, x=12, y=24)
        self.group.append(self.details)

        self.rxname=None
        self.rxclue=None

    def update(self):
        #show trade page
        self.group.hidden=False

        while True:
            #turn on the PHY to enable tx/rx
            self.ir.enablePHY()

            # Transmit state. Transmit the pre-calculated tx value
            if self.state == "transmitting":
                print("transmitting")
                self.details.text="transmitting..."
                self.ir.writebytes(self.game.mytxval)
                #tx complete; prepare to rx. Clear buffer and set timeout
                self.ir.uart.reset_input_buffer()
                self.state="receiving"
                self.timeout=ticks_ms()+30000

            # recieve state. listen until data recieved, then check it and proceed
            elif self.state == "receiving":
                if self.ir.ready(4):
                    #4 bytes are in the queue - enough to get started. Get data
                    rxval=self.ir.readbytes()
                    print(f"RX: {rxval}")
                    #if we have 3 csvs, parse them
                    #todo: get signature too
                    if rxval.count(',') == 2:
                        chksum, self.rxclue, self.rxname = rxval.split(',')
                        print(f"RX: {chksum}, {self.rxclue}, {self.rxname}")
                        #check crc is valid.
#                        if False or binascii.crc32(bytearray(str(self.rxclue) + "," + str(self.rxname))) != int(chksum, 16):
#                            print("[!] Invalid Checksum")
#                            self.state="error"
#                            self.details.text="receive error :(\n^ try again\nv cancel"
#                        elif self.rxclue is not None and self.rxname is not None and self.game.check_clue(self.rxclue, self.rxname):
                        #until crc is reliable, check that strings are not none
                        if self.rxclue is not None and self.rxname is not None and self.game.check_clue(self.rxclue, self.rxname):
                            #if the clue was valid, move to responding
                            print("recieved")
                            self.state="responding"
                        else:
                            #if clue was invali, we got an error
                            #maybe this should probably be retry since tx/rx is more robust now
                            print("recieve error")
                            self.state="error"
                            self.details.text="error try agian or\ncheck your game #\n^ again    v cancel"
                #go to timeout if we've been waiting too long
                elif ticks_ms()> self.timeout:
                    print("timeout")
                    self.state="timeout"
                    self.details.text="timeout :(\n^ try again\nv cancel"
                #otherwise, show a timeout countdown
                else:
                    self.details.text="receiving "+str((self.timeout - ticks_ms()) // 1000)
                    #print("nothing received yet",self.timeout,ticks_ms())

            #responding state. Send our clue one more time
            elif self.state == "responding":
                print("responding")
                self.details.text="responding"
                self.ir.writebytes(self.game.mytxval)
                #done responding. Go to success state
                self.state="success"
                print(self.rxname,"\nsaid it wasn't\n",self.rxclue)
                self.details.text="< "+self.rxname+" \nsaid it wasn't\n >"+self.rxclue

            #success, timeout, and error states don't have any followon action - just wait for buttons    

            # process keypresses
            self.dpad.update()
            # if down is pressed, return to where we came from
            retval=None
            if self.dpad.d.fell: retval=0            
            if self.state=="success" and self.dpad.l.fell: retval="alibis"
            if self.state=="success" and self.dpad.r.fell: retval="clues"
            if retval is not None:
                self.ir.disablePHY()
                self.state="transmitting"
                self.group.hidden=True
                return retval
            # if u is pressed, restart the trade process
            if self.dpad.u.fell:
                self.state="transmitting"
