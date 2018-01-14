#!/bin/python
import functools
import http_parser
import re
import socket
import time
#from functools import reduce
from http_parser.http import HttpStream
from http_parser.reader import SocketReader
from operator import add

MTU = 2**16

#sending back to client
def receive(receive,send,session_function,parent):
    #session = session_function(parent,"hello there")

    ##chunked test code
    #chunk = http_chunk()
    #chunk.add_data("HELLO".encode('utf-8'))
    #print(chunk.get_whole_data())
    #chunk = http_chunk()
    #chunk.add_data("no way".encode('utf-8'))
    #print(chunk.get_whole_data())
    #chunk = http_chunk()
    #chunk.add_header("Expires","Wed, 21 Oct 2015 07:28:00 GMT")
    #print(chunk.get_whole_data())


    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                continue
            recv = receive.recv(length)

            manager = http_clientside_data_manager()
            manager.add_data(recv)
            manager.get_req_line()

            send.send(recv)
        except socket.error as error:
            print(error)
            return



#sending to server
def send(receive,send,session_function,parent):

    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                continue
            recv = receive.recv(length)

            send.send(recv)
        except socket.error as error:
            print(error)
            return

def insert_data(body,pattern,data):
    result = re.findall(pattern,body)
    length = len(result)
    position = get_position(length)
    print(position)



def get_position(length):
    current = 1
    next = 1

    while(next < length):
        current = next
        next += current*1.2+2
        next += next*1.4 + 2
        next = int(next)

    return current

#this is from data from server->client
class http_clientside_data_manager:
    def __init__(self):
        self.data = bytes()

        self.state = 0
        #0 waiting for req-line
        #1 waiting for rest of headers
        #2 waiting for body
        #3 waiting for chunked encoding
        #4 ended

        self.http = http_header_body() #initialise both of these
        self.chunk = http_chunk()
        self.data = bytes()

    def add_data(self,data):

        response = 1

        while response == 1:
            self.data+=data



    def get_req_line(self):
        nlpos = self.data.find(b'\r\n')
        if nlpos == -1:
            return 0
        reqline = self.data[:nlpos]
        self.data = self.data[2+nlpos:]

        self.http.set_req_line(reqline)

        return 1






class http_chunk:
    def __init__(self):
        self.length = 0
        self.data = bytes()
        self.header = dict()
        self.done = 0

    def update_length(self):
        self.length = len(self.data)

    def update_data(self,data):
        self.data = data
        self.update_length()

    def add_data(self,data):
        self.data = self.data + bytes(data)
        self.update_length()

    def add_header(self,key,value):
        self.header[key] = value

    def is_done(self):
        return self.done

    def get_whole_data(self):
        if(self.length == 0):
            self.done = 1
        out = bytes((hex(self.length)[2:]).encode('utf-8'))
        out += bytes("\r\n".encode('utf-8'))
        out += self.data
        for key,value in self.header.items():
            out += bytes((key + ": " + value + "\r\n").encode('utf-8'))
        out += bytes("\r\n".encode('utf-8'))
        return out

class http_header_body:
    def __init__(self):
        self.chunked = 0
        self.inital_length = 0
        self.current_length = 0
        self.headers = dict()
        self.body = bytes()
        self.req_line = bytes()
        self.complete_body = 0

    def update_header(self,key,value):
        self.headers[key] = value

    def remove_header(self,key):
        del self.headers[key]

    def get_header(self,key):
        return self.headers[key]

    def set_length(self,length):
        self.body_length = length

    def set_chunked(self):
        self.chunked = 1

    def set_notchunked(self):
        self.chunked = 0

    def add_header(self,key,value):
        self.headers[key] = value

    def append_body(self,body):
        self.body += body
        self.update_length()
        if(self.current_length == self.inital_length):
            complete_body = 1

    def update_body(self,body):
        self.body = body
        self.update_length()

    def update_length(self):
        self.current_length = len(body)

    def set_req_line(self, reqline):
        self.req_line = reqline

    def get_whole_data(self):
        out = self.req_line
        out += "\r\n".encode('utf-8')
        if self.chunked == 0:
            self.headers["content-length"] = self.current_length
        for key,value in self.headers.items():
            out += bytes((key + ": " + value + "\r\n").encode('utf-8'))

        out+="\r\n".encode('utf-8')
        out+=self.body

        return out
