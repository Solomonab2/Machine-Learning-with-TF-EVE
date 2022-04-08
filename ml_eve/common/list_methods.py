""" reads lists from files and writes lists to files """

def appendListFile(filePath, outList):
    with open(filePath, 'a', encoding='utf-8') as f:
        for items in outList:
            f.write('%s\n' % items)
    f.close()

def writeListFile(filePath, outList):
    with open(filePath, 'w', encoding='utf-8') as f:
        for items in outList:
            f.write('%s\n' % items)
    f.close()

def readListFile(filePath):
    inList = []
    f = open(filePath, 'r', encoding='utf-8')
    for x in f.readlines():
        temp = x.rstrip("\n")
        inList.append(temp)
    return inList

