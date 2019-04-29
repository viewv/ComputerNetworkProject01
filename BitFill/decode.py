# Define FLAG:01111110 (0x7e)
FLAG = '01111110'


def mergedata(data):
    data = ''.join(data)
    return data


def decode(receive):
    i = 0
    count = 0
    data = []
    allFrame = []
    start = False
    receive = list(receive)
    while i < len(receive):
        bit = receive[i]
        if start is False:
            if bit == '0':
                for x in range(7):
                    if receive[i + 1 + x] == '1':
                        count += 1
                    if receive[i + 1 + x] == '0':
                        if count == 6:
                            start = True
                            count = 0
                            i += 1
                        i += x
                        count = 0
                        break
            i += 1
            continue
        if bit == '1':
            count += 1
        if bit == '0':
            count = 0
        data.append(bit)
        if count == 5:
            if receive[i + 1] == '1':
                for _ in range(6):
                    data.pop()
                allFrame.append(mergedata(data))
                data = []
                start = False
                i += 6
            else:
                i += 1
            count = 0
        i += 1
    return allFrame


# l = decode(
#     '010111010111111010111011111011010110111111010000101101111110101110111110110101101111110')
# print(l[0])
# print(l[1])
# print('101110111111101011')
