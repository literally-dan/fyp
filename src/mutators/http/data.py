#!/bin/python
import re
from lib.databuffer import *
from lib.obfuscation import *
from lib.datalistener import *

LENGTHCHARCOUNT = 4

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
    data = session.get_data("sendbuffer").read(2048) #number of bytes to send


    page = readPage("lib/obfuscation/pages/html.pg")
    
    length = len(data)

    zeros = '00000000'

    bitcount = bytes(str((zeros + str(length)))[-LENGTHCHARCOUNT:],'utf-8')

    datasource = Datasource(bitcount + data)

    out = ''

    while datasource.bitsleft() > 0:
        out += walkPageR(page,datasource) + "\n"

    remadestring = body[:match.start()] + match[0] +  bytes(out,'utf-8') + body[match.end():]

    return remadestring
