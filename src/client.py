#!/bin/python
import requests
from lib.datalistener import *
import re
from lib.obfuscation import *
from time import sleep

LENGTHCHARCOUNT = 4

def run(socket):
    pattern = "<.*?>"
    headers = {
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'en-us,en;q=0.8',
            'user-agent': 'mozilla/5.0 (macintosh; intel mac os x 10_10_1) applewebkit/537.36 (khtml, like gecko) chrome/39.0.2171.95 safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'referer': 'http://www.wikipedia.org/',
            'connection': 'keep-alive',
            }

    response = requests.get('http://localhost', headers=headers).text

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
        if(type(get_data(socket,response,x,resultlist,page)) == int):
            return 0;
    return 1;


def get_data(socket,data,position,matches,page):
    try:
        body = data[matches[position].end():]
        process = body.split("\n")
        length = deobfuscate(page,process,LENGTHCHARCOUNT*8) #4 characters is 32 bits

        real_length = int(length)*8

        real_length += LENGTHCHARCOUNT*8 #for the length, as we can't calculate how long it was, and it's more efficient to just do it again

        output = deobfuscate(page,process,real_length)


        output = output[LENGTHCHARCOUNT:]
        if(len(output) > 0):
            socket.send(output)
            return len(output)

    except ValueError as e:
        pass

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(('localhost',33333)) #high random port number

    sock.listen(5)
    while True:
        (client,address) = sock.accept() 
        client.settimeout(300)
        Thread(target=recv_thread,args=(client,)).start()

def recv_thread(socket):
        try:
            while True:
                ret = run(socket)
                if(ret != 0):
                    sleep(1)
        except:
            return

if __name__ == "__main__":
    main()
