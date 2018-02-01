#!/bin/python
import re
import socket
import time
from operator import add
from mutators.http import *

MTU = 2**16

#sending back to client
def receive(receive,send,session_function,parent):
    #session = session_function(parent,"hello there")

    manager = http_clientside_data_manager(send)

    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                break #eof
            recv = receive.recv(length)
            if manager.add_data(recv) == 1:
                #reset
                manager = http_clientside_data_manager(send)

            #send.send(recv)
        except socket.error as error:
            return


    send.close()



#sending to server
def send(receive,send,session_function,parent):

    manager = http_serverside_data_manager(send)
    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                continue
            recv = receive.recv(length)

            if manager.add_data(recv) == 1:
                #reset
                manager = http_serverside_data_manager(send)



        except socket.error as error:
            return

    send.close()
