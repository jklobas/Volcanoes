from __future__ import division
import numpy as np
import re

def parser(filename): #returns np array
	inp = open(filename).readlines()
	timedepth = len(inp)/(55*51*19) #55 lines per entry, 51 levels, 19 lats
	pdepth = 51 #51 pressure levels
	latdepth = 19 #19 latitudes
	#                   z        p         l     y  
	out = np.zeros((timedepth, pdepth, latdepth, 54,2), dtype = 'object')
	counterlist = [] #list of counters
	for x in range(0,len(inp)): #list of linenumbers to read / counters
		if x%55 ==0:
			counterlist.append(int(np.floor(x/55)))
	for x in counterlist:
		for y in range(1,55):
			linenum = (x*55)+y
			if y ==1: #grep indices from header
				p = int(re.search(r"(?<=J=)\s?\w+", inp[linenum]).group()) -1
				l = int(re.search(r"(?<=\I=)\s?\w+", inp[linenum]).group())-1
			        z = np.floor(linenum / (55*51*19))
				out[z,p,l,y-1,0] = float(re.search(r"(?<=\O3=)\-?\s*\d+\.?\d*(?:[Ee]\+\d+)?",inp[linenum]).group())
				out[z,p,l,y-1,1] = float(re.search(r"(?<=\VD=)\-?\s*\d+\.?\d*(?:[Ee]\+\d+)?",inp[linenum]).group())	
			if 1 < y < 54: #grep rates and constants from lines
				out[z,p,l,y-1,0] = float(re.search(r"(?<=RATE=)\s*\+?\-?\s*\d+\.?\d*(?:[Ee]\+?\-?\d+)?",inp[linenum]).group())
				out[z,p,l,y-1,1] = float(re.search(r"(?<=CONC=)\s*\+?\-?\s*\d+\.?\d*(?:[Ee]\+?\-?\d+)?",inp[linenum]).group())
			if y == 54: #grep total ozone rates
				out[z,p,l,y-1,0] = float(re.search(r"(?<=PROD=)\s*\+?\-?\s*\d+\.?\d*(?:[Ee]\+?\-?\d+)?",inp[linenum]).group())
				out[z,p,l,y-1,1] = float(re.search(r"(?<=LOSS=)\s*\+?\-?\s*\d+\.?\d*(?:[Ee]\+?\-?\d+)?",inp[linenum]).group())
	
			
	return out
		
		
def rxnrates(outplq, day): #extracts rate data from output of .parser()

#	for x in range(2,55):
#		match = re.search(r"(?<=BR)", str.split(inp[x])[0]
#		if match:
#			print x-1
	Brrows = [3,33,34,35,36,37,40,41,42,43,44,45,46,47,48,49]
	BrClrows = [38,39]
	Clrows = [2,4,20,21,22,23,24,25,26,27,28,29,30,31,32]
	NOxrows = [5,7,8,9,18,19]
	HOxrows = [6,10,11,12,13,14,15,16,17]
	Oxrows = [1,50]
	O3 = np.zeros((51,19,2), dtype = "object")
	Prod = np.zeros((51,19,2), dtype = "object")
	Loss = np.zeros((51,19,2), dtype = "object")
	Brx = np.zeros((51,19,2), dtype = "object")
	BrxClx = np.zeros((51,19,2), dtype = "object")
	Clx = np.zeros((51,19,2), dtype = "object")
	NOx = np.zeros((51,19,2), dtype = "object")
	HOx = np.zeros((51,19,2), dtype = "object")
	Ox = np.zeros((51,19,2), dtype = "object")
	
		
	for level in range(len(outplq[day])):
		for lat in range(len(outplq[day][level])):
			O3[level][lat][0] = outplq[day][level][lat][0][0] #number density of O3
			O3[level][lat][1] = np.divide(outplq[day][level][lat][0][0], outplq[day][level][lat][0][1]) #mixing ratio of O3
			Prod[level][lat][0] = outplq[day][level][lat][53][0] 
			Loss[level][lat][0] = outplq[day][level][lat][53][1]	
			Brx[level][lat][0] = np.sum([np.sum(outplq[day][level][lat][x][0] ) for x in Brrows]) #for the following [0] is rate
			Brx[level][lat][1] = np.sum([np.sum(outplq[day][level][lat][x][1] ) for x in Brrows if outplq[day][level][lat][x][1] < 0]) #for the following [1] is rate*conc
			BrxClx[level][lat][0] = np.sum([np.sum(outplq[day][level][lat][x][0] ) for x in BrClrows])
			BrxClx[level][lat][1] = np.sum([np.sum(outplq[day][level][lat][x][1] ) for x in BrClrows if outplq[day][level][lat][x][1] < 0])
			Clx[level][lat][0] = np.sum([np.sum(outplq[day][level][lat][x][0] ) for x in Clrows])
			Clx[level][lat][1] = np.sum([np.sum(outplq[day][level][lat][x][1] ) for x in Clrows if outplq[day][level][lat][x][1] < 0])
			NOx[level][lat][0] = np.sum([np.sum(outplq[day][level][lat][x][0] ) for x in NOxrows])
			NOx[level][lat][1] = np.sum([np.sum(outplq[day][level][lat][x][1] ) for x in NOxrows if outplq[day][level][lat][x][1] < 0])
			HOx[level][lat][0] = np.sum([np.sum(outplq[day][level][lat][x][0] ) for x in HOxrows])
			HOx[level][lat][1] = np.sum([np.sum(outplq[day][level][lat][x][1] ) for x in HOxrows if outplq[day][level][lat][x][1] < 0])
			Ox[level][lat][0] = np.sum([np.sum(outplq[day][level][lat][x][0] ) for x in Oxrows])
			Ox[level][lat][1] = np.sum([np.sum(outplq[day][level][lat][x][1] ) for x in Oxrows if outplq[day][level][lat][x][1] < 0])
	return O3, Prod, Loss, Brx, BrxClx, Clx, NOx, HOx, Ox
		
		
