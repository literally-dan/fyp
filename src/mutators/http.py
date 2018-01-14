#!/bin/python
import functools
import http_parser
import re
import socket
import time
#from functools import reduce
from http_parser.http import HttpStream
from http_parser.reader import SocketReader
from operator import add

MTU = 2**16

#sending back to client
def receive(receive,send,session_function,parent):
    #session = session_function(parent,"hello there")
    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                continue
            recv = receive.recv(length)

            send.send(recv)
        except socket.error as error:
            print(error)
            return



#sending to server
def send(receive,send,session_function,parent):

    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                continue
            recv = receive.recv(length)

            send.send(recv)
        except socket.error as error:
            print(error)
            return

def insert_data(body,pattern,data):
    result = re.findall(pattern,body)
    length = len(result)
    position = get_position(length)
    print(position)



def get_position(length):
    current = 1
    next = 1

    while(next < length):
        current = next
        next += current*1.2+2
        next += next*1.4 + 2
        next = int(next)

    return current




