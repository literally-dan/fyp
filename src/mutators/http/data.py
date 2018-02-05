#!/bin/python
import re
from lib.databuffer import *
from lib.obfuscation import *

def insert_data(body,pattern,session_function):

    session = session_function[0](session_function[1],session_function[2])

    if(session.get_data("sendbuffer") == ""):
        session.add_data("sendbuffer",databuffer())


    resultlist = []
    result = re.finditer(pattern,body)
    for x in result:
        resultlist.append(x)

    count = len(resultlist)

    position = get_position(count)
    
    match = resultlist[position]
    data = session.get_data("sendbuffer").read(1024) #number of bytes to send

    output = ""

    datasource = Datasource(data)

    page = readPage("lib/obfuscation/pages/html.pg")
    
    length = datasource.bitsleft()

    zeros = '0000'

    bitcount = str((zeros + str(length)))[-4:]

    secondsource = Datasource(bytes(bitcount,'utf-8'))

    while secondsource.bitsleft() > 0:
        output += walkPageR(page,secondsource)+"\n"

    while datasource.bitsleft() > 0:
        output += walkPageR(page,datasource) + "\n"

    remadestring = body[:match.start()] + match[0] +  bytes(output,'utf-8') + body[match.end():]

    return remadestring

def get_position(length):
    current = 1
    next = 1

    while(next < length):
        current = next
        next += current*1.2+2
        next += next*1.4 + 2
        next = int(next)

    return current
