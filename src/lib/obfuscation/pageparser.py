#!/usr/bin/python
import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**31,-1))
sys.setrecursionlimit(10**9)
import random
from . import *
from pathlib import Path

def readPage(filename):
    path = Path(filename)
    if(not path.is_file()):
        return -1
    page = open(filename, "r")
    lines = page.readlines()

    if(lines[0] != "PAGE#0.1\n"):
        return -2

    expressions = []

    for x in range(1,len(lines)):
        if lines[x][0] != "#" and lines[x] != "\n":
            if lines[x][-1:] == "\n":
                expressions.append(lines[x][:-1])
            else:
                return -3

    if not "DELIM" in expressions[0]:
        return -4
    delim = expressions[0][6:]

    if delim == "":
        return -5

    expressions = expressions[1:]
    page = pageclasses.Page()


    for x in range(0,len(expressions)):
        expressions[x] = breakapart(delim,expressions[x])
    
    for x in range(0,len(expressions)):
        if expressions[x][1][0] == " ":
            expressions[x][1] = expressions[x][1][1:]

        if expressions[x][0][-1:] == " ":
            expressions[x][0] = expressions[x][0][:-1]

        if "%" in expressions[x][0]:
            return -6

        if expressions[x][0][0] != "*" : 
            page.add_token(expressions[x][0], expressions[x][1])
        else:
            page.add_base_token(expressions[x][0],expressions[x][1])

    return page 

def breakapart(delim, string):
    return string.split(delim,1)

def walkPageR(page,datasource):
    x = len(page.basetokens)
    num = random.randint(0,x-1)
    return walkTokenR(page.basetokens[num],datasource)
def walkTokenR(token,datasource):
    count = len(token.forms)
    if count == 1:
        form = token.forms[0]
    else:
        form = token.forms[datasource.gettox(count)]
    output = ""
    for f in form.formslist:
        if(isinstance(f,str)):
            output += f
        else:
            output+=walkTokenR(f,datasource)

    return output
