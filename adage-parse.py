import numbers, json, sys, argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Transform ADAGE formatted raw JSON data.')
parser.add_argument('-f', metavar='FILE.json', type=str, help='ADAGE API formatted JSON file', required=True)
parser.add_argument('--elem', metavar='FIELD', type=str, help='Field in data (e.g., user_id)', nargs='+')
#TODO parser.add_argument('--usersum', action="store_true", help='numeric field(s) summed over a user_id')
#TODO parser.add_argument('--totalsum', action="store_true", help='numeric field(s) summed over the entire file')
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
elif args.elem:
    searchfields = args.elem
    for elem in data:
        print [elem[x] for x in elem if x in searchfields] 
