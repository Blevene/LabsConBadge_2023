import circuitpython_csv

class gamedata:
    myclue=None
    myname=None
    threats=[]
    attacks=[]
    victims=[]
    def __init__(self,gamenum):
        self.read_name()
        self.read_clues_collection("data/game"+str(gamenum)+".csv")
        self.check_clue(self.myclue,"I")

    def check_clue(self,newclue,alibi):
        # todo: decrypt
        #print(newclue,alibi)
        for clue in (self.threats+self.attacks+self.victims):
            if clue[1] == newclue: 
                clue[3] = newclue
                clue[4] = alibi
                return newclue
        return False 
    
    def is_solved(self):

        #for t in threats:# for t,a,v
            # for each clue
                # if clue is null append to suspects
            # if >1 suspect return false
        return True

    def read_name(self):
        #getname, if not, do oob?
        try:
            with open("data/myname",'r') as file:
                self.myname=file.readline().rstrip()
                print("hello",self.myname)
        except OSError:
            print("Error reading name from file")
            self.myname="unknown"

    def read_clues_collection(self,filename):
        #should only be called by constructor at powerup
        try:
            with open(filename, 'r') as file:
                csv=circuitpython_csv.reader(file)
                for row in csv:
                    if row[0] == "T":self.threats.append(row)
                    elif row[0] == "A":self.attacks.append(row)
                    elif row[0] == "V":self.victims.append(row)
                    elif row[0] == "*":self.myclue=row[1]
        except OSError:
            print("Error reading from file:", filename)

    def write_clues_collection(self,filename, collection):
        #should be called every time we add a clue?
        try:
            fhandle = open(filename, 'w')
            fhandle.write("\n".join(collection))
            fhandle.close()
        except OSError:
            print("Error writing file:", filename)
            return False
        return True

        
