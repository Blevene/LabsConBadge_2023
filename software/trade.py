import time
from adafruit_ticks import ticks_ms, ticks_add, ticks_less
from adafruit_display_text import label
from fake_irda import FakeIRDA
from sh1106_ui import box
import terminalio
import displayio

BLACK=0x000000
WHITE=0xFFFFFF


class trade:
    state="transmitting"
    count=0
    timeout=5
    retries=3
    myclue=[13]

    def __init__(self, group, dpad):
        self.group=group
        self.dpad=dpad
        self.ir=FakeIRDA()

        self.group.append(box(96,48,WHITE,0,0))
        self.group.append(box(94,31,BLACK,1,16))

        self.header=label.Label(terminalio.FONT,text="trade", color=BLACK, x=24, y=8)
        self.group.append(self.header)

        self.details=label.Label(terminalio.FONT,text="transmitting", color=WHITE, x=12, y=32)
        self.group.append(self.details)

    def update(self):
        #show trade page
        self.group.hidden=False

        while True:
            #print("starting trade",self.state,self.count,self.timeout)

            # process tx/rx
            # if state is tx, transmit and increment count
            if self.state == "transmitting":
                #todo: perhaps add a 100ms delay between each tx?
                self.count += 1
                print("transmitting", self.count)
                self.ir.writebytes(self.myclue)
                #time.sleep(.2)
                #afer transmitting a few times, prepare to recieve
                if self.count > self.retries:
                    self.count=5
                    self.state="receiving"
                    self.ir.uart.reset_input_buffer()
                    self.timeout=ticks_ms()+5000

            # if state is rx, recieve until valid clue recieved or timeout
            elif self.state == "receiving":
                if self.ir.ready(1):
                    rxval=self.ir.readbytes(1)
                    # if data valid:
                    # store data
                    print("recieved")
                    self.count=3
                    self.state="responding"
                    time.sleep(.5)
                elif ticks_ms()> self.timeout:
                    print("timeout")
                    self.state="timeout"
                else:
                    self.count=(self.timeout - ticks_ms()) // 1000
                    print("nothing receivd yet",self.timeout,ticks_ms())
                    time.sleep(.5)
            # else state is respond, tx 3 more times
            elif self.state == "responding":
                self.count += 1
                print("transmitting", self.count)
                self.ir.writebytes(self.myclue)
                #time.sleep(.2)
                #afer transmitting a few times, prepare to recieve
                if self.count > self.retries:
                    self.count=0
                    self.state="success"
            else: 
                #print(self.state)
                #self.header.text=self.state
                pass

            # process keypresses
            self.details.text=self.state+" "+str(self.count)
            self.dpad.update()
            # if down is pressed, return to where we came from
             #todo: l for alibi details, r for clue details
            if self.dpad.d.fell:
                self.state="transmitting"
                self.count=0
                self.group.hidden=True
                return 0
            # if u is pressed, restart the trade process
            elif self.dpad.u.fell: 
                self.state="transmitting"
                self.count=0
