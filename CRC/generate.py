import numpy as np

crctable = np.load("crctable.npy")
crctable = crctable.tolist()


def generate(strHexData):
    if len(strHexData) % 2 != 0:
        strHexData = '0' + strHexData
    crc = 0xffff
    i = 0
    while i < len(strHexData):
        strHexNumber = strHexData[i:i+2]
        intNumber = int(strHexNumber, 16)
        Index = (((crc >> 8) & 0xff) ^ intNumber)
        crc = ((crc << 8) & 0xff00) ^ crctable[Index]
        i += 2
    crc = hex(crc)
    crc = crc[2:]
    return crc


# num = '1b0f1df4433121dfdf123'
#
# if len(num) % 2 != 0:
#     num = '0'+num

# check = generate(num)
# send = num + hex(check)[2:]
# print(generate(num))
# print(send)
# print(generate(send))
#
#
# def formatHex(intNum, lenofHexString):
#     return format(intNum, "0" + str(lenofHexString) + "x")
