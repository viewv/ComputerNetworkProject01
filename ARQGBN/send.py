import os
import errno
import ByteFill.generate as bg
import ByteFill.decode as bd
import CRC.generate as cg
import CRC.verify as cv
from ARQGBN.timeout import timeout


# import CRC.crctable as cc

# cc.init()
# send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# send_socket.bind(('127.0.0.1', 8888))
# print('Send UDP bind on 127.0.0.1:8888')


def send(data, seq, flag, send_socket, target):
    hexseq = hex(seq)[2:]
    if len(hexseq) == 1:
        hexseq = '0' + hexseq
    print("Send Hex", hexseq, "Send FLAG", flag)
    message = flag + hexseq + data
    crc = cg.generate(message)
    if len(crc) < 4:
        crc = '0' + crc
    print("Send crc", crc)
    frame = bg.fill(message + crc)
    print("Send Frame:", frame)
    send_socket.sendto(frame.encode(), target)


# @timeout(2, os.strerror(errno.ETIMEDOUT))
def receive(seq, receive_socket):
    while True:
        data = receive_socket.recv(1024).decode()
        print("Receive Trying:", data)
        if len(data) != 0:
            break
    print(data)
    data = bd.decode(data)
    print("Receive Data:", data)
    data = data[0]
    if cv.verify(data):
        flag = data[:2]
        hexseq = data[2:4]
        message = data[4:-4]
        if int(hexseq, 16) == seq:
            return [message, int(hexseq, 16), flag]
        else:
            return [message, int('ff', 16), flag]
    return None


def main(send_data, recv_data, socket, target, size):
    # target should be a set like ('127.0.0.2', 8888)
    send(send_data[0], 0, '00', socket, target)
    socket.sendto(send_data[0].encode(), target)
    # send_socket.sendto('Hello!'.encode(), ('127.0.0.2', 8888))
    n = len(send_data)
    i = 1
    while i < n:
        stop = 0
        for x in range(size):
            recv = receive(x, socket)
            if recv is None:
                flag = 'ff'
            else:
                if recv == 'ff':
                    flag = 'ff'
                    stop = int(recv[2], 16)
                else:
                    message = recv[0]
                    flag = recv[2]
                    recv_data.append(message)
                    print("Receive Message", message)
                    stop = x
            if x + i >= n:
                return recv_data
            send(send_data[i + x], x, flag, socket, target)
        i += stop
    return recv_data
