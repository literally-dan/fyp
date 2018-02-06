#!/bin/python
import requests
from lib.datalistener import *
import re
from lib.obfuscation import *

def main():
    pattern = "<.*?>"
    headers = {
        'accept-encoding': 'gzip, deflate, sdch',
        'accept-language': 'en-us,en;q=0.8',
        'user-agent': 'mozilla/5.0 (macintosh; intel mac os x 10_10_1) applewebkit/537.36 (khtml, like gecko) chrome/39.0.2171.95 safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'referer': 'http://www.wikipedia.org/',
        'connection': 'keep-alive',
    }

    response = requests.get('http://localhost', headers=headers).text

    resultlist = []
    result = re.finditer(pattern,response)
    for x in result:
        resultlist.append(x)

    count = len(resultlist)

    positions = []

    while count > 1:
        count = get_position(count)
        positions.append(count)

    page = readPage("lib/obfuscation/pages/html.pg")

    for x in positions:
        get_data(response,x,resultlist,page)




def get_data(data,position,matches,page):
    if(position == 70):
        body = data[matches[position].end():]
        process = body.split("\n")
        length = deobfuscate(page,process,32) #4 characters is 32 bits

        real_length = int(length)

        real_length += 32 #for the length, as we can't calculate how long it was, and it's more efficient to just do it again

        output = deobfuscate(page,process,real_length)


        print(output[4:])



if __name__ == "__main__":
    main()
