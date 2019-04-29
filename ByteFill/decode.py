# Define Escape character: 0x7d
ESC = '7d'
# Define Flag character: 0x7e
FLAG = '7e'


def mergedata(data):
    data = ''.join(data)
    return data


def decode(receive):
    i = 0
    data = []
    allFrame = []
    start = False
    while i < len(receive):
        byte = receive[i:i+2]
        if start is False:
            if byte == FLAG:
                if i == 0:
                    start = True
                elif receive[i-2:i] != ESC:
                    start = True
            i += 2
            continue
        if byte == ESC:
            data.append(receive[i + 2: i + 4])
            i += 2
        elif byte == FLAG:
            start = False
            allFrame.append(mergedata(data))
            data = []
        else:
            data.append(byte)
        i += 2
    return allFrame


# testhex = '7e007f7d7d7d7e1d145677816ee237e'
# print(decode(testhex))
