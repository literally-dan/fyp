#!/bin/python
import re 
import math
from pageparser import *
from datasource import *
from pageclasses import *
from pathlib import Path
import binascii

def readObfsc(filename):
    path = Path(filename)
    if(not path.is_file()):
        return -1

    page = open(filename, "r")
    lines = page.readlines()
    return lines

page = readPage(sys.argv[1])
lines = readObfsc(sys.argv[2])

leaves = []
branches = []
final = []


for token in page.tokens:
    i = 0
    total = len(token.forms)
    length = math.floor(math.log2(total))
    for form in token.forms:
        if(i < 2**length):
            pattern = ""
            for ii in range(1,form.tokencount()+1):
                pattern += "\\" + str(ii)

            if(total == 1):
                replace = "%" + token.name + ":" + pattern + "%"
            else:
                replace = "%" + token.name + ":" + str(format(i, '0'+str(length)+'b'))[::-1]  + pattern + "%"
            find = form.toString()

            if(token.name[0] == "*"):
                final.append((re.compile(find),replace))
            else:
                if(form.tokencount() == 0):
                    leaves.append((re.compile(find),replace))
                else:
                    branches.append((re.compile(find),replace))
        i += 1

for i in range(0,len(lines)):
    lines[i] = lines[i][:-1]

def replaceBranches(branches, line):
    for b in branches:
        line = b[0].sub(b[1],line)
    return line

binary = ""
for line in lines:
    l = line
    subs = []
    for leaf in leaves:
        f = leaf[0].finditer(l)
        for x in f:
            subs.append((x.span()[0],x.span()[1],leaf[1]))

    subs = sorted(subs, key=lambda x:-x[0])
    for s in subs:
        first = l[0:s[0]]
        middle = s[2]
        last = l[s[1]:]
        l = first + middle + last

    prev = ""
    while l != prev:
        prev = l 
        l = replaceBranches(branches,l)

    l = replaceBranches(final,l)
    pos = l.find(":")
    l = l[pos+1:-1]
    binary+=l

length=int(sys.argv[3])
l = binary[:length]
s = l[::-1]
data = bytes(int(s[i : i + 8], 2) for i in range(0, len(s), 8))[::-1]
open('out.bin', 'wb').write(data)


