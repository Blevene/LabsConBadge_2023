from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio
import random

BLACK=0x000000
WHITE=0xFFFFFF

#this class manages the home display and navigation
#it also presents the new user process when no name is defined
class home:
    #store all the strings to display in a list
    currentstring=0
    strings=[
            "< - > change view\n^ trade | v sleep\nPress for more",
            "Thank you sponsors:\n   LutaSecurity, \n     Stairwell\n",
            "Thank you sponsors:\n Binarly, Aesir,\nGreyNoise, Canary\n",
            "Thank you sponsors:\nThe Vertex Project,\n  Vector 35\n",
            "Thank you sponsors:\n  Cisco Talos,\n   BugCrowd\n",
            "Thank you sponsors:\n  The Alperovitch\n    Institute\n",
            "Thank you sponsors:\nHiddenLayer, Nuand,\n Framework\n",
            " Thank you coders:\n   @silascutler\n    @psifertex\n"
            ]

    def __init__(self, group, dpad):
        self.group=group
        self.dpad=dpad

        #put the title text in black on the white bar
        self.header=label.Label(terminalio.FONT,text="LABScon 2023", color=BLACK, x=24, y=8)
        self.group.append(self.header)
        #put the content in white on the black text area
        self.contents=label.Label(terminalio.FONT,text=self.strings[0], scale=1, color=WHITE, x=8, y=24)
        self.contents.hidden=False
        self.group.append(self.contents)

        #get the username from file. This duplicates the work done by game.read_name()
        #but i'd rather add file i/o here than add display management there
        try:
            with open("data/myname.txt",'r') as file:
                name=file.readline().rstrip()
        except OSError as e:
            print(e)
            name=""

        #if there's no file or it's blank, give some instructions and ask for a name
        if name=="":
            self.showandwait("        The\n    Attribution\n       Game!      v")
            self.showandwait("Meet people & trade\n clues to attribute \n the attack       v")
            self.showandwait("You don't have\n a handle yet!\n                  v")
            self.showandwait("Your handle \nwill be shared with\n people you meet  v")
            name=self.showandprompty(" ^v to choose chars\n Press to save\n{}")
            self.showandwait("welcome\n to the game   v\n"+name+"!")
            self.showandwait("press '^' & point @\n another to trade \n contact & clues! v")
            self.showandwait("press '<' to get to\n settings and a list\n of alibis        v")
            self.showandwait("press '>' to get to\n your clue collection\n                  v")
            self.showandwait("Collect enough clues\n to figure out\n what happend     v")
            self.showandwait("\n     Have fun!\n                  v")
            self.contents.text=self.strings[0]

    #show a string and wait for a keypress
    def showandwait(self,mystring):
        self.contents.text=mystring
        self.dpad.update()
        while not self.dpad.d.fell:
            self.dpad.update()

    #show a string and handle text input
    def showandprompty(self,mystring):
        self.dpad.update()

        playername = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", ]             # ## ZGllIGxhYXN0ZSBzdHVra2llIHZhbiAnbiBsZWdrYWFydCBpcyBiby1hYW4gZGllIFZyeWRhZ29nZ2VuZHN0YXAu
        crange = "abcdefghijklmnopqrstuvwxyz.@!"
        cindex = 0
        nindex = 0
        playername[nindex] = crange[cindex]
        self.contents.text=mystring.format("".join(playername))
        while True:
            self.dpad.update()
            if self.dpad.u.fell:
                #if they press up, set the current char to the previous one in the list and update
                cindex=(cindex-1)%len(crange)
                playername[nindex] = crange[cindex]
                self.contents.text=mystring.format("".join(playername))
            elif self.dpad.d.fell:
                #if they press down, set the current char to the next one in the list and update
                cindex=(cindex+1)%len(crange)
                playername[nindex] = crange[cindex]
                self.contents.text=mystring.format("".join(playername))
            elif self.dpad.l.fell:
                #l moves to the previous char
                if nindex >= 0:
                    nindex -= 1
                else:
                    nindex = 0
            elif self.dpad.r.fell:
                #r moes to the next char
                if nindex == len(playername)-1:
                    nindex = 0
                else:
                    nindex += 1
            elif self.dpad.x.fell:
                #x means we're done. Save file and resume.
                print("Saving name")
                try:
                    with open("data/myname.txt",'w') as file:
                        file.write("".join(playername))
                except OSError as e:
                    print(e)
                return "".join(playername)

    def update(self):
        #show contents, process keypresses
        self.contents.hidden=False
        if self.dpad.u.fell:
            return "trade"
        if self.dpad.d.fell:
            self.contents.hidden=True
            return "sleep"
        if self.dpad.l.fell:
            self.contents.hidden=True
            return "alibis"
        if self.dpad.r.fell:
            self.contents.hidden=True
            return "clues"
        if self.dpad.x.fell:
            #x will cycle through the list of strings
            self.currentstring=(self.currentstring+1)%(len(self.strings))
            print(self.strings[self.currentstring])
            self.contents.text=self.strings[self.currentstring]
        return "home"
