#!/usr/bin/python3

import random
import sys

myt = list()
mya = list()
myv = list()

threat = "SIM Swap"
actor = "PlugwalkJoe"
victim = "T-Mobile"

myt.append("SIM Swap")
myt.append("Malware")
myt.append("Ransomware")
mya.append("PlugwalkJoe")
mya.append("ALPHV")
mya.append("China")
myv.append("T-Mobile")
myv.append("MGM")
myv.append("European Council")

for i in range(0,199):
	fn = "g1/" + str(i) + "_game1.csv"
	f = open(fn,"w")
	myq = i%6
	for j in myt:
		f.write("T,"+j+",0,,\n")
	for k in mya:
		f.write("A,"+k+",0,,\n")
	for l in myv:
		f.write("V,"+l+",0,,\n")
	if myq == 0:
		f.write("*,ALPHV")
	elif myq == 1:
		f.write("*,China")
	elif myq == 2:
		f.write("*,Ransomware")
	elif myq == 3:
		f.write("*,Malware")
	elif myq == 4:
		f.write("*,MGM")
	elif myq == 5:
		f.write("*,European Council")
	f.close()



