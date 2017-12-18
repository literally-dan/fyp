#!/bin/python
from pathlib import Path
import os
from subprocess import call
import re
import yaml
import socket

class ServerConfig:
    def __init__(self,path):
        self.isyaml = 0
        self.valid = 0
        if(os.path.exists(path)):
            with open(path, 'r') as stream:
                try:
                    self.yaml = yaml.load(stream)
                    self.isyaml = 1
                    self.check_config()
                except yaml.YAMLError as exc:
                    print(exc)

    def check_config(self):
        if(self.isyaml == 1):
            print("Config for '" + self.yaml['config']['name'] + "' loading...")

            if(check_port(self.yaml['config']['remote-port'],"remote-port") == 0 | check_port(self.yaml['config']['local-port'],"local-port") == 0):
                return 0


            try:
                x = int(self.yaml["config"]["test-response-length"])
            except ValueError:
                print("Response-length in file is not a number")
                return 0

            if("test-response-length-stupid" not in self.yaml["config"]):
                if(self.yaml["config"]["test-response-length"] > 1024):
                    print("Very high response length specified - this is just for the response regex.\nTo allow the program to continue, add the following into the config in the same place as 'test-response-length':\n'test-response-length-stupid: yes'")
                    return 0

            if(conn_check(self.yaml["config"]) == 0):
                return 0

            self.valid = 1
            print("File valid!")
        else:
            print("config file not loaded")

def conn_check(yaml):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((yaml['remote'],yaml['remote-port']))
        if(int(yaml['test-response-length']) ==  0):
            #as no response is needed, don't send anything
            return 1
        s.send(str.encode(yaml['test-request'].replace('\n','\r\n')))
        reply = s.recv(yaml['test-response-length']).decode("utf-8","replace")
        if(not re.match(yaml['test-response'],reply)):
            print("Server sent an invalid response: {}".format(repr(reply)))
            return 0
        s.close()
    except socket.error as exc:
        print("Connection failed: '" + exc + "'")
        return 0

    return 1


def check_port(port_string, descriptor):
    try:
        x = int(port_string)
    except ValueError:
        print(descriptor + " port in file is not a number")
        return 0

    if(port_string < 1 | port_string > 65535):
        print(descriptor + " port is out of range")
        return 0

    return 1
