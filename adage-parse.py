import json, sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Transform ADAGE formatted raw JSON data.')
parser.add_argument('-f', metavar='FILE.json', type=str, help='ADAGE API formatted JSON file', required=True)
parser.add_argument('--elem', metavar='FIELD', type=str, help='Field in data (e.g., user_id)', nargs='+')
parser.add_argument('--usersum', action="store_true", help='numeric field(s) summed over a user_id')
parser.add_argument('--totalsum', action="store_true", help='numeric field(s) summed over the entire file')
parser.add_argument('--csvfy', action="store_true", help='turns entire file into CSV (note: 2n for n lines to get all fields)')
parser.add_argument('--userdaytotalcsv', action="store_true", help='create buckets by day csv by user')

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

columns = defaultdict(bool)
if args.csvfy:
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
    #print_columns(columns)
    userdaydict = defaultdict(lambda : defaultdict(lambda : defaultdict(list)))
    for line in data:
        user = line['user_id']
        day = parse_day(line['created_at'])
        for elem in line:
            userdaydict[user][day][elem].append(line[elem])
    for u in userdaydict:
        print u
        for d in userdaydict[u]:
            print d
            for e in userdaydict[u][d]:
                print e,'===>',userdaydict[u][d][e]



elif args.elem:
    searchfields = args.elem

    for elem in data:
        print [elem[x] for x in elem if x in searchfields] 
