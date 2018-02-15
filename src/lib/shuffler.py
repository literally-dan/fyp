#!/bin/python
import math

class DatasourceWrapped:

    def __init__(self,data):
        self.data = bytes(str(len(data)) + ":",'utf-8')+ data
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
        out = 1 if x else 0
        #print(out, end='')
        return out

        def gettox(self, x):
            bits = math.floor(math.log2(x))
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



def main():
    data = b"this is a testing string aaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbccccccccccccccccccdddddddddddddeeeeeeeeeefffffffgggggggghhhhhhhiiiiiiiiijjjjjjjjkkkkkkllllllmmmmmmmmmnnnnnnnooooooopppppppqqqqqqrrrrrssssssssttttttttttuuuuuuuuuvvvvvvvwwwwwwwwxxxxxxxxxyyyyyyyyyyzzzzzzzzzzzz"
    d = DatasourceWrapped(data)

    ls = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    done=""
    decoder = shuffledecoder("")
    while True:
        output = shuffle(d,ls)

        done = decoder.add_data(unshuffle(output))
        if done != "":
            break


    print(done)
    print(data)

        
class shuffledecoder:
    def __init__(self,data):
        self.data = data
        self.length = -1
        self.haslength = False
        self.complete = False
        self.check_data()

    def add_data(self, data):
        self.data += data
        self.check_data()
        return self.convert()
        


    def check_data(self):
        if self.haslength == False:
            length = ""
            char = ""
            for i in range(0,math.floor(len(self.data)/8)):
                char = chr(int(self.data[i*8:(i*8)+8][::-1],2))
                if(char == ":"):
                    self.length = int(length)*8
                    self.haslength = True
                    self.data = self.data[len(length)*8:]
                    return True
                length+=char
        return False


    def convert(self):
        if self.haslength == True:
            if len(self.data) >= self.length:
                data = self.data[:self.length][::-1]
                return bytes(int(data[i:i+8],2) for i in range (0,self.length,8))[::-1]

        return ""


def unshuffle(ls):
    if(len(ls) <= 1):
        return ""
    output = ""
    sortedls = sorted(ls)
    pivot = ls.index(sortedls[0])
    leftlist = ls[:pivot]
    rightlist = ls[pivot+1:]
    for x in sortedls[1:]:
        if x in leftlist:
            output+="1"
        else:
            output+="0"

    return output + unshuffle(leftlist) + unshuffle(rightlist)




def shuffle(datasource,ls):
    ls = sorted(list(set(ls))) #sort and remove duplicates
    x = shuffleR(datasource,ls)
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

