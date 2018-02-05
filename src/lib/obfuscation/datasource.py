#!/usr/bin/python
import sys
import math
from pathlib import Path
from . import *
class Datasource:

    def __init__(self,data):
        self.data = data
        self.bitsdone = 0
        self.length = len(self.data)
        #print("Number of bits (you'll need this to decode): " + str(self.bitsleft()), file=sys.stderr)

    def bitsleft(self):
        return self.length*8-self.bitsdone

    def getbit(self):
        if(self.bitsdone>=8*self.length):
            return 0
        byte = math.floor(self.bitsdone/8)
        x = ((self.data[byte]&(1<<(self.bitsdone % 8)))!=0);
        self.bitsdone += 1
        return 1 if x else 0 

    def gettox(self, x):
        bits = math.floor(math.log2(x))
        #print(str(x) + " -> " +  str(bits))
        bitstream = ""
        for i in range(0,bits):
            bit = str(self.getbit())
            bitstream += bit 

        current = 0
        total = 0
        for i in bitstream:
            total+=math.pow(2,current)*int(i)
            current+=1

        return int(total)
