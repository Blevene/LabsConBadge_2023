#!/usr/bin/python3
import random
import os

#build $filecount unique files for separate badges.
#each file will be a CSV of all the T,A, and V for that game
#each file will also have a unique * line with one clue 
def gengamefiles(gamenum,threats,attacks,victims,filecount=None):
    #we'll re-write this for each file, so build a string
    #one line per clue, coded with the clue type
    cluecsv=""
    for j in threats: cluecsv+="T,"+j+",0,,\n"
    for k in attacks: cluecsv+="A,"+k+",0,,\n"
    for l in victims: cluecsv+="V,"+l+",0,,\n"

    #select the winning combo - randomly choose a threat, attack, and victim
    threats.pop(random.randrange(len(threats)))
    attacks.pop(random.randrange(len(attacks)))
    victims.pop(random.randrange(len(victims)))

    #combine what's left so we can give one each
    allclues=(threats+attacks+victims)
    
    #if we don't specify how many files, do one of each.
    if filecount is None: filecount=len(allclues)

    for i in range(filecount):
        #make the dir if not already there
        os.makedirs(str(i),exist_ok=True)
        #create the game file
        f=open(str(i) + "/game"+str(gamenum)+".csv", "w")
        #write the generated CSV, followed by one line with a * containing a single clule
        f.write(cluecsv+"*,"+allclues[i%len(allclues)]+"\n")
        f.close()

gengamefiles(0,
    ["Lapsus", "North Korea"],
    ["Social Eng", "Cred Stuffing"],
    ["NVIDIA", "SWIFT"],
    50)

gengamefiles(1,
    ["PlugwalkJoe", "ALPHV", "China"],
    ["SIM Swap", "Malware", "Ransomware"],
    ["T-Mobile", "MGM", "EU Council"],
    50)

gengamefiles(2,
    ["North Korea", "China", "Russia", "Stupidity"],
    ["Supply Chain","Malware"],
    ["3CX", "Solar Winds", "Taiwan", "Ukraine", "Okta"],
    50)

gengamefiles(3,
    ["China", "North Korea", "Russia", "Periwinkle Temp"],
    ["Ransomware", "Phishing", "Social Eng", "Zero Day"],
    ["Costa Rica", "McDonalds", "Sec Researchers", "Exchange Servers"],
    50)

gengamefiles(4,
    ["Sea Turtle", "Lulz Sec", "Lamberts", "Israel", "Shamoon", "SEA"],
    ["DNS", "SQL-i", "Zero Day", "Zero Day", "Malware", "Defacement"],
    ["Turkey", "HB Gary", "China", "Iran", "Saudi ARAMCO", "UCLA"],
    50)

gengamefiles(5,
    ["ALPHV", "APT39", "Black Basta", "Fancy Bear", "j4guar17", "Kevin Mitnick", "North Korea"],
    ["Phishing", "Ransomware", "Social Engineering", "SQL Injection"],
    ["7-Eleven", "ADA", "Ceasers", "DNC", "Kuwait", "Maresk", "Nokia"],
    50)

gengamefiles(6,
    ["Anonymous", "China", "Mirai", "North Korea", "Rubico", "Russia"],
    ["Cred Stuffing", "DDoS", "iMessage", "Phishing", "Graains of Rice"],
    ["Code Cove", "DynDNS", "Iran", "Sarah Palin", "Sony", "SuperMicro", "Ukraine"],
    50)

gengamefiles(7,
    ["Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"],
    ["Col. Mustard", "Dr. Scarlett", "Mr. Green", "Ms. White", "Mx. Peacock", "Prof. Plum"],
    ["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Lounge", "Study"],
    50)
