#!/bin/python
from threading import Thread
import socket
import pytun

IP = "spectre" #laptop hostname
PORT = 1337


def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((IP,PORT))

    tun = pytun.TunTapDevice(flags=pytun.IFF_TUN|pytun.IFF_NO_PI)
    tun.addr = '10.8.0.2'
    tun.dstaddr = '10.8.0.1'
    tun.netmask = '255.255.255.0'
    tun.mtu = 1500



    tun.up() #the volume

    readthread = threadWrapper(readfunc,tun,server)

    writethread = threadWrapper(writefunc,tun,server)


    readthread.start()
    writethread.start()

class threadWrapper(Thread):
    def __init__(self,function,tun,socket):
        Thread.__init__(self)
        self.exe = function
        self.tun = tun
        self.socket = socket

    def run(self):
        self.exe(self.tun,self.socket)

def readfunc(tun,socket):
    try:
        while True:
            data = tun.read(tun.mtu)
            print(type(data))
            if(len(data) == 0):
                break
            #print("read from tun ", len(data), "bytes")
            socket.send(data)
    except Exception as error:
        print("shit")
        print(error)
        return

def writefunc(tun,socket):
    try:
        while True:
            data = socket.recv(tun.mtu)
            if(len(data) == 0):
                break
            #print("read from socket", len(data), "bytes")
            tun.write(data)
    except Exception as error:
        print("poop")
        print(error)
        return

if __name__ == "__main__": main()
