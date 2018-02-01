import re

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
        insert_data(body,b"<.*?>","poop")
        x = body.decode('utf-8')
        x = x.replace("Lecturer","Legend")
        return x.encode('utf-8')
    return body

def insert_data(body,pattern,data):
    resultlist = []
    result = re.finditer(pattern,body)
    for x in result:
        resultlist.append(x)

    count = len(resultlist)

    position = get_position(count)
    
    match = resultlist[position]

    print(match.start())
    print(match.end())
    print(match)
    remadestring = body[:match.start()] + match[0] + body[match.end():]
    print(body == remadestring)

def get_position(length):
    current = 1
    next = 1

    while(next < length):
        current = next
        next += current*1.2+2
        next += next*1.4 + 2
        next = int(next)

    return current

class databuffer():
    def __init__():
        self.data = bytes()

    def read(size):
        if(len(self.data) < size):
            ret = self.data
            self.data = bytes()
        else:
            ret = self.data[:size]
            self.data = self.data[size:]
        return ret

    def write(data):
        self.data.append(data)
