import board
import digitalio
import busio
import time
import pulseio
from five_way_pad import FiveWayPad
from fake_irda import FakeIRDA
import displayio
import adafruit_imageload
import adafruit_displayio_sh1106
from sh1106_ui import sh1106ui
import terminalio
from adafruit_display_text import label
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

BLACK=0x000000
WHITE=0xFFFFFF

display=sh1106ui()
dpad=FiveWayPad()

class home:
    def __init__(self, group, dpad):
        self.dpad=dpad
        self.group=group

        self.header=label.Label(terminalio.FONT,text="home", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        self.details=displayio.Group()
        self.details.hidden=True
        self.group.append(self.details)

    def update(self):
        if dpad.u.fell: return "trade"
        if dpad.d.fell: return "sleep"
        if dpad.l.fell: return "contacts"
        if dpad.r.fell: return "cards"
        if dpad.x.fell: self.details.hidden=not self.details.hidden
        return "home"

class cards:
    def __init__(self, group, dpad):
        self.dpad=dpad
        self.group=group

        self.header=label.Label(terminalio.FONT,text="cards", color=BLACK, x=8, y=8)
        self.group.append(self.header)

        card_sheet, palette = adafruit_imageload.load("assets/cards.bmp",bitmap=displayio.Bitmap, palette=displayio.Palette)
        self.card_grid = displayio.TileGrid(card_sheet, pixel_shader=palette,
            width=11, height=3,
            tile_width=12, tile_height=16)
        card_group=displayio.Group()
        card_group.y=15
        card_group.append(self.card_grid)
        self.group.append(card_group)

        self.details=displayio.Group()
        self.details.hidden=True
        self.details.x=16
        self.details.y=8
        self.group.append(self.details)

        self.details.append(display.box(98,50,WHITE,0,0))
        self.details.append(display.box(96,48,BLACK,1,1))

        self.det=label.Label(terminalio.FONT,text="details", color=WHITE, x=4, y=8)
        self.details.append(self.det)

        for i in range(3):
            self.card_grid[i,0]=1
        for i in range(5):
            self.card_grid[i,1]=3
        for i in range(4):
            self.card_grid[i,2]=5
        self.x=2
        self.y=2

    def update(self):
        self.card_grid[self.x,self.y]=self.y*2+1
        if self.dpad.u.fell:
            if self.y==0: return "trade"
            self.y -=1
        if self.dpad.d.fell:
            if self.y==2: return "sleep"
            self.y +=1
        if self.dpad.l.fell:
            if self.x==0: return "home"
            self.x -=1
        if self.dpad.r.fell:
            #todo change this to max # cards in the row
            if self.x==2: return "settings"
            self.x+=1
        if dpad.x.fell: self.details.hidden=not self.details.hidden
        self.card_grid[self.x,self.y]=self.y*2+2
        self.det.text="details of card\n at [" + str(self.x) + "," + str(self.y) + "]"
        return "cards"

class contacts:
    def __init__(self, group, dpad):
        self.dpad=dpad
        self.group=group
        self.header=label.Label(terminalio.FONT,text="contacts", color=BLACK, x=8, y=8)
        self.group.append(self.header)
        self.details=displayio.Group()
        self.details.hidden=True
        self.group.append(self.details)

        self.contactlist=["@securelyfitz","@blevene","@oscontext","@4","@5","@6"]
        self.x=0
        self.y=0

    def update(self):
        if self.dpad.u.fell:
            if self.x==0: return "trade"
            self.x -=1
        if self.dpad.d.fell:
            if self.x==0: return "sleep"
            self.x +=1
        if self.dpad.l.fell:
            if self.y==0: return "settings"
            self.y -=1
        if self.dpad.r.fell:
            if self.y==0: return "home"
            self.y+=1
        if self.dpad.x.fell: self.display.details.hidden=not self.display.details.hidden
        return "contacts"

class settings:
    def __init__(self, group, dpad):
        self.dpad=dpad
        self.group=group
        self.header=label.Label(terminalio.FONT,text="settings", color=BLACK, x=8, y=8)
        self.group.append(self.header)
        self.details=displayio.Group()
        self.details.hidden=True
        self.group.append(self.details)

    def update(self):
        if dpad.u.fell: return "trade"
        if dpad.d.fell: return "sleep"
        if dpad.l.fell: return "cards"
        if dpad.r.fell: return "contacts"
        if dpad.x.fell: display.details.hidden=not display.details.hidden
        return "settings"

class trade:
    state="transmitting"
    count=0
    timeout=5
    retries=3
    mycard=[13]

    def __init__(self, group, dpad):
        self.dpad=dpad
        self.group=group
        self.ir=FakeIRDA()
        
        self.group.append(display.box(96,48,WHITE,0,0))
        self.group.append(display.box(94,31,BLACK,1,16))
        
        self.header=label.Label(terminalio.FONT,text="trade", color=BLACK, x=24, y=8)
        self.group.append(self.header)
        
        self.details=label.Label(terminalio.FONT,text="transmitting", color=WHITE, x=12, y=32)
        self.group.append(self.details)

    def update(self):
        #show trade page
        self.group.y=8

        while True:
            #print("starting trade",self.state,self.count,self.timeout)

            # process tx/rx
            # if state is tx, transmit and increment count
            if self.state == "transmitting":
                #todo: perhaps add a 100ms delay between each tx?
                self.count += 1
                print("transmitting", self.count)
                self.ir.writebytes(self.mycard)
                time.sleep(.2)
                #afer transmitting a few times, prepare to recieve
                if self.count > self.retries:
                    self.count=5
                    self.state="receiving"
                    self.ir.uart.reset_input_buffer()
                    self.timeout=ticks_ms()+5000

            # if state is rx, recieve until valid card recieved or timeout
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
                self.ir.writebytes(self.mycard)
                time.sleep(.2)
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
            dpad.update()
            # if down is pressed, return to where we came from
             #todo: l for contact details, r for card details
            if dpad.d.fell:
                self.state="transmitting"
                self.count=0
                self.group.y=-64
                return 0
            # if u is pressed, restart the trade process
            elif dpad.u.fell: 
                self.state="transmitting"
                self.count=0

class sleep:
    def __init__(self, display, dpad):
        self.dpad=dpad
        self.display=display

    def update(self):
        #self.display.header.text="sleep"
        if dpad.x.fell:
            display.maingroup.hidden=False
            return 0 # will return to last normal page
        elif dpad.u.fell:
            display.maingroup.hidden=False
            return "trade"
        display.maingroup.hidden=True
        return "sleep"

homepage=home(display.homegroup,dpad)
cardspage=cards(display.cardsgroup,dpad)
settingspage=settings(display.settingsgroup,dpad)
contactspage=contacts(display.contactsgroup,dpad)
tradepage=trade(display.tradegroup,dpad)
sleeppage=sleep(display,dpad)

page="sleep"
lastpage="home"

while True:
    #scan inputs
    #print("update loop:",page)
    #time.sleep(1)
    dpad.update()
    display.show(page)
    #go to sleep if timeout
    if dpad.duration()>10 and page != "trade": page=sleeppage.update()
    #if a button is pressed, handle it
    elif not dpad.pressed():
    #print("sleep")
        time.sleep(0.01)
    elif page == "home":
        #display.pagegroup.x=-260
        lastpage=page
        page=homepage.update()
    elif page == "settings":
        #display.pagegroup.x=0
        lastpage=page
        page=settingspage.update()
    elif page == "contacts":
        #display.pagegroup.x=-130
        lastpage=page
        page=contactspage.update()
    elif page == "cards":
        #display.pagegroup.x=-390
        lastpage=page
        page=cardspage.update()
    elif page == "trade":
        print("update trade")
        page=tradepage.update()
    elif page == "sleep": page=sleeppage.update()
    else: page=lastpage
