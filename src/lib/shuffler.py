#!/bin/python
import math
#this should be imported, but python doesn't like imports
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


def main():
    data = b"this is a testing string aaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbccccccccccccccccccdddddddddddddeeeeeeeeeefffffffgggggggghhhhhhhiiiiiiiiijjjjjjjjkkkkkkllllllmmmmmmmmmnnnnnnnooooooopppppppqqqqqqrrrrrssssssssttttttttttuuuuuuuuuvvvvvvvwwwwwwwwxxxxxxxxxyyyyyyyyyyzzzzzzzzzzzz"
    d = Datasource(data)

    ls = ['hello','there','my','name','is','poop','hello','again']
    shuffle(d,ls)

def shuffle(datasource,ls):
    ls = sorted(list(set(ls))) #sort and remove duplicates
    x = shuffleR(datasource,ls)
    print(x)
    return x

def shuffleR(datasource,ls):
    if(len(ls) <= 1):
        return ls
    (right,left) = get_sides(datasource,ls)
    return shuffleR(datasource,right) + [ls[0]] + shuffleR(datasource,left)


def get_sides(datasource,ls):
    ls = ls[1:]

    right = []
    left = []

    for x in ls:
        if(datasource.getbit() == 1):
            right+=[x]
        else:
            left+=[x]

    return(right,left)

if __name__ == "__main__":
    main()

