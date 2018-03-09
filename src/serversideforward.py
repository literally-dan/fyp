#!/bin/python
from threading import Thread
import socket
import sys



PORT1 = 44444
PORT2 = 1194
REMOTE1 = "localhost"
REMOTE2 = "localhost"
MTU = 2**16




def main():
    p1 = PORT1
    p2 = PORT2
    r1 = REMOTE1
    r2 = REMOTE2
    arguments = len(sys.argv)
    try:
        if(arguments != 1):
            if(arguments != 2):
                if(arguments != 3):
                    if(arguments != 4):
                        r1 = sys.argv[4]
                    p1 = int(sys.argv[3])
                r2 = sys.argv[2]
            p2 = int(sys.argv[1])
    except:
        print("One of the provided parameters was invalid, using defaults")
        print("Parameters (all optional, defaults shown):")
        print(sys.argv[0])
        print("Remote port2:",PORT2)
        print("Remote host2:",REMOTE2)
        print("Remote port1:",PORT1)
        print("Remote host1:",REMOTE1)

    print("Connecting",r1,":",p1,"to",r2,":",p2)

    s1 = socketwrapper(r1,p1)
    s2 = socketwrapper(r2,p2)

    Thread(target=data_transfer,args=(s1,s2)).start()
    Thread(target=data_transfer,args=(s2,s1)).start()



def data_transfer(send,recieve):

    data = b''

    while(True): 

        print("loop")

        if(data == b''):
            try:
            #get some data
                data = recieve.recv()
                x = len(data)
                print("Got bytes:",x)
            except:
                try:
                    recieve.kill_socket()
                except:
                    pass

                try:
                    recieve.make_conn()
                except:
                    pass
        else:
            try:
            #send some data
                x = send.send(data)
                print("Sent bytes:",x)
                data = b''


            except:
                try:
                    send.kill_socket()
                except:
                    pass

                try:
                    send.make_conn()
                except:
                    pass

class socketwrapper():
    def __init__(self,remote,port):
        self.remote = remote
        self.port = port
        self.make_conn()

    def make_conn(self):
        print("trying to make")
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((self.remote,self.port))
        print("made")

    def send(self,data):
        return self.socket.send(data)

    def kill_socket(self):
        print("trying to kill")
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()
        print("killed")


    def recv(self):
        length = len(self.socket.recv(MTU,socket.MSG_PEEK))
        print("aaa",length)
        if(length == 0):
            raise Exception("socket is dead")
        data = self.socket.recv(length)
        return data



if __name__ == "__main__": main()


