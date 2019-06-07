# -*- coding: utf-8 - *-
import os
import sys
import socket
import struct
import select
import time
import errno

# 根据系统设置时钟，我也不知道为什么不同系统不一样，网上是这么说的
# if sys.platform == "win32":
#     timer = time.clock
# else:
#     timer = time.time
# 这里我使用类Unix的设置，也可以引入上面的代码使用

timer = time.time

ICMP_REQ = 8


def checksum(source):
    s = 0
    counto = (len(source) / 2) * 2
    count = 0
    while count < counto:
        val = ord(source[count + 1]) * 256 + ord(source[count])
        s += val
        count += 2
    if counto < len(source):
        s += ord(source[len(source) - 1])

    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)
    ans = ~s
    ans = ans & 0xffff

    ans = ans >> 8 | (ans << 8 & 0xff00)

    return ans


def recv(p_socket, id, timeout):
    timeleft = timeout
    while True:
        start = timer()
        ready = select.select([p_socket], [], [], timeleft)
        longselect = (timer() - start)
        if ready[0] == []:  # 这个时候超时了
            return
        timerecv = timer()
        recPacket, addr = p_socket.recvfrom(1024)
        icmpHeader = recPacket[20:28]
        # 处理得到的icmp包头
        type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )
        if type != 8 and packetID == id:
            bytesInDouble = struct.calcsize("d")
            timesent = struct.unpack("d", recPacket[28: 28 + bytesInDouble])[0]
            return timerecv - timesent

        timeleft = timeleft - timesent
        if timeleft <= 0:
            return


def oneping(p_socket, dest_addr, id):
    dest_addr = socket.gethostbyname(dest_addr)
    p_checksum = 0
    header = struct.pack("bbHHh", ICMP_REQ, 0, p_checksum, id, 1)
    bytesInDouble = struct.calcsize("d")
    data = (192 - bytesInDouble) * "Q"
    data = struct.pack("d", timer()) + data

    p_checksum = checksum(header + data)

    header = struct.pack(
        "bbHHh", ICMP_REQ, 0, socket.htons(p_checksum), id, 1
    )

    packet = header + data
    p_socket.sendto(packet, (dest_addr, 1))


def test(dest_addr, timeout):
    icmp = socket.getprotobyname("icmp")
    try:
        p_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error as error:
        if error.errno == errno.ECONNREFUSED:
            print(os.strerror(error.errno))
        else:
            raise
    p_id = os.getpid() & 0xffff

    oneping(p_socket, dest_addr, p_id)
    delay = recv(p_socket, p_id, timeout)

    p_socket.close()
    return delay


def ping(dest_addr, timeout=2, counter=10):
    for i in range(counter):
        print("ping %s ..." % dest_addr)
        try:
            delay = test(dest_addr, timeout)
        except socket.gaierror as e:
            print("Failed. (timeout within %ssec.)" % timeout)
        else:
            delay = delay * 1000
            print("ping in %0.4fms" % delay)


if __name__ == "__main__":
    dest = sys.argv[1]
    ping(dest)
    # ping("www.baidu.com")
    # ping('10.0.0.1')
