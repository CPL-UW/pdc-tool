import numbers, json, sys, argparse, os, time, datetime
from collections import defaultdict
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

'''
	Copyright 2014, CPL
	This script was written and maintained by Matthew Berland, Dennis Ramirez (@dennisRamirez), Jazmyn Russell
	This script is provided as is with no other guarantees.
	Please comment code.
'''

#this function is a simple function for first pass csv writing.
def toCSV(fileName, formattedText):
	f = open(os.path.join(os.path.dirname(__file__),'outputs/'+fileName), 'w')
	f.write(formattedText)
	f.close()
	print("file saved as "+fileName)


def getKeySums(filename):
	output = ''
	jfile = open(os.path.join(os.path.dirname(__file__),'uploads/'+filename),'rb')
	jdata = json.loads(jfile.read())
	key_dict = {}
	for x in jdata:
		if x["key"] in key_dict:
			key_dict[x["key"]] += 1
		else:
			key_dict[x["key"]] = 1
	for y in key_dict.keys():
		output += y+', '+str(key_dict[y])+'\n'
	return output
	
def getKeys(filename):
	jfile = open(os.path.join(os.path.dirname(__file__),'uploads/'+filename),'rb')
	jdata = json.loads(jfile.read())
	key_dict = {}
	for x in jdata:
		if x["key"] in key_dict:
			key_dict[x["key"]] += 1
		else:
			key_dict[x["key"]] = 1
	return key_dict.keys()

#
def getKeySumsByPlayer(filename):
	jfile = open(os.path.join(os.path.dirname(__file__),'uploads/'+filename),'rb')
	jdata = json.loads(jfile.read())
	use_dict = {}
	key_dict = []
	csvOut = "User ID"
	
	for x in jdata:
		if x["user_id"] in use_dict:
			if x["key"] in use_dict[x["user_id"]]:
				use_dict[x["user_id"]][x["key"]] += 1
			else:
				use_dict[x["user_id"]][x["key"]] = 1
		else:
			use_dict[x["user_id"]] = {}
			use_dict[x["user_id"]]["key"] = 1
	for x in jdata:
		if not x["key"] in key_dict:
			key_dict.append(x["key"])
	
	for t in key_dict:
		csvOut += ","+t
	csvOut += "\n"
	
	for y in use_dict.keys():
		csvOut += str(y)
		for t in key_dict:
			if t != "User ID":
				if t in use_dict[y].keys():
					csvOut += ","+str(use_dict[y][t])
				else:
					csvOut += ",0"
		csvOut +="\n"
	return csvOut
	
#Functions to Plot
#assumes timestamp
def plotVar(filename, Key):
	jfile = open(os.path.join(os.path.dirname(__file__),'uploads/'+filename),'rb')
	jdata = json.loads(jfile.read())
	x = []
	y = []
	z = []
	firstTime = False;
	count = 0
	t1 = 0
	for d in jdata:
		if d["key"] == Key:
			count += 1
			if not(firstTime):
				t1 = float(d["timestamp"])
				firstTime = True;
			#since I remove the first timestamp from each sequential we get the delta in ms.
			y.append((float(d["timestamp"])-t1)/1000/60) #this converts it to minutes
			x.append(count)
	pl.clf()
	pl.plot(x, y) #, 'ro' <- if you want red dots.
	pl.ylabel(Key)
	pl.xlabel('Time')
	oName = str(time.mktime(datetime.datetime.now().timetuple()))+'.png'
	pl.savefig(os.path.join(os.path.dirname(__file__))+'/outputs/'+oName)
	return oName
	
#Functions to Plot
#assumes timestamp
def plotVars(filename, Key1, Key2):
	jfile = open(os.path.join(os.path.dirname(__file__),'uploads/'+filename),'rb')
	jdata = json.loads(jfile.read())
	x = []
	y = []
	z = []
	firstTime = False;
	count1 = 0
	count2 = 0
	for d in jdata:
		if d["key"] == Key1:
			count1 += 1
			y.append(count1) #this converts it to minutes
			x.append(count2)
		elif d["key"] == Key2:
			count2 += 1
			y.append(count1) #this converts it to minutes
			x.append(count2)
	pl.clf()
	pl.plot(x, y)#, 'ro')
	pl.ylabel(Key1)
	pl.xlabel(Key2)
	oName = str(time.mktime(datetime.datetime.now().timetuple()))+'.png'
	pl.savefig(os.path.join(os.path.dirname(__file__))+'/outputs/'+oName)
	return oName

#functions for converting to CSV	
def get_headers(pdata, coldict):
	header_line = ""
	for line in pdata:
		for col in line:
			coldict[col] = True
	for col in sorted(coldict):
		header_line = header_line + col + ','
	return header_line

def find_columns(colsdict, data):
    for line in data:
        for col in line:
            colsdict[col] = True

def print_columns(colsdict, data):
    for col in sorted(colsdict):
        print col,',',
    print ''

def parse_day(daystring):
    return daystring[:10]

def getCSV(filepath):
	jfile = open(filepath,'rb')
	data = json.loads(jfile.read())
	columns = defaultdict(bool)
	
	find_columns(columns, data)
	csvout = ""
	for col in sorted(columns):
		csvout += col + ','
	csvout += '\n'
	
	for line in data:
		lineout = defaultdict(str)
		outputlist = []
		for elem in line:
			lineout[elem] = line[elem]
		for col in sorted(columns):
			outputlist.append(str(lineout[col]))
		csvout += "\""+'","'.join(outputlist)+"\"\n"
	return csvout