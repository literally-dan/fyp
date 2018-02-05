#!/bin/python
import re
import socket
import time
from operator import add
from mutators.http import *

MTU = 2**16

#sending back to client
def receive(receive,send,session_function):
    #session = session_function(parent,"hello there")


    manager = http_clientside_data_manager(send,session_function)

    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                break #eof
            recv = receive.recv(length)
            if manager.add_data(recv) == 1:
                #reset
                manager = http_clientside_data_manager(send,session_function)

            #send.send(recv)
        except socket.error as error:
            return


    send.close()



#sending to server
def send(receive,send,session_function):

    manager = http_serverside_data_manager(send,session_function)
    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                break #eof
            recv = receive.recv(length)

            if manager.add_data(recv) == 1:
                #reset
                manager = http_serverside_data_manager(send,session_function)



        except socket.error as error:
            return

    send.close()
