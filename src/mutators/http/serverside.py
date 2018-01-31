#this is for data from client->server
from mutators.http.httplib import *
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