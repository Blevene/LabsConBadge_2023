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
    retries=0

    def __init__(self, group, dpad, game):
        self.group=group
        self.dpad=dpad
        self.ir=FakeIRDA()
        self.game=game

        self.group.append(box(112,56,WHITE,0,0))
        self.group.append(box(110,54,BLACK,1,16))

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
            #print("starting trade",self.state,self.count,self.timeout)
            self.ir.enablePHY()
            
            # process tx/rx
            # if state is tx, transmit and increment count
            if self.state == "transmitting":
                self.count += 1
                print("transmitting", self.count)
                self.details.text="transmitting"
                self.ir.writebytes(bytearray(self.game.myclue+","+self.game.myname))
                self.count=5
                self.state="receiving"
                self.timeout=ticks_ms()+5000

            # if state is rx, recieve until valid clue recieved or timeout
            elif self.state == "receiving":
                if self.ir.ready(1):
                    rxval=self.ir.readbytes()
                    print(rxval)
                    if rxval.find(',') != -1: 
                        self.rxclue,self.rxname=rxval.split(',')
                        print(self.rxclue,self.rxname)
                        if self.rxclue is not None and self.rxname is not None and self.game.check_clue(self.rxclue,self.rxname):
                            print("recieved")
                            self.count=0
                            self.state="responding"
                            #time.sleep(.5)
                elif ticks_ms()> self.timeout:
                    print("timeout")
                    self.state="timeout"
                else:
                    self.details.text="receiving"+str((self.timeout - ticks_ms()) // 1000)
                    print("nothing received yet",self.timeout,ticks_ms())
                    #time.sleep(.5)
            # if state is respond, tx 1 time
            elif self.state == "responding":
                self.count += 1
                print("transmitting", self.count)
                self.details.text="responding"
                self.ir.writebytes(bytearray(self.game.myclue+","+self.game.myname))
                self.count=0
                self.state="success"
            elif self.state =="success":
                print(self.rxname,"\nsaid it wasn't\n",self.rxclue)
                self.details.text=self.rxname+" \nsaid it wasn't\n"+self.rxclue
            else:
                print("timeout", self.count)
                self.details.text="responding"
                
            # process keypresses
            self.dpad.update()
            # if down is pressed, return to where we came from
            #todo: l for alibi details, r for clue details
            if self.dpad.d.fell:
                self.ir.disablePHY()
                self.state="transmitting"
                self.count=0
                self.group.hidden=True
                return 0
            # if u is pressed, restart the trade process
            elif self.dpad.u.fell: 
                self.state="transmitting"
                self.count=0
