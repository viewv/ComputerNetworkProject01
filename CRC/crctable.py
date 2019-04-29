import numpy as np


def init():
    num = 0
    crctable = []
    for num in range(256):
        crc = 0x0000
        crc = crc ^ (num << 8)
        for x in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
        crc &= 0xFFFF
        crctable.append(crc)
        # print(num, hex(crc))
    crctable = np.array(crctable)
    np.save('crctable.npy', crctable)
    print("finish")
