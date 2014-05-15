import numbers, json, sys, argparse, os
from collections import defaultdict
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

'''
	Copyright 2014, CPL
	This script was written and maintained by Matthew Berland, Dennis Ramirez (@dennisRamirez), Jazmyn Russell
	This script is provided as is with no other guarantees.
	Please comment code.
'''

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
	
def get_headers(pdata, coldict):
	header_line = ""
	for line in pdata:
		for col in line:
			coldict[col] = True
	for col in sorted(coldict):
		header_line = header_line + col + ','
	return header_line
	
def getCSV(filepath):
	csvout = ""
	jfile = open(filepath,'rb')
	data = json.loads(jfile.read())
	#find the column headers
	csvout = csvout + get_headers(data, defaultdict(bool))
	for line in data:
		lineout = defaultdict(str)
        outputlist = []
        for elem in line:
            lineout[elem] = line[elem]
        for col in sorted(columns):
            outputlist.append(str(lineout[col]))
        csvout = csvout + "\"",'","'.join(outputlist),"\""
    return csvout
