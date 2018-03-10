#!/bin/python
from threading import Thread
import socket
import sys
from lib.databuffer import *
from time import sleep

MTU = 2048
BUFFERSIZE = MTU*2


def begin_listen(session_function):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(('localhost',44444))
    sl = socket_list()

    sock.listen(5)

    while True:
        (client,address) = sock.accept()
        client.settimeout(300)
        sl.add_socket(client)
        session = session_function[0](session_function[1],session_function[2])
        session.add_data("socket",sl)
        Thread(target=data_rec_thread,args=(client,sock,session_function)).start()

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

            except Exception as e:
                pass

        self.sockets = list(filter(ds,self.sockets))


def data_rec_thread(client,sock,session_function):
    try:
        while True:

            session = session_function[0](session_function[1],session_function[2])

            if(session.get_data("sendbuffer") == ""):
                session.add_data("sendbuffer",databuffer())

            bu = session.get_data("sendbuffer")

            max_data = int(BUFFERSIZE - bu.get_len())


            if(max_data <= BUFFERSIZE/2):
                sleep(0.01)
                continue

            length = len(client.recv(max_data,socket.MSG_PEEK))
            if(length == 0):
                return



            data = client.recv(length)
            session.get_data("sendbuffer").write(data)

    except socket.timeout as e:
        data_rec_thread(client,sock,session_function) # yeah this is probably a bad idea

    except Exception as error:
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

