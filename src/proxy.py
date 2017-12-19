#!/bin/python
import configreader
import imp
import os
from threading import Thread
import socket
import sys
import time

class session_database:
    def __init__(self):
        self.dictionary = {}

    def get(self,identifier):
        if identifier in self.dictionary:
            return self.dictionary[identifier]
        else:
            self.dictionary[identifier] = session()
            return self.dictionary[identifier]

    def check(self):
        keys =  list(self.dictionary.keys())
        for identifier in keys:
            max_age = 30
            if(self.dictionary[identifier].get_time() + max_age < time.clock()):
                del self.dictionary[identifier]


class session:
    def __init__(self):
        self.data = {}
        self.update_time()

    def get_time(self):
        return self.last_access

    def add_data(self,key,value):
        self.update_time()
        self.data[key] = value

    def update_time(self):
        self.last_access = time.clock()

    def get_data(self, key):
        self.update_time()
        if(key in self.data):
            return self.data[key]
        else:
            self.data[key] = ""
            return self.data[key]



class threadWrapper(Thread):
    def __init__(self,function,receive,send,session_function,parent):
        Thread.__init__(self)
        self.exe = function
        self.receive = receive
        self.send = send
        self.session_function = session_function
        self.parent = parent

    def run(self):
        self.exe(self.receive,self.send,self.session_function,self.parent)
        self.receive.close()
        self.send.close()

class ProxyServer:
    def __init__(self,config):
        self.config = config
        self.remote_host = config["remote"]
        self.remote_port = config["remote-port"]
        self.local_port = config["local-port"]
        self.session_database = session_database()

        self.listeningsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listeningsocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.listeningsocket.bind(('',self.local_port))

    def init_listen(self):
        self.listeningsocket.listen(5)
        while True:
            client,address = self.listeningsocket.accept()
            client.settimeout(300)
            Thread(target=self.proxythread,args = (client,address,self.remote_host,self.remote_port)).start()
            self.session_database.check()


    def proxythread(self,client,address,remote_host,remote_port):
        print("connect to '" + remote_host + ":" + str(remote_port) + "'")
        filepath = self.config["proxy-mutator-location"]
        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
        mutator = imp.load_source(mod_name, filepath)
        send = getattr(mutator,self.config["proxy-mutate-send"])
        receive = getattr(mutator,self.config["proxy-mutate-receive"])
        session_function = getattr(ProxyServer,"data_fetch")
        connectsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connectsocket.connect((self.remote_host,self.remote_port))


        sendthread = threadWrapper(send,client,connectsocket,session_function,self)
        recievethread = threadWrapper(receive,connectsocket,client,session_function,self)
        recievethread.start()
        sendthread.start()


        if recievethread.isAlive():
            recievethread.join()
        if sendthread.isAlive():
            sendthread.join()

        print("all closed")


    def data_fetch(self,identifier):
        return self.session_database.get(identifier)

def main():
    c = configreader.ServerConfig(sys.argv[1])
    ps = ProxyServer(c.yaml["config"])
    ps.init_listen()

if __name__ == "__main__": main()
