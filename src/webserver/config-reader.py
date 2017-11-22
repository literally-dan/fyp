#!/bin/python
from pathlib import Path
import os
from subprocess import call
import re

class Config:
    supportedprotocols = ['http']

    def __init__(self, path):
        self.path = path
        self.valid = -1

    def parseconfig(self):
        path = Path(self.path)
        if(not path.is_file()):
            return -1

        configfile = open(self.path, "r")
        lines = configfile.readlines();

        config = []
        for x in range(0,len(lines)):
            if(lines[x][0] != '#'):
                config.append(lines[x]);

        for x in range(0,len(config)):
            if config[x][len(config[x])-1] == "\n":
                config[x] = config[x][:-1]
        

        self.url = config[0]
        self.connectport = config[1]
        self.listenport = config[2]
        self.protocol = config[3]

        if self.verifyself() == 0:
            self.valid = 0

        return self.valid

    def verifyself(self):
        total = 0
        total += self.verifyurl(self.url)
        total += self.verifyport(self.connectport, 0)
        total += self.verifyport(self.listenport, 1)
        total += self.verifyprotocol(self.protocol)
        if total == 0:
            return 0
        return 1


    def verifyurl(self, url):
        response = os.system("host " + url + "&>/dev/null")
        if(response !=  0):
            print("Remote host not found")
        return response

    def verifyport(self, port, listen):
        if(port.isdigit()):
            port = int(port)
        else:
            print("Port specified for " + ("listening" if listen == 1 else "connecting")+ " was not a number")
            return 1
        if(port > 65535):
            print("Port specified too high for " + ("listening" if listen == 1 else "connecting") + ".")
            return 1
        if port <= 0:
            print("Port specified too low for "+ ("listening" if listen == 1 else "connecting"      ) + ".")      
            return 1
        return 0

    def verifyprotocol(self, protocol):
        if protocol in self.supportedprotocols:
            return 0
        print("Protocol "+ protocol + " not supported")
        return 1

def main():
    c = Config("config");
    c.parseconfig();
    if(c.valid !=0 ):
        print("Config not valid")
        exit(1)

if __name__ == "__main__": main()
