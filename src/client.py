#!/bin/python
import requests
from lib.datalistener import *
import re
from lib.obfuscation import *
from time import sleep
import sys
from lib.shuffler import *

LENGTHCHARCOUNT = 4
MTU = 150
BUFFERSIZE = MTU * 2

def datacount(ds):
    count = 0;
    for dw in ds:
        count+=dw.bitsleft()/8

    return count

def run(socket_list,data_store):
    pattern = "<.*?>"

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


    if(len(data_store) == 0):
        ds = DatasourceWrapped(b"")
    else:
        ds = data_store[0]
        if(ds.bitsleft() == 0):
            if(len(data_store) > 1):
                data_store.remove(data_store[0])
                ds = data_store[0]
            else:
                ds = DatasourceWrapped(b"")

    left = ds.bitsleft()
    headers = shuffle(ds,headers)

    headers = add_whitespace(headers,ds,64)

    sentdata = left - ds.bitsleft()-16 # this ISN'T a number of bits sent, it's an estimate on whether any was sent for when needing to send more data

    req = requests.Session()
#
    req.headers = listofdicttodict(headers)

    response = req.get(sys.argv[1]).text
    resultlist = []
    result = re.finditer(pattern,response)
    for x in result:
        resultlist.append(x)

    count = len(resultlist)

    positions = []

    while count > 1:
        count = get_position(count)
        positions.append(count)

    page = readPage("lib/obfuscation/pages/html.pg")

    for x in positions:
        if(type(get_data(socket_list,response,x,resultlist,page)) == int):
            return 1
    return sentdata;


def get_data(socket_list,data,position,matches,page):
    try:
        body = data[matches[position].end():]
        process = body.split("\n")
        length = deobfuscate(page,process,LENGTHCHARCOUNT*8) #4 characters is 32 bits

        real_length = int(length)*8

        real_length += LENGTHCHARCOUNT*8 #for the length, as we can't calculate how long it was, and it's more efficient to just do it again

        output = deobfuscate(page,process,real_length)


        output = output[LENGTHCHARCOUNT:]
        if(len(output) > 0):
            socket_list.send(output)
            return len(output)

    except ValueError as e:
        pass

class socket_list:
    def __init__(self):
        self.sockets = []

    def add_socket(self,sock):
        self.sockets += [sock]

    def send(self,data):

        def ds(sock):
            try:
                sock.send(data)
                return True
            except socket.error:
                pass

        self.sockets = list(filter(ds,self.sockets))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(('localhost',33333)) #high random port number

    data_store = []
    sl = socket_list()
    Thread(target=recv_thread,args=(sl,data_store)).start()

    sock.listen(5)
    while True:
        (client,address) = sock.accept() 
        client.settimeout(300)
        sl.add_socket(client)
        Thread(target=send_thread,args=(client,data_store)).start()

def send_thread(socket_obj,data_store):
        try:
            while True:
                max_data = int(BUFFERSIZE - datacount(data_store))
                if(max_data <= BUFFERSIZE/2):
                    sleep(0.01)
                    continue
                length = len(socket_obj.recv(max_data,socket.MSG_PEEK))
                if(length == 0):
                    socket_obj.close()

                recv = socket_obj.recv(length)
                data_store += [DatasourceWrapped(recv)]
                #print(recv)
        except socket.timeout as e:
            send_thread(socket_obj,data_store) #yeah this is probably a bad idea

        except Exception as e:
            print(e)
            return

def recv_thread(socket_list,data_store):
        try:
            while True:
                ret = run(socket_list,data_store)
                if(ret == 0): #if data isn't sent/recv this will be 0
                    sleep(1)
        except Exception as e:
            print(e)
            return

def listofdicttodict(ls):
    dct = {}
    for (key,value) in ls:
        dct[key]=value

    return dct



if __name__ == "__main__":
    main()


