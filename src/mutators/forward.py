#!/bin/python
import socket

def send(receive,send):
    while True:
        recv = receive.recv(1)
        print(recv.decode(), end='',flush=True)
        send.send(recv)
def receive(receive,send):
    while True:
        recv = receive.recv(1)
        print(recv.decode("utf-8","replace"), end='', flush=True)
        send.send(recv)
