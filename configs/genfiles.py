#!/usr/bin/python3
import random
import os

def gengamefiles(gamenum,threats,attacks,victims):    
    cluecsv=""
    for j in threats:
        cluecsv+="T,"+j+",0,,\n"
    for k in attacks:
        cluecsv+="A,"+k+",0,,\n"
    for l in victims:
        cluecsv+="V,"+l+",0,,\n"
    threats.pop(random.randrange(len(threats)))
    attacks.pop(random.randrange(len(attacks)))
    victims.pop(random.randrange(len(victims)))
    allclues=(threats+attacks+victims)

    for i in range(50):
        os.makedirs(str(i),exist_ok=True)
        f=open(str(i) + "/game"+str(gamenum)+".csv", "w")
        f.write(cluecsv+"*,"+allclues[i%len(allclues)]+"\n")
        f.close()

gengamefiles(0,
    ["Lapsus", "North Korea"],
    ["Social Eng", "Cred Stuffing"],
    ["NVIDIA", "SWIFT"])

gengamefiles(1,
    ["PlugwalkJoe", "ALPHV", "China"],
    ["SIM Swap", "Malware", "Ransomware"],
    ["T-Mobile", "MGM", "EU Council"])

gengamefiles(2,
    ["North Korea", "China", "Russia", "Stupidity"],
    ["Supply Chain","Malware"],
    ["3CX", "Solar Winds", "Taiwan", "Ukraine", "Okta"])

gengamefiles(3,
    ["China", "North Korea", "Russia", "Periwinkle Temp"],
    ["Ransomware", "Phishing", "Social Eng", "Zero Day"],
    ["Costa Rica", "McDonalds", "Sec Researchers", "Exchange Servers"])

gengamefiles(4,
    ["Sea Turtle", "Lulz Sec", "Lamberts", "Israel", "Shamoon", "SEA"],
    ["DNS", "SQL-i", "Zero Day", "Zero Day", "Malware", "Defacement"],
    ["Turkey", "HB Gary", "China", "Iran", "Saudi ARAMCO", "UCLA"])

gengamefiles(5,
    ["ALPHV", "APT39", "Black Basta", "Fancy Bear", "j4guar17", "Kevin Mitnick", "North Korea"],
    ["Phishing", "Ransomware", "Social Engineering", "SQL Injection"],
    ["7-Eleven", "ADA", "Ceasers", "DNC", "Kuwait", "Maresk", "Nokia"])

gengamefiles(6,
    ["Anonymous", "China", "Mirai", "North Korea", "Rubico", "Russia"],
    ["Cred Stuffing", "DDoS", "iMessage", "Phishing", "Graains of Rice"],
    ["Code Cove", "DynDNS", "Iran", "Sarah Palin", "Sony", "SuperMicro", "Ukraine"])

gengamefiles(7,
    ["Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"],
    ["Col. Mustard", "Dr. Scarlett", "Mr. Green", "Ms. White", "Mx. Peacock", "Prof. Plum"],
    ["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Lounge", "Study"])
