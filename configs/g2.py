#!/usr/bin/python3

import random
import sys

myt = list()
mya = list()
myv = list()

threat = "Zero Day"
actor = "Russia"
victim = "Excahnge Servers"

myt.append("Ransomware")
myt.append("Phishing")
myt.append("Social Eng")
myt.append("Zero Day")
mya.append("China")
mya.append("North Korea")
mya.append("Russia")
mya.append("Periwinkle Temp")
myv.append("Costa Rica")
myv.append("McDonalds")
myv.append("Sec Researchers")
myv.append("Exchange Servers")

for i in range(0,199):
	fn = "g2/" + str(i) + "_game2.csv"
	f = open(fn,"w")
	myq = i%9
	for j in myt:
		f.write("T,"+j+",0,,\n")
	for k in mya:
		f.write("A,"+k+",0,,\n")
	for l in myv:
		f.write("V,"+l+",0,,\n")
	if myq == 0:
		f.write("*,Ransomware")
	elif myq == 1:
		f.write("*,Phishing")
	elif myq == 2:
		f.write("*,Social Eng")
	elif myq == 3:
		f.write("*,Periwinkle Temp")
	elif myq == 4:
		f.write("*,China")
	elif myq == 5:
		f.write("*,North Korea")
	elif myq == 6:
		f.write("*,Costa Rica")
	elif myq == 7:
		f.write("*,McDonalds")
	elif myq == 8:
		f.write("*,Sec Researchers")
	f.close()



