#!/bin/python
import sys
from lib.obfuscation import *

LENGTHCHARCOUNT = 4

print("arg1 : page",file=sys.stderr)
print("arg2 : data",file=sys.stderr)

page = readPage(sys.argv[1])

data = open(sys.argv[2],"rb").read()

process = str(data).split("\\n")

length = deobfuscate(page,process,LENGTHCHARCOUNT*8)
real_length = int(length)*8
real_length += LENGTHCHARCOUNT*8

output = deobfuscate(page,process,real_length)
output = output[LENGTHCHARCOUNT:]

print(output.decode('utf-8'))
