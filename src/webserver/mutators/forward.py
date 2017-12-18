#!/bin/python
import socket

def send(receive,send):
    while True:
        recv = receive.recv(1)
        send.send(recv)
def receive(receive,send):
    while True:
        recv = receive.recv(1)
        send.send(recv)
