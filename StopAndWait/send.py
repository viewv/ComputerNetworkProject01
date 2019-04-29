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
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.bind(('127.0.0.1', 8888))
print('Send UDP bind on 127.0.0.1:8888')


@timeout(2, os.strerror(errno.ETIMEDOUT))
def wait(seq):
    while True:
        data = send_socket.recv(1024).decode()
        print("Send wait Trying:", data)
        if len(data) != 0:
            break
    data = bd.decode(data)[0]
    print("Feedback Data:", data)
    if cv.verify(data):
        data = data[:-4]
        state = data[:2]
        hexstr = data[2:]
        print("Data:", data, "State:", state, "Receive Seq:", hexstr, "Need Seq", seq)
        if hexstr == seq and state == '01':
            return True
        else:
            return False
    else:
        return False


def send(message, seq):
    # This data should be a Hex String List
    _FLAG = False
    hexseq = hex(seq)[2:]
    if len(hexseq) == 1:
        hexseq = '0' + hexseq
    print("Send Hex", hexseq)
    message = hexseq + message
    crc = cg.generate(message)
    if len(crc) < 4:
        crc = '0' + crc
    print("Crc", crc)
    frame = bg.fill(message + crc)
    print("Send Frame:", frame)
    send_socket.sendto(frame.encode(), ('127.0.0.2', 8888))
    try:
        _FLAG = wait(hexseq)
    except Exception as e:
        print("Send Timeout!", e)
        _FLAG = False
    if _FLAG is False:
        send(message, seq)
    else:
        return True


def main(data):
    send_socket.sendto('Hello!'.encode(), ('127.0.0.2', 8888))
    n = len(data)
    for x in range(n):
        print("now_frame_to_send", x)
        print("next_frame_to_send", x + 1)
        print("Send Data:", data[x])
        send(data[x], x)
