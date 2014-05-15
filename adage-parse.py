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

# States the feilds that can be parsed by this script
parser = argparse.ArgumentParser(description='Transform ADAGE formatted raw JSON data.')
parser.add_argument('-f', metavar='FILE.json', type=str, help='ADAGE API formatted JSON file', required=True)
parser.add_argument('--elem', metavar='FIELD', type=str, help='Field in data (e.g., user_id)', nargs='+')
#TODO parser.add_argument('--usersum', action="store_true", help='numeric field(s) summed over a user_id')
#TODO parser.add_argument('--totalsum', action="store_true", help='numeric field(s) summed over the entire file')

parser.add_argument('--csvfy', action="store_true", help='turns entire file into CSV (note: 2n for n lines to get all fields)')

parser.add_argument('--userdaytotalcsv', action="store_true", help='create buckets by day csv by user')

parser.add_argument('--heatmap', action="store_true", help='Generates a heat map based on all player click events')

parser.add_argument('--keysums', action="store_true", help='Identifies all unique keys in the given json file and prints their counts to the screen')

parser.add_argument('--keysumsbyplayer', action="store_true", help='Identifies all unique user IDs and keeps a count of the unique keys in the given json file')

args = parser.parse_args()

jsonfile = open(args.f,'rb')
data = json.loads(jsonfile.read())

def find_columns(colsdict):
    for line in data:
        for col in line:
            colsdict[col] = True

def print_columns(colsdict):
    for col in sorted(colsdict):
        print col,',',
    print ''

def parse_day(daystring):
    return daystring[:10]
    
def toCSV(fileName, formattedText):
    f = open(fileName, 'w')
    f.write(formattedText)
    f.close()
    print("file saved as "+fileName)

columns = defaultdict(bool)

# If selected, this option produces a CSV of the specified .json file 
#
# TODO: change this to write to file rather than printing and relying on pipes
if args.csvfy:
#TODO encapsulate all the things
    find_columns(columns)
    print_columns(columns)
    for line in data:
        lineout = defaultdict(str)
        outputlist = []
        for elem in line:
            lineout[elem] = line[elem]
        for col in sorted(columns):
            outputlist.append(str(lineout[col]))
        print "\"",'","'.join(outputlist),"\""
        
elif args.userdaytotalcsv:
    find_columns(columns)
    print_columns(columns)
    userdaydict = defaultdict(lambda : defaultdict(lambda : defaultdict(list)))
    userdayout = defaultdict(lambda : defaultdict(lambda : defaultdict(str)))
    for line in data:
        user = line['user_id']
        day = parse_day(line['created_at'])
        for elem in line:
            userdaydict[user][day][elem].append(line[elem])
    for u in userdaydict:
        for d in userdaydict[u]:
            for e in userdaydict[u][d]:
                retlist = userdaydict[u][d][e]
                if all(isinstance(item, numbers.Number) for item in retlist):
                    userdayout[u][d][e] = str(sum(retlist)/len(retlist))
                if any(isinstance(item, list) or isinstance(item,dict) for item in retlist):
                    outlist = []
                    [outlist.append(i) for i in retlist if i not in outlist]
                    #TODO fix this stupid hack. for endless lists probably just ignore.
                    if len(outlist) < len(retlist)/2:
                        userdayout[u][d][e] = str(outlist)
                    else:
                        userdayout[u][d][e] = 'sample: ' + str(outlist[0])
                else:
                    retset = frozenset(retlist)
                    if len(retset) == 1:
                        userdayout[u][d][e] = str(retlist.pop())
                    elif len(retset) == len(retlist):
                        userdayout[u][d][e] = 'sample: ' + str(retlist.pop())
                    else: 
                        userdayout[u][d][e] = str(list(retset))
    for u in userdayout:
        for d in userdayout[u]:
            outstr = ''
            for c in sorted(columns):
                outstr += '\"' + userdayout[u][d][c] + '\",'
            print outstr
            
# If selected, each value of the supplied arguments to the flag -elem are printed to the screen.
elif args.elem:
    searchfields = args.elem
    for elem in data:
        print [elem[x] for x in elem if x in searchfields] 
        
elif args.keysums:
    key_dict = {}
    for x in data:
        if x["key"] in key_dict:
            key_dict[x["key"]] += 1
        else:
            key_dict[x["key"]] = 1
    print("\nUnique keys and counts:\n")
    for y in key_dict.keys():
        print(y+", "+str(key_dict[y]))


#Check to see if we have a user Id, if we don't add it and the key to our struct
#if we do, only check to see if the key is in the struct and increase/set it's count.
#TODO: Bryan pointed out that we'll be working with a lot of data. Will need rewrite so that
#csvOut does not contain all data and is instead written to a file.
elif args.keysumsbyplayer:
    use_dict = {}
    key_dict = []

    csvOut = "User ID"

    for x in data:
        if x["user_id"] in use_dict:
            if x["key"] in use_dict[x["user_id"]]:
                use_dict[x["user_id"]][x["key"]] += 1
            else:
                use_dict[x["user_id"]][x["key"]] = 1
        else:
            use_dict[x["user_id"]] = {}
            use_dict[x["user_id"]]["key"] = 1
    for x in data:
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
    
    toCSV("KeySumsByPlayer.csv",csvOut)

    #keeping this in tact because it's nicely formatted for a GUI
    ''' print("\nUnique keys and counts:\n")
        for y in use_dict.keys():
        print("User ID = "+str(y))
        for z in use_dict[y].keys():
            print("   "+z+", "+str(use_dict[y][z]))'''

#This script assumes you have numpy and mpl_toolkits installed. It'll choke if you don't
#This method assumes 2 things right now A) a 3d world, and B) that you implemented PathWorldClick
#TODO: we should list this as a dependency on the read me
elif args.heatmap:
    x = []
    y = []
    z = []
    count = 0;
    for d in data:
        if d["key"] == "PathWorldClick":
            x.append(d["positional_context"]["x"])
            y.append(d["positional_context"]["y"])
            z.append(d["positional_context"]["z"])
            count += 1
    #pl.plot(x, y, 'ro')
    
    sizeseq = 2
    colorseq = "k"

    fig = pl.figure(1, (5,5), dpi=100)
    ax = Axes3D(fig)
    ax.view_init(20, -45)

    ax.plot3D(x, z, y, 'k.', alpha=.8)

    pl.show();
    
def keysums(filepath):
	output = ""
	jfile = open(filepath,'rb')
	jdata = json.loads(jfile.read())
	key_dict = {}
    for x in data:
        if x["key"] in key_dict:
            key_dict[x["key"]] += 1
        else:
            key_dict[x["key"]] = 1
    output += "\nUnique keys and counts:\n")
    for y in key_dict.keys():
        output += y+", "+str(key_dict[y])
    
#TODO - GUI this thing, or interactive command line
#TODO - Extract logic to functions rather then trigger them on elifs