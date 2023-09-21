#!/usr/bin/python3

import random
import sys

myt = list()
mya = list()
myv = list()

threat = "Supply Chain"
actor = "Stupidity"
victim = "Okta"

myt.append("Supply Chain")
myt.append("Supply Chain")
myt.append("Malware")
myt.append("Malware")
myt.append("Supply Chain")
mya.append("North Korea")
mya.append("Russia")
mya.append("China")
mya.append("Russia")
mya.append("Stupidity")
myv.append("3CX")
myv.append("Solar Winds")
myv.append("Taiwan")
myv.append("Ukraine")
myv.append("Okta")

for i in range(0,199):
	fn = "g3/" + str(i) + "_game3.csv"
	f = open(fn,"w")
	myq = i%12
	for j in myt:
		f.write("T,"+j+",0,,\n")
	for k in mya:
		f.write("A,"+k+",0,,\n")
	for l in myv:
		f.write("V,"+l+",0,,\n")
	if myq == 0:
		f.write("*,Supply Chain")
	elif myq == 1:
		f.write("*,Supply Chain")
	elif myq == 2:
		f.write("*,Malware")
	elif myq == 3:
		f.write("*,Malware")
	elif myq == 4:
		f.write("*,North Korea")
	elif myq == 5:
		f.write("*,Russia")
	elif myq == 6:
		f.write("*,China")
	elif myq == 7:
		f.write("*,Russia")
	elif myq == 8:
		f.write("*,3CX")
	elif myq == 9:
		f.write("*,Solar Winds")
	elif myq == 10:
		f.write("*,3CX")
	elif myq == 11:
		f.write("*,Taiwan")
	f.close()



