#!/bin/python
import configreader
import imp
import os
import threading
import socket
import sys

class ProxyServer:
    def __init__(self,config):
        self.config = config
        self.remote_host = config["remote"]
        self.remote_port = config["remote-port"]
        self.local_port = config["local-port"]

        self.listeningsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listeningsocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.listeningsocket.bind(('',self.local_port))

    def init_listen(self):
        self.listeningsocket.listen(5)
        while True:
            client,address = self.listeningsocket.accept()
            client.settimeout(30)
            threading.Thread(target=self.proxythread,args = (client,address,self.remote_host,self.remote_port)).start()


    def proxythread(self,client,address,remote_host,remote_port):
        print("connect to '" + remote_host + ":" + str(remote_port) + "'")
        filepath = self.config["proxy-mutator-location"]
        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
        mutator = imp.load_source(mod_name, filepath)
        send = getattr(mutator,self.config["proxy-mutate-send"])
        receive = getattr(mutator,self.config["proxy-mutate-receive"])
        connectsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connectsocket.connect((self.remote_host,self.remote_port))

        threading.Thread(target=send,args=(client,connectsocket)).start()
        threading.Thread(target=receive,args=(connectsocket,client)).start()



def main():
    c = configreader.ServerConfig(sys.argv[1])
    ps = ProxyServer(c.yaml["config"])
    ps.init_listen()

if __name__ == "__main__": main()
