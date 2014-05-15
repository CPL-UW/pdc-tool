import numbers, json, sys, argparse
from collections import defaultdict
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

'''
	Copyright 2014, CPL
	This script was written and maintained by Matthew Berland, Dennis Ramirez (@dennisRamirez), Jazmyn Russell
	This script is provided as is with no other guarantees.
	Please comment code.
'''

def getKeySums(filepath):
	output = ''
	jfile = open(filepath,'rb')
	jdata = json.loads(jfile.read())
	key_dict = {}
	for x in jdata:
		if x["key"] in key_dict:
			key_dict[x["key"]] += 1
		else:
			key_dict[x["key"]] = 1
	output += '\nUnique keys and counts:\n'
	for y in key_dict.keys():
		output += y+', '+str(key_dict[y])