#!/usr/bin/python
import re

class Token:

    def __init__(self, token):
        self.name = token
        self.forms = []

    def add_form(self, form, tokens):

        f = Form()

        split = form.split("%")

        if split[0] == "":
            split = split[1:]
            split[0] = "%" + split[0]

        for i in range(1,len(split)):
            split[i] = "%"+split[i]

        otokens = sorted(tokens,key= lambda t: -len(t.name)) 


        for s in split:
            found = False
            for t in otokens:
                if ("%" + t.name) in s and not found:
                    f.addpart(t)
                    f.addpart(s.replace("%" + t.name,""))
                    found = True
            if not found:
                f.addpart(s)


        self.forms.append(f)
        return 0

class Form:

    def __init__(self):
        self.formslist = []

    def addpart(self,part):
        if(part == ""):
            return
        self.formslist.append(part)

    def toString(self):
        s = ""
        for f in self.formslist:
            if isinstance(f,str):
                s+=re.escape(f)
            else:
                s+=re.escape("%"+f.name + ":")+"([01]*)" + re.escape("%")
        return s

    def tokencount(self):
        i = 0
        for f in self.formslist:
            if isinstance(f,str):
                i = i
            else:
                i+=1
        return i

class Page:

    def __init__(self):
        self.tokens=[]
        self.basetokens=[]

    def add_base_token(self, token, form):

        t =  self.add_token(token, form)

        self.basetokens.append(t)
        return t

    def add_token(self, token, form):

        for t in self.tokens:
            if t.name == token:
                t.add_form(form,self.tokens)
                return t

        t = Token(token)
        if t.add_form(form,self.tokens) == 0:
            self.tokens.append(t)
            return t

        return -1

