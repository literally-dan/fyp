#!/bin/python
import socket

def send(receive,send,session_function):
    while True:
        recv = receive.recv(1)
        send.send(str.encode("'" + (recv).decode() + "' -> you got MiTM\n"))
def receive(receive,send,session_function):
    while True:
        recv = receive.recv(1)
        send.send(str.encode("'" + (recv).decode() + "' -> And on the way back?!\n"))
