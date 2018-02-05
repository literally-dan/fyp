class databuffer():
    def __init__(self):
        self.data = bytes()

    def read(self,size):
        if(len(self.data) < size):
            ret = self.data
            self.data = bytes()
        else:
            ret = self.data[:size]
            self.data = self.data[size:]
        return ret

    def write(self,data):
        self.data = self.data + data
