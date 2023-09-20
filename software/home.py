from adafruit_display_text import label
from sh1106_ui import box
import terminalio
import displayio
import random

BLACK=0x000000
WHITE=0xFFFFFF

nList = ["Phishing",  "Malware",  "Ransomware",  "Spoofing",  "Encryption",  "Adware",  "0day",  "hashes",  "Bot",  "Botnets",  "DDoS",  "Firewall",  "Payload",  "White hat",  "Rootkit",  "Worm",  "Cloaking",  "Eavesdropping",  "SQL",  "XSS",  "Backdoor",  "Doxing",  "Keystroke",  "Botnet",  "Blacklisting",  "Attack",  "Authentication",  "Backup",  "Blackhat",  "Code injection",  "Exploit",  "Patch",  "Spam",  "URL injection",  "CSRF",  "APT",  "Jags",  "Ajax",  "Security Team",  "Alibaba",  "Admin338",  "1.php",  "Arid", "Viper",  "FANCY",  "PANDA",  "SPIDER",  "BEAR",  "CHOLLIMA",  "KITTEN",  "EAGLE",  "QRCode",  "Berserk",  "VOODOO",  "SANDW0RM",  "Bluenoroff",  "Group",  "Team",  "RedBull",  "Twitter",  "Agency"]

class home:
    currentstring=0
    #todo: sponsor images

    strings=[
            "< - > change view\n^ - v to trade\nPress for more",
            "Thank you sponsors:\n   LutaSecurity, \n     Stairwell\n",
            "Thank you sponsors:\n Binarly, Aesir,\nGreyNoise, Canary\n",
            "Thank you sponsors:\nThe Vertex Project,\n  Vector 35\n",
            "Thank you sponsors:\n  Cisco Talos,\n   BugCrowd\n",
            "Thank you sponsors:\n  The Alperovitch\n    Institute\n",    
            "Thank you sponsors:\nHiddenLayer, Nuand,\n Framework\n",
            ]

    def __init__(self, group, dpad):
        self.group=group
        self.dpad=dpad

        self.header=label.Label(terminalio.FONT,text="LABScon 2023", color=BLACK, x=24, y=8)
        self.group.append(self.header)
        self.contents=label.Label(terminalio.FONT,text=self.strings[0], scale=1, color=WHITE, x=8, y=24)
        self.contents.hidden=False
        self.group.append(self.contents)

        try:
            with open("data/myname.txt",'r') as file:
                name=file.readline().rstrip()
        except OSError as e:
            print(e)
            name=""
        
        if name=="":
            self.showandwait("        The\n    Attribution\n       Game!      v")
            self.showandwait("Meet people & trade\n clues to attribute \n the attack       v")
            self.showandwait("You don't have\n a handle yet!\n                  v")
            self.showandwait("Your handle \nwill be shared with\n people you meet  v")
            name=self.showandprompty(" ^v to choose chars\n Press to save\n{}")
            self.showandwait("welcome\n to the game\n"+name+"!")
            self.showandwait("press '^' & point @\n another to trade \n contact & clues! v")
            self.showandwait("The combo w/o alibi\n is the solution!\n                  v")
            self.showandwait("\n     Have fun!\n                  v")

    def showandwait(self,mystring):
        self.contents.text=mystring
        self.dpad.update()
        while not self.dpad.d.fell:
            self.dpad.update()

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
            #print(self.dpad.r.fell)
            #print(self.dpad.l.fell)

            if self.dpad.u.fell: 
                cindex=(cindex-1)%len(crange)
                playername[nindex] = crange[cindex]
                self.contents.text=mystring.format("".join(playername))
            elif self.dpad.d.fell:
                cindex=(cindex+1)%len(crange)
                playername[nindex] = crange[cindex]
                self.contents.text=mystring.format("".join(playername))
            elif self.dpad.l.fell:
                if nindex >= 0: 
                    nindex -= 1
                else:
                    nindex = 0
            elif self.dpad.r.fell:
                if nindex == len(playername)-1:
                    nindex = 0
                else:
                    nindex += 1
            elif self.dpad.x.fell: 
                print("Saving name")
                try:
                    with open("data/myname.txt",'w') as file:
                        file.write("".join(playername))
                except OSError as e:
                    print(e)
                return "".join(playername)

    def update(self):
        self.contents.hidden=False
        #todo: make display auto-advance
        #todo: don't sleep till done?
        if self.dpad.u.fell: 
            self.contents.hidden=True
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
            self.currentstring=(self.currentstring+1)%(len(self.strings))
            print(self.strings[self.currentstring])
            self.contents.text=self.strings[self.currentstring]
        return "home"
