#!/bin/python
from lib.obfuscation import *
import sys

LENGTHCHARCOUNT = 4

print("arg1 = page",file=sys.stderr)
print("arg2 = data file",file=sys.stderr)

page = readPage(sys.argv[1])
data = open(sys.argv[2],"rb").read()

length = len(data)

zeros = '00000000'

bitcount = bytes(str((zeros + str(length)))[-LENGTHCHARCOUNT:],'utf-8')

datasource = Datasource(bitcount + data)

out = ''

while datasource.bitsleft() > 0:
    out += walkPageR(page,datasource) + "\n"


print(out)
