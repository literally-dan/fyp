#!/bin/python
from threading import Thread
import socket
import sys
from lib.databuffer import *


def begin_listen(session_function):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(('localhost',39806)) #high random port number

    sock.listen(5)

    while True:
        (client,address) = sock.accept()
        client.settimeout(300)
        try:
            while True:
                length = len(client.recv(2**16,socket.MSG_PEEK))
                if(length == 0):
                    break

                data = client.recv(length)

                session = session_function[0](session_function[1],session_function[2])

                if(session.get_data("sendbuffer") == ""):
                    session.add_data("sendbuffer",databuffer())


                session.get_data("sendbuffer").write(data)


            sock.close()
        except socket.error as error:
            print(error)
            return

def get_position(length):
    current = 1
    next = 1

    while(next < length):
        current = next
        next += current*1.2+2
        next += next*1.4 + 2
        next = int(next)

    return current

