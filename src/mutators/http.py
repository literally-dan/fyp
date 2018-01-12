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
    while True:
        try:
            r = SocketReader(receive)
            p = HttpStream(r)
            headers = p.headers()
            body = p.body_file().read()
            reqline = ("HTTP/" + str(p.version()[0]) + "." + str(p.version()[1]) + " " + str(p.status()))
            request = httprequest(reqline,headers,body)
            #pattern = re.compile("<.*?>")

            #insert_data(str(body),pattern,"poop")

            request.send(send)
        except socket.error as error:
            print("receive1")
            print(error)
            return
        except (StopIteration, http_parser.http.NoMoreData) as error:
            print("recieve2")
            print(error)
            return



#sending to server
def send(receive,send,session_function,parent):
    while True:
        try:
            r = SocketReader(receive)
            p = HttpStream(r)
            headers = p.headers()
            body = p.body_file().read()
#            reqline = (str(p.method() + " " + p.path() + " HTTP/" + str(p.version()[0]) + "." + str(p.version()[1])))

            reqline = (str(p.method() + " " + p.path() + " HTTP/1.0"))

            request = httprequest(reqline,headers,body)
            request.remove_header("Accept-Encoding")
            request.remove_header("Range")
            request.remove_header("If-Range")
            request.remove_header("Referer")
            request.remove_header("Host")
            request.remove_header("ETag")
            request.remove_header("Connection")
            request.remove_header("User-Agent")
            request.remove_header("Accept")
            request.remove_header("Accept-Language")
            request.remove_header("DNT")
            request.remove_header("Pragma")
            request.remove_header("Cache-Control")
            request.remove_header("Connection")
            request.remove_header("Upgrade-Insecure-Requests")


            #request.print()
            request.send(send)
        except socket.error as error:
            print("send1")
            print(error)
            return
        except (StopIteration, http_parser.http.NoMoreData) as error:
            print("send2")
            print(error)
            return

class httprequest:
    def __init__(self,reqline,headers,body):
        self.reqline = reqline
        self.headers = {}
        for (key,value) in headers.items():
            self.headers[key] = value
        self.body = body

    def checklength(self):
        length = len(self.body)
        if length > 0:
            self.headers.update({'Content-Length':length})

    def get_body(self):
        return self.body

    def update_body(self,body):
        self.body = body

    def print(self):
        print(str(self.reqline))
        for (key,value) in self.headers.items():
            headerline = str(key) + ": " + str(value)
            print(headerline)

        print(str(self.body))

    def change_header(self, header, value):
        self.headers[header] = value

    def remove_header(self, header):
        try:
            del self.headers[header]
        except:
            pass


    def send(self,socket):
        self.checklength()
        socket.send(str.encode(self.reqline))
        print(self.reqline)
        socket.send(str.encode("\r\n"))
        for (key,value) in self.headers.items():
            headerline = str(key) + ": " + str(value) + "\r\n"
            socket.send(str.encode(headerline))
            print(str(key) + ": " + str(value))

        socket.send(str.encode("\r\n"))
        socket.send(self.body)
        print()
        print()

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




