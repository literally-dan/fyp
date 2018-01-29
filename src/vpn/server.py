#!/bin/python
from threading import Thread
import socket
import pytun
import traceback

PORT = 1337

def main():

    listeningsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningsocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    listeningsocket.bind(('',PORT))

    listeningsocket.listen(5)
    tun = pytun.TunTapDevice(flags=pytun.IFF_TUN|pytun.IFF_NO_PI,name='tap0')
    tun.mtu = 1500

    print(tun.name)
    tun.persist(True)
    tun.addr = '10.8.0.1'
    tun.netmask = '255.255.255.0'

    tun.up() #the volume

    while True:
        client,address = listeningsocket.accept()
        client.settimeout(300)

        Thread(target=serverthread,args=(client,address,tun)).start()

def serverthread(client,address,tun):
    print("Received connection from "+ str(address[0]) + " on " + str(address[1]))
    try:


        readthread = threadWrapper(readfunc,tun,client)

        writethread = threadWrapper(writefunc,tun,client)


        readthread.start()
        writethread.start()

    except Exception as error:
        print("shitty")
        print(error)
        return


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
            print(data)
            if(len(data) == 0):
                break
            #print("read from tun ", len(data), "bytes")
            socket.send(data)
    except Exception as error:
        print("bugger")
        print(error)
        return

def writefunc(tun,socket):
    try:
        while True:
            print("banana?")
            data = socket.recv(tun.mtu)
            print(len(data))
            print(type(data))
            print(data)
            if(len(data) == 0):
                break
            print("read from socket", len(data), "bytes")
            tun.write(data)
            print("writ")
    except Exception as error:
        print("###sausage rolls")
        print(error)
        traceback.print_exc()
        return

if __name__ == "__main__": main()
