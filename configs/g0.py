#!/usr/bin/python3

import random
import sys

myt = list()
mya = list()
myv = list()

threat = "Social Eng"
actor = "Lapsus"
victim = "NVIDIA"

myt.append("Social Eng")
myt.append("Cred Stuffing")
mya.append("Lapsus")
mya.append("North Korea")
myv.append("NVIDIA")
myv.append("SWIFT")

for i in range(0,199):
	fn = "g0/" + str(i) + "_game0.csv"
	f = open(fn,"w")
	myq = random.randint(0,1000000)
	myn = myq % 3
	if myn == 0:
		for j in myt:
			f.write("T,"+j+",0,,\n")
		for k in mya:
			f.write("A,"+k+",0,,\n")
		for l in myv:
			f.write("V,"+l+",0,,\n")
		f.write("*,Cred Stuff\n")
	if myn == 1:
		for j in myt:
			f.write("T,"+j+",0,,\n")
		for k in mya:
			f.write("A,"+k+",0,,\n")
		for l in myv:
			f.write("V,"+l+",0,,\n")
		f.write("*,North Korea\n")
	if myn == 2:
		for j in myt:
			f.write("T,"+j+",0,,\n")
		for k in mya:
			f.write("A,"+k+",0,,\n")
		for l in myv:
			f.write("V,"+l+",0,,\n")
		f.write("*,SWIFT\n")
	f.close()



