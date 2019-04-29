# Define FLAG:01111110 (0x7e)
FLAG = '01111110'


def generate(strData):
    i = 0
    count = 0
    data = []
    strData = list(strData)
    while i < len(strData):
        bit = strData[i]
        if bit == '1':
            count += 1
        if bit == '0':
            count = 0
        data.append(bit)
        if count == 5:
            data.append('0')
        i += 1
    data = ''.join(data)
    data = FLAG + data + FLAG
    return data


# print(generate('101110111111101011'))
