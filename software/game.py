import circuitpython_csv
import gc
import binascii

# this class contains all the data relevant to the game. It manages
# loading the data from files, updating it, and writing it back.
class gamedata:
    gamenum=0
    myclue=None
    myname=None
    mytxval=None
    newclue=None
    namefile="data/myname.txt"
    gamefile="data/game1.csv"
    alibifile="data/alibis.txt"

    #clues are stored in these three lists. Counts are stored for frequent use
    threats=[]
    attacks=[]
    victims=[]
    cluecounts=[0,0,0]
    alibis=[]

    #initialize all the data. Read all 3 files and load into memory
    def __init__(self,gamenum=0):
        self.gamenum=gamenum
        self.read_name()
        self.read_alibis()
        self.gamefile="data/game"+str(gamenum)+".csv"
        self.read_clues()

    #check a clue, and if valid for this game, add it to the sturcre.
    def check_clue(self,newclue,alibi):
        #gc here since this is the densest memory allocation
        gc.collect()
        #if we haven't met the alibi before, a them to the list, and flush to disk
        if alibi not in self.alibis:
            self.alibis.append(alibi)
            self.write_alibis()
        else:
            print(f"Alibi {alibi} already known")
        #iterate over all clues. If we have the clue, mark it collectes, log the alibi,
        #flag it so the dislplay knows to update it, and flush to disk
        for j, cluetype in enumerate([self.threats,self.attacks,self.victims]):
            for i in range(self.cluecounts[j]):
                if cluetype[i][1]==newclue:
                    cluetype[i][3]=newclue
                    cluetype[i][4]=alibi
                    self.newclue=[i,j]
                    self.write_clues()
                    return newclue
        return False

    #load name from file - if it's not there, set to unknown
    #note that we don't do the oob flow here because that needs
    #control of display we don't want in the data storage class.
    def read_name(self):
        try:
            with open("data/myname.txt",'r') as file:
                self.myname=file.readline().rstrip()
                print("hello",self.myname)
        except OSError:
            print("Error reading name from data/myname.txt")
            self.myname="unknown"

    #clear name and write to file
    def wipe_name(self):
        self.myname=""
        self.write_name()

    #open the name file and write out to it
    def write_name(self):
        try:
            with open("data/myname.txt", 'w') as fhandle:
                fhandle.write(self.myname)
        except OSError:
            print("Error writing name file")
            return False
        return True

    #read csv file of clues for this game. Can be called again
    #to change to a different game number
    def read_clues(self):
        try:
            with open(self.gamefile, 'r') as file:
                csv=circuitpython_csv.reader(file)
                self.threats=[]
                self.attacks=[]
                self.victims=[]
                #first value tells us what type of clue it is
                for row in csv:
                    if row[0] == "T":self.threats.append(row)
                    elif row[0] == "A":self.attacks.append(row)
                    elif row[0] == "V":self.victims.append(row)
                    elif row[0] == "*":self.myclue=row[1]
            #calculate the frequently-used cluecounts
            self.cluecounts=[len(self.threats),len(self.attacks),len(self.victims)]
            #add our clue to the table
            self.check_clue(self.myclue,self.myname)
            #calculate the message we'll send when we trade.
            crc = hex(binascii.crc32(bytearray(str(self.myclue)+","+str(self.myname))))[2:]
            crs = bytearray([13,13,13,13,13,13,13,13])
            print(crc,self.myclue,self.myname)
            #lead-in of CRs, followed by CRC, clue, and name
            self.mytxval=crs+bytearray(",".join([crc,self.myclue,self.myname]))
            print(f"{self.mytxval}")
        except OSError:
            print("Error reading from file:", self.gamefile)

    #essentially 'resets' the current game, wiping all clues then adding yours back
    def wipe_clues(self):
        for cluetype in [self.threats,self.attacks,self.victims]:
            for clue in cluetype:
                if clue!=self.myclue:
                    clue[3]=""
                    clue[4]=""
        self.newclue=-1
        self.check_clue(self.myclue,self.myname)
        self.write_clues()

    #write clues csv to disk so it persists through power cycles
    def write_clues(self):
        #should be called every time we add a clue?
        try:
            fhandle = open(self.gamefile, 'w')
            for cluetype in [self.threats,self.attacks,self.victims]:
                for clue in cluetype:
                    #just joint it all with comas
                    fhandle.write(",".join(clue))
                    fhandle.write("\n")
            #tack on your clue at the end
            fhandle.write("*,"+str(self.myclue))
            fhandle.close()
        except OSError:
            print("Error writing clues file:", self.gamefile)
            return False
        return True

    #load list of alibis from disk
    def read_alibis(self):
        try:
            with open("data/alibis.txt", 'r') as file:
                self.alibis = [line.strip() for line in file]
        except OSError:
            print("Error reading alibis.txt")

    #clear list of alibis excep for yourself, and flush to disk
    def wipe_alibis(self):
        self.alibis=[self.myname]
        self.write_alibis()

    #write alibis to disk, one per line
    def write_alibis(self):
        try:
            fhandle = open("data/alibis.txt", 'w')
            fhandle.write("\n".join(self.alibis))
            fhandle.close()
        except OSError:
            print("Error writing ailbis file")
            return False
        return True