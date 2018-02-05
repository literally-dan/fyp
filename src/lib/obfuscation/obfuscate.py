#!/bin/python
def main():
    path = Path(sys.argv[2])
    if(not path.is_file()):
        print("Second argument is not a file")
        return -1


    path = Path(sys.argv[1])
    if(not path.is_file()):
        print("First argument is not a file")
        return -1

    with open(sys.argv[2], 'rb') as datafile:
         datacontents = datafile.read()

    data = Datasource(datacontents)

    page = readPage(sys.argv[1])

    while data.bitsleft() > 0:
        print(walkPageR(page, data))

if __name__ == "__main__":
    main()
