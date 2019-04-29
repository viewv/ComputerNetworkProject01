import CRC.generate as cg


def verify(message):
    if cg.generate(message) == '0':
        return True
    else:
        return False


# test = '007f7d7e1d1456778167607e'
# print(verify(test))
