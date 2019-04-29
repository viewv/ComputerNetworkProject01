import os
import socket
import errno
import ByteFill.generate as bg
import ByteFill.decode as bd
import CRC.generate as cg
import CRC.verify as cv
from StopAndWait.timeout import timeout

# import CRC.crctable as cc

# cc.init()
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.bind(('127.0.0.2', 8888))
print('Receive UDP bind on 127.0.0.2:8888')


@timeout(2, os.strerror(errno.ETIMEDOUT))
def receive(seq):
    while True:
        data = receive_socket.recv(1024).decode()
        print("Receive Trying:", data)
        if len(data) != 0:
            break
    data = bd.decode(data)
    print("Decode:", data)
    data = data[0]
    print("Receive Data:", data)
    if cv.verify(data):
        hexseq = data[:2]
        message = data[2:-4]
        if int(hexseq, 16) == seq:
            return message
    else:
        return None


def sendcheck(seq, state=False):
    print("Feedback Start")
    hexseq = hex(seq)[2:]
    if len(hexseq) == 1:
        hexseq = '0' + hexseq
    print("Hex:", hexseq)
    if state is False:
        hexseq = '00' + hexseq
    else:
        hexseq = '01' + hexseq
    print("State:", hexseq[:2])
    crc = cg.generate(hexseq)
    if len(crc) < 4:
        crc = '0' + crc
    print("crc:", crc)
    frame = bg.fill(hexseq + crc)
    print("Feedback Frame:", frame)
    print("Feedback stop:")
    receive_socket.sendto(frame.encode(), ('127.0.0.1', 8888))


def main(n):
    while True:
        hello = receive_socket.recv(1024).decode()
        if len(hello) != 0:
            print("Receive OK!", hello)
            break
    alldata = []
    i = 0
    while i < n:
        try:
            rec = receive(i)
        except Exception as e:
            print("Receive Timeout", e)
            rec = None
        if rec is None:
            sendcheck(i, state=False)
        else:
            print("Rec", rec)
            alldata.append(rec)
            sendcheck(i, state=True)
            # print(alldata)
            i += 1
    print("All Data:")
    for x in range(len(alldata)):
        print(alldata[x], end=' ')
        if x % 3 == 0:
            print()
    return alldata
