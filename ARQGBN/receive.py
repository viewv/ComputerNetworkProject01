import os
import socket
import errno
import time

import ByteFill.generate as bg
import ByteFill.decode as bd
import CRC.generate as cg
import CRC.verify as cv
from ARQGBN.timeout import timeout


# import CRC.crctable as cc

# cc.init()
# receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# receive_socket.bind(('127.0.0.2', 8888))
# print('Receive UDP bind on 127.0.0.2:8888')


@timeout(2, os.strerror(errno.ETIMEDOUT))
def receive(seq, receive_socket):
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
        # TODO Make hexstr ff as a singal shows that frame is show receiew seq
        if hexseq == 'ff':
            return ['seq', message]
        if int(hexseq, 16) == seq:
            return ['data', message]
    else:
        return None


def sendcheck(seq, receive_socket, target, state=False):
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
    print("Receive crc:", crc)
    frame = bg.fill(hexseq + crc)
    print("Feedback Frame:", frame)
    print("Feedback stop:")
    receive_socket.sendto(frame.encode(), target)


def main(n, receive_socket, target):
    while True:
        hello = receive_socket.recv(1024).decode()
        if len(hello) != 0:
            print("Receive OK!", hello)
            break
    alldata = []
    checkseq = {}
    i = 0
    while i < n:
        try:
            rec = receive(i)
        except Exception as e:
            print("Receive Timeout", e)
            rec = None
        time.sleep(1)
        if rec is None:
            sendcheck(i, receive_socket, target, state=False)
        else:
            print("Rec", rec)
            if rec[0] == 'data':
                alldata.append(rec[1])
                sendcheck(i, receive_socket, target, state=True)
                i += 1
            else:
                pass

    print("All Data:")
    for x in range(len(alldata)):
        print(alldata[x], end=' ')
        if x % 3 == 0:
            print()
    return alldata
