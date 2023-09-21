#!/usr/bin/python3

import random
import sys

myt = list()
mya = list()
myv = list()

threat = "DNS"
actor = "Sea Turtle"
victim = "Turkey"

myt.append("DNS")
myt.append("SQL-i")
myt.append("Zero Day")
myt.append("Zero Day")
myt.append("Malware")
myt.append("Defacement")
mya.append("Sea Turtle")
mya.append("Lulz Sec")
mya.append("Lamberts")
mya.append("Israel")
mya.append("Shamoon")
mya.append("SEA")
myv.append("Turkey")
myv.append("HB Gary")
myv.append("China")
myv.append("Iran")
myv.append("Saudi ARAMCO")
myv.append("UCLA")

for i in range(0,199):
	fn = "g4/" + str(i) + "_game4.csv"
	f = open(fn,"w")
	myq = i%15
	for j in myt:
		f.write("T,"+j+",0,,\n")
	for k in mya:
		f.write("A,"+k+",0,,\n")
	for l in myv:
		f.write("V,"+l+",0,,\n")
	if myq == 0:
		f.write("*,SQL-i")
	elif myq == 1:
		f.write("*,Zero Day")
	elif myq == 2:
		f.write("*,Zero Day")
	elif myq == 3:
		f.write("*,Malware")
	elif myq == 4:
		f.write("*,Defacement")
	elif myq == 5:
		f.write("*,Lulz Sec")
	elif myq == 6:
		f.write("*,Lamberts")
	elif myq == 7:
		f.write("*,Israel")
	elif myq == 8:
		f.write("*,Shamoon")
	elif myq == 9:
		f.write("*,SEA")
	elif myq == 10:
		f.write("*,HB Gary")
	elif myq == 11:
		f.write("*,China")
	elif myq == 12:
		f.write("*,Iran")
	elif myq == 13:
		f.write("*,Saudi ARAMCO")
	elif myq == 14:
		f.write("*,UCLA")
	f.close()



