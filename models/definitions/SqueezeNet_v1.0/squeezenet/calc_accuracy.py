import os, sys, time

lines = [line.strip() for line in open(sys.argv[1],"r").readlines()]
correct=0
for line in lines:
	truth=line.split("/")[6]
	predict=line.split(" ")[3]
	if truth==predict:
		correct+=1
print "accuracy=%s"%(float(correct)/len(lines))
