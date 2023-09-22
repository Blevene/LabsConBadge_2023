import circuitpython_csv
import binascii

class gamedata:
    gamenum=0
    myclue=None
    myname=None
    mytxval=None
    newclue=None
    namefile="data/myname.txt"
    gamefile="data/game1.csv"
    alibifile="data/alibis.txt"

    threats=[]
    attacks=[]
    victims=[]
    cluecounts=[0,0,0]
    alibis=[]
    def __init__(self,gamenum=0):
        self.gamenum=gamenum
        self.read_name()
        self.read_alibis()
        self.gamefile="data/game"+str(gamenum)+".csv"
        self.read_clues()

    def check_clue(self,newclue,alibi):
        #print(newclue,alibi)
        if alibi not in self.alibis:
            self.alibis.append(alibi)
            self.write_alibis()
        else:
            print(f"Alibi {alibi} already known")

#        for clue in (self.threats+self.attacks+self.victims):
#            if clue[1] == newclue:
#                clue[3] = newclue
#                clue[4] = alibi
#                self.newclue=newclue
#                return newclue
        for j, cluetype in enumerate([self.threats,self.attacks,self.victims]):
            for i in range(self.cluecounts[j]):
                if cluetype[i][1]==newclue:
                    cluetype[i][3]=newclue
                    cluetype[i][4]=alibi
                    self.newclue=[i,j]
                    self.write_clues()
                    return newclue
        return False

    def read_name(self):
        #getname, if not, do oob?
        try:
            with open("data/myname.txt",'r') as file:
                self.myname=file.readline().rstrip()
                print("hello",self.myname)
        except OSError:
            print("Error reading name from data/myname.txt")
            self.myname="unknown"

    def wipe_name(self):
        self.myname=""
        self.write_name()

    def write_name(self):
        try:
            with open("data/myname.txt", 'w') as fhandle:
                fhandle.write(self.myname)
        except OSError:
            print("Error writing name file")
            return False
        return True

    def read_clues(self):
        try:
            with open(self.gamefile, 'r') as file:
                csv=circuitpython_csv.reader(file)
                self.threats=[]
                self.attacks=[]
                self.victims=[]
                for row in csv:
                    if row[0] == "T":self.threats.append(row)
                    elif row[0] == "A":self.attacks.append(row)
                    elif row[0] == "V":self.victims.append(row)
                    elif row[0] == "*":self.myclue=row[1]
            self.cluecounts=[len(self.threats),len(self.attacks),len(self.victims)]
            self.check_clue(self.myclue,self.myname)
            crc = hex(binascii.crc32(bytearray(str(self.myclue)+","+str(self.myname))))[2:]
            crs = bytearray([13,13,13,13,13,13,13,13])
            print(crc,self.myclue,self.myname)
            self.mytxval=crs+bytearray(",".join([crc,self.myclue,self.myname]))
            print(f"{self.mytxval}")
        except OSError:
            print("Error reading from file:", self.gamefile)

    def wipe_clues(self):
        for cluetype in [self.threats,self.attacks,self.victims]:
            for clue in cluetype:
                if clue!=self.myclue:
                    clue[3]=""
                    clue[4]=""
        self.newclue=-1
        self.check_clue(self.myclue,self.myname)
        self.write_clues()

    def write_clues(self):
        #should be called every time we add a clue?
        try:
            fhandle = open(self.gamefile, 'w')
            for cluetype in [self.threats,self.attacks,self.victims]:
                for clue in cluetype:
                    fhandle.write(",".join(clue))
                    fhandle.write("\n")
            fhandle.write("*,"+str(self.myclue))
            fhandle.close()
        except OSError:
            print("Error writing clues file:", self.gamefile)
            return False
        return True

    def read_alibis(self):
        try:
            with open("data/alibis.txt", 'r') as file:
                self.alibis = [line.strip() for line in file]
        except OSError:
            print("Error reading alibis.txt")

    def wipe_alibis(self):
        self.alibis=[self.myname]
        self.write_alibis()

    def write_alibis(self):
        try:
            fhandle = open("data/alibis.txt", 'w')
            fhandle.write("\n".join(self.alibis))
            fhandle.close()
        except OSError:
            print("Error writing ailbis file")
            return False
        return True

