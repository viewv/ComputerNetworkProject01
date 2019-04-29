# Define Escape character: 0x7d
ESC = '7d'
# Define Flag character: 0x7e
FLAG = '7e'


def fill(strHexData):
    i = 0
    strgenerate = []
    while i < len(strHexData):
        byte = strHexData[i:i+2]
        if byte != ESC and byte != FLAG:
            strgenerate.append(byte)
        else:
            strgenerate.append(ESC)
            strgenerate.append(byte)
        i += 2
    strgenerate = ''.join(strgenerate)
    strgenerate = FLAG + strgenerate + FLAG
    return strgenerate


# print(fill('1b7d7d7e7d7d7e23'))
