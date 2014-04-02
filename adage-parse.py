import json, sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Transform ADAGE formatted raw JSON data.')
parser.add_argument('-f', metavar='FILE.json', type=str, help='ADAGE API formatted JSON file', required=True)
parser.add_argument('--elem', metavar='FIELD', type=str, help='Field in data (e.g., user_id)', nargs='+')
parser.add_argument('--usersum', action="store_true", help='numeric field(s) summed over a user_id')
parser.add_argument('--totalsum', action="store_true", help='numeric field(s) summed over the entire file')
parser.add_argument('--csvfy', action="store_true", help='turns entire file into CSV (note: 2n for n lines to get all fields)')
args = parser.parse_args()

jsonfile = open(args.f,'rb')
data = json.loads(jsonfile.read())

if args.csvfy:
    columns = defaultdict(bool)
    for line in data:
        for col in line:
            columns[col] = True
    for col in sorted(columns):
        print col,',',
    print ''
    for line in data:
        lineout = defaultdict(str)
        outputlist = []
        for elem in line:
            lineout[elem] = line[elem]
        for col in sorted(columns):
            outputlist.append(str(lineout[col]))
        print "\"",'","'.join(outputlist),"\""

elif args.fields:
    searchfields = args.fields

    for elem in data:
        print [elem[x] for x in elem if x in searchfields] 
