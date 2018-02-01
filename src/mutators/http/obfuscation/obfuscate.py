#!/bin/python
from pageparser import *
from datasource import *
from pageclasses import *


page = readPage(sys.argv[1])
data = Datasource(sys.argv[2])

while data.bitsleft() > 0:
    print(walkPageR(page, data))
