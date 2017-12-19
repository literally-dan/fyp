#!/bin/python
import socket

MTU = 2**16

def client_send(receive,send,session_function,parent):
    session = session_function(parent,"hello there")
    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                continue
            recv = receive.recv(length)
            print("send " + str(length))
            #data = session.get_data("client sent")
            #session.add_data("client sent",data+str(recv))
        except socket.error as error:
            print("Client socket is dead")
            #this is a bad outcome, need to reconnect to server
            return
        try:
            send.send(recv)
        except socket.error as error:
            print("Server has disconnected")
            #this isn't a bad outcome
            return

def client_receive(receive,send,session_function,parent):
    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                continue
            recv = receive.recv(length)
            print("recv " + str(length))
        except socket.error as error:
            print("Server has disconnected")
            return
        try:
            send.send(recv)
        except socket.error as error:
            print("Client has disconnected")
            #this isn't a bad outcome
            return
