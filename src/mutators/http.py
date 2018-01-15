#!/bin/python
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

    manager = http_clientside_data_manager(send)

    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                break #eof
            recv = receive.recv(length)
            if manager.add_data(recv) == 1:
                #reset
                manager = http_clientside_data_manager(send)

            #send.send(recv)
        except socket.error as error:
            return


    send.close()



#sending to server
def send(receive,send,session_function,parent):

    manager = http_serverside_data_manager(send)
    while True:
        try:
            length = len(receive.recv(MTU,socket.MSG_PEEK))
            if(length == 0):
                continue
            recv = receive.recv(length)

            if manager.add_data(recv) == 1:
                #reset
                manager = http_serverside_data_manager(send)



        except socket.error as error:
            return

    send.close()

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

#this is for data from client->server
class http_serverside_data_manager:

    def __init__(self, socket):
        self.socket = socket
        self.data = bytes()

        self.state = 0
        #0 waiting for req-line
        #1 waiting for rest of headers
        #2 waiting for body
        #3 ended

        self.http = http_header_body() #initialise both of these
        self.data = bytes()

    def add_data(self,data):

        response = 1
        self.data+=data

        while response != 0:
            response = 0

            if self.state == 0:
                response = self.get_req_line()

            if self.state == 1:
                response = self.get_headers()
                response = self.get_body()

            if self.state == 3:
                self.make_changes()
                self.http.send(self.socket)
                return 1

        return 0

    def make_changes(self):
        self.http.update_header(b"Accept-Encoding",b"None")

    def get_headers(self):

        nlpos = self.data.find(b'\r\n')
        while nlpos != -1:
            header = self.data[:nlpos]
            if(len(header) == 0):
                self.data = self.data[nlpos+2:]
                self.state = 2
                return 1
            colonpos = self.data.find(b':')
            if colonpos != -1:
                key = header[:colonpos]
                value = header[colonpos+2:]
                if len(key) > 0 and len(value) > 0:
                    self.http.add_header(key,value)
                    self.data = self.data[nlpos+2:]
                else:
                    return 0

            else:
                return 0

            nlpos = self.data.find(b'\r\n')

        return 0

    def get_body(self):
        if b'Content-Length' in self.http.headers:
            hlength = int(self.http.headers[b'Content-Length'].decode('utf-8'))
            dlength = len(self.data)

            blength = len(self.http.body)

            llength = hlength - blength

            if llength > dlength:
                self.http.append_body(self.data)
                self.data = bytes()
                return 0
            else:
                postdata = self.data[:llength]
                self.data = self.data[llength:]
                self.http.append_body(postdata)
                self.state = 3
                return 1

        self.state = 3
        return 1

    def get_req_line(self):
        nlpos = self.data.find(b'\r\n')
        if nlpos == -1:
            return 0

        reqline = self.data[:nlpos]
        self.data = self.data[2+nlpos:]

        self.http.set_req_line(reqline)

        self.state = 1
        return 1



#this is from data from server->client
class http_clientside_data_manager:
    def __init__(self, socket):
        self.socket = socket 
        self.data = bytes()

        self.state = 0
        #0 waiting for req-line
        #1 waiting for rest of headers
        #2 chunked or body
        #3 waiting for body
        #4 waiting for chunked encoding
        #5 ended

        self.http = http_header_body() #initialise both of these
        self.chunk = http_chunk()
        self.data = bytes()

    def add_data(self,data):

        response = 1
        self.data+=data

        while response != 0:
            response = 0

            if self.state == 0:
                response = self.get_req_line()

            if self.state == 1:
                response = self.get_headers()

            if self.state == 2:
                response = self.chunkedornormal()
                self.make_changes()

            if self.state == 3:
                response = self.get_body()

            if self.state == 4:
                response = self.get_chunks()

            if self.state == 5:
                return 1

        return 0

    def make_changes(self):
        self.http.update_header(b"Accept-Ranges",b"none")


    def chunkedornormal(self):

        if b'Transfer-Encoding' in self.http.headers:
            if self.http.headers[b'Transfer-Encoding'] == b'chunked':
                self.state = 4
                self.http.chunked = 1
                self.http.send(self.socket)
                return 1

        self.state = 3
        return 1


    def get_headers(self):

        nlpos = self.data.find(b'\r\n')
        while nlpos != -1:
            header = self.data[:nlpos]
            if(len(header) == 0):
                self.data = self.data[nlpos+2:]
                self.state = 2
                return 1
            colonpos = self.data.find(b':')
            if colonpos != -1:
                key = header[:colonpos]
                value = header[colonpos+2:]
                if len(key) > 0 and len(value) > 0:
                    self.http.add_header(key,value)
                    self.data = self.data[nlpos+2:]
                else:
                    return 0

            else:
                return 0

            nlpos = self.data.find(b'\r\n')

        return 0

    def get_body(self):
        if b'Content-Length' in self.http.headers:
            hlength = int(self.http.headers[b'Content-Length'].decode('utf-8'))
            dlength = len(self.data)

            blength = len(self.http.body)

            llength = hlength - blength

            if llength > dlength:
                self.http.append_body(self.data)
                self.data = bytes()
                return 0
            else:
                postdata = self.data[:llength]
                self.data = self.data[llength:]
                self.http.append_body(postdata)

                if len(self.http.body) > 0:
                    if b'Content-Type' in self.http.headers:
                        self.http.update_body(change_html(self.http.body,self.http.headers[b'Content-Type']))
                self.state = 5
                self.http.send(self.socket)
                return 1

        self.state = 5
        return 1

    def get_chunks(self):
        if self.chunk.length == -1:
            location = self.data.find(b'\r\n')
            if location == -1:
                return 0

            hexlength = self.data[:location]
            offset = len(hexlength) + 2
            try:
                length = int(hexlength.decode('utf-8'),16)
            except:
                length = 0

            self.chunk.update_length(length)
            self.data = self.data[offset:]


        hlength = self.chunk.length
        dlength = len(self.data)

        blength = len(self.chunk.data)

        llength = hlength - blength

        if llength > dlength:
            self.chunk.add_data(self.data)
            self.data = bytes()
            return 0
        else:
            postdata = self.data[:llength]
            self.data = self.data[llength:]
            self.chunk.add_data(postdata)
            if(self.chunk.length > 0):
                if b'Content-Type' in self.http.headers:
                    self.chunk.update_data(change_html(self.chunk.data,self.http.headers[b'Content-Type']))


            self.chunk.send(self.socket)
            self.data = self.data[2:] #get rid of the \r\n
            if(self.chunk.length == 0):
                self.state = 5
                return 1
                
            self.chunk = http_chunk()
            return 1

        

    def get_req_line(self):
        nlpos = self.data.find(b'\r\n')
        if nlpos == -1:
            return 0

        reqline = self.data[:nlpos]
        initial = self.data.find(b'HTTP')
        reqline = reqline[initial:]


        self.data = self.data[2+nlpos:]

        self.http.set_req_line(reqline)

        self.state = 1
        return 1






class http_chunk:
    def __init__(self):
        self.length = -1
        self.data = bytes()
        self.header = dict()
        self.done = 0

    def update_length(self,length):
        self.length = length

    def check_length(self):
        self.length = len(self.data)

    def update_data(self,data):
        self.data = data
        self.update_length(len(self.data))

    def add_data(self,data):
        self.data = self.data + data
        if(len(self.data) > self.length):
            self.check_length()

    def add_header(self,key,value):
        key = key.title()
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

    def send(self,socket):
        data = self.get_whole_data()
        length = len(data)
        sent = 0
        while(sent < length):
            i = socket.send(data)
            sent+=i
            data = data[i:]



class http_header_body:
    def __init__(self):
        self.chunked = 0
        self.inital_length = 0
        self.current_length = 0
        self.headers = dict()
        self.body = bytes()
        self.req_line = bytes()
        self.complete_body = 0

    def print_headers(self):
        print(self.req_line.decode('utf-8'))
        
        for key,value in self.headers.items():
            print((key + b": " + value).decode('utf-8'))

        print("#####")

    def send(self,socket):
        data = self.get_whole_data()
        length = len(data)
        sent = 0
        while(sent < length):
            i = socket.send(data)
            sent+=i
            data = data[i:]
        
    def update_header(self,key,value):
        self.headers[key] = value

    def remove_header(self,key):
        del self.headers[key]

    def get_header(self,key):
        return self.headers[key]

    def set_length(self,length):
        self.body_length = length

    def add_header(self,key,value):
        key = key.title()
        self.headers[key] = value

    def append_body(self,body):
        self.body += body
        if(self.current_length == self.inital_length):
            complete_body = 1

    def update_body(self,body):
        self.body = body
        try:
            self.update_length()
        except:
            pass

    def update_length(self):
        self.current_length = len(self.body)

    def set_req_line(self, reqline):
        self.req_line = reqline

    def get_whole_data(self):
        out = self.req_line
        out += bytes("\r\n".encode('utf-8'))
        if self.chunked == 0:
            self.headers[b"Content-Length"] = bytes(str(self.current_length),'utf-8')
        for key,value in self.headers.items():
            out += key + ": ".encode('utf-8') + value + "\r\n".encode('utf-8')

        out+="\r\n".encode('utf-8')
        out+=self.body
        return out 

def change_html(body,contenttype):
    if 'text/html' in contenttype.decode('utf-8'):
        x = body.decode('utf-8').replace("Computer","shitty old broken boxes")
        x = x.replace("Lecturer","Legend")
        return x.encode('utf-8')
    return body
