#!/bin/python
import socket
from http_parser.http import HttpStream
from http_parser.reader import SocketReader
import http_parser

MTU = 2**16

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
            request.send(send)
        except socket.error as error:
            print(error)
            return
        except (StopIteration, http_parser.http.NoMoreData):
            continue



def send(receive,send,session_function,parent):
    while True:
        try:
            r = SocketReader(receive)
            p = HttpStream(r)
            headers = p.headers()
            print(headers)
            body = p.body_file().read()
            reqline = (str(p.method() + " " + p.path() + " HTTP/" + str(p.version()[0]) + "." + str(p.version()[1])))
            request = httprequest(reqline,headers,body)
            request.send(send)
        except socket.error as error:
            print(error)
            return
        except (StopIteration, http_parser.http.NoMoreData):
            continue

class httprequest:
    def __init__(self,reqline,headers,body):
        self.reqline = reqline
        self.headers = {}
        for (key,value) in headers.items():
            self.headers[key] = value
        self.body = body
        print(self.headers)

    def checklength(self):
        length = len(self.body)
        self.headers.update({'Content-Length':length})



    def send(self,socket):
        self.checklength()
        socket.send(str.encode(self.reqline))
        socket.send(str.encode("\r\n"))
        for (key,value) in self.headers.items():
            headerline = str(key) + ": " + str(value) + "\r\n"
            print(repr(headerline))
            socket.send(str.encode(headerline))

        socket.send(str.encode("\r\n"))
        socket.send(self.body)
