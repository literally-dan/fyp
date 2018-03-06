#!/bin/python
import math

class DatasourceWrapped:

    def __init__(self,data):
        self.data = bytes(str(len(data)) + ":",'utf-8')+ data
        self.bitsdone = 0
        self.length = len(self.data)
        if(self.length > 2):
            pass
          #  self.printbits()

    def bitsleft(self):
        return self.length*8-self.bitsdone

    def getbit(self):
        if(self.bitsdone>=8*self.length):
            return 0
        byte = math.floor(self.bitsdone/8)
        x = ((self.data[byte]&(1<<(self.bitsdone % 8)))!=0);
        self.bitsdone += 1
        out = 1 if x else 0
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

    def printbits(self):
        prevbitsdone = self.bitsdone
        self.bitsdone = 0
        count = self.bitsleft()
        print("{",self.data,"} : ")
        for i in range(0,count):
            print(self.getbit(),end='')

        self.bitsdone = prevbitsdone
        print()

        
            


def test_shuffle():
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

def test_whitespace():
    data = b"this is a testing stringsssssssssssssssssssssssssssssssssssssssssssss\n\n\n\n\nddddddddddddddddddddddd;kasjhdkjahwdkjwahdkjawhd;iuwakhdiuwahd98qwpdh93824vunr983uv39pm45u349-v85muq9p8v6umv9-386yum49p869pq846um495w0[687w45bm967wb945459w67ub5w89,7u85697bu,95687ub-390,7-856,7u-36897ub,=w56,u70=5697uw0=987=94w57=4085b=w9i409s7ioiyu5d[0biyus,[0497i[509disssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssspooooooooooooooooooopppppppppooooooooo{@:@~:~@:LOP){~ $I_)$IO{$PKL${@P$L@:$L@:$L:L$$@KO:K{K}@_~P{I+~{O+~{}{~:}{{}[]][}{{}@}{@}{}{{}}{][p34roije;kj43iopu34598u5fj9pj3459385798798(*&(*&98798&(P*OU(IO*U(*&YIOUhu98YIUOHKJ(*OYIUHKLJn98&UOIHJLK&*()UIOJLK)&(UIOJKL&*()UJIOKL*()UOIJKL)&*(UIOJ)&_P(*)*O&H^*&(*O&^(*&&*("*2200

    print(len(data))

    d = DatasourceWrapped(data)
    print(d.bitsleft())

    ls = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    headers  = []
    headers += [('Host', 'www.cs.bham.ac.uk')]
    headers += [('Connection', 'keep-alive')]
    headers += [('Pragma','no-cache')]
    headers += [('Cache-Control','no-cache')]
    headers += [('Upgrade-Insecure-Requests','1')]
    headers += [('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')]
    headers += [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')]
    headers += [('DNT','1')]
    headers += [('Accept-Encoding','gzip, deflate')]
    headers += [('Accept-Language', 'en-US,en;q=0.9,en-GB;q=0.8')]
    headers += [('Cookie','_ga=GA1.3.1924440076.1506628216')]
    headers += [('Referer','google.com')]
    headers += [('Content-Length','0')]
    headers += [('X-Request-ID','8a5da39b-a61f-44eb-8952-c19ad81f3817')]

    decoder = shuffledecoder("")
    while True:
        output = add_whitespace(headers,d,16)

        done = decoder.add_data(get_whitespace(output))

        output = shuffle(d,ls)

        done = decoder.add_data(unshuffle(output))
        
        if done != "":
            break

    print(decoder.data)


def main():
    test_whitespace()

        
class shuffledecoder:
    def __init__(self,data):
        self.data = data
        self.length = -1
        self.haslength = False
        self.complete = False
        self.check_data()
        self.offset = 0

    def add_data(self, data):
        if self.complete == True:
            return self.data
        self.data += data
        self.check_data()
        return self.convert()
        


    def check_data(self):
        if self.haslength == False:
            offset = self.calc_offset()
            if offset == -1:
                return False
            length = ""
            char = ""
            for i in range(0,math.floor(len(self.data)/8)):
                char = chr(int(self.data[i*8+offset:i*8+8+offset][::-1],2))
                if(char == ":"):
                    self.length = int(length)*8
                    self.haslength = True
                    self.data = self.data[len(length)*8+offset+8:]
                    return True
                length+=char
        return False

    def calc_offset(self):
        end = math.floor(len(self.data)/8)
        if end > 10:
            end = 10
        for offset in range(0,8): #bit offset, note python range doesn't include upper limit
            for charindex in range(0,end): #characters to check though, maximum 10 or len/8-1
                start = charindex*8+offset
                finish = charindex*8+8+offset
                char = chr(int(self.data[start:finish][::-1],2))
                if charindex >= 1:
                    if char == ":":
                        self.offset = offset
                        print(offset)
                        return offset
                if not str.isdigit(char):
                    break

        if(len(self.data) > 80):
            self.data = ""
        return -1




    def convert(self):
        if self.haslength == True:
            if len(self.data) >= self.length:
                data = self.data[:self.length][::-1]
                self.complete = True
                if(self.length > 0):
                    print(self.data)
                self.data = bytes(int(data[i:i+8],2) for i in range (0,self.length,8))[::-1]
        if self.complete == True:
            return self.data
        return ""


def unshuffle(ls):
    if(len(ls) <= 1):
        return ""
    output = ""
    sortedls = sorted(list(set(ls)))
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



def get_whitespace(header_list):
    whitespacedata = ''

    for header in header_list:
        count = len(header[1])-len(header[1].rstrip())
        binary = format(count,'04b')
        whitespacedata += binary[::-1]

    return whitespacedata


def add_whitespace(headers,datasource,count):
    ret = []
    for header in headers:
        left = header[0]
        right = header[1]
        right = right.rstrip()
        num = datasource.gettox(count)
        right = right + (" " * num)
        ret += [(left,right)]

    return ret


if __name__ == "__main__":
    main()

