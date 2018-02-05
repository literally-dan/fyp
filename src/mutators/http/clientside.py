#this is from data from server->client
from mutators.http.httplib import *
class http_clientside_data_manager:
    def __init__(self, socket,session_function):
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
        self.session_function = session_function

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
                        self.http.update_body(change_html(self.http.body,self.http.headers[b'Content-Type'],self.session_function))
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
                    self.chunk.update_data(change_html(self.chunk.data,self.http.headers[b'Content-Type'],self.session_function))


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


