# -*- coding: utf-8 - *-
import socket
import struct
import sys
# import io


def trace(dest):
    dest_addr = socket.gethostbyname(dest)
    port = 23144
    max_jump = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        timeout = struct.pack("ll", 5, 0)

        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
        recv_socket.bind(("", port))
        print(" %d " % (ttl), end='')
        send_socket.sendto(bytes("", "utf-8"), (dest, port))
        curr_addr = None
        curr_name = None
        finished = False
        attemp = 3

        while not finished and attemp > 0:
            try:
                _, curr_addr = recv_socket.recvfrom(512)
                finished = True
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except socket.error as error:
                attemp -= 1
                print("* ", end='')

        send_socket.close()
        recv_socket.close()

        if not finished:
            pass

        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
        else:
            curr_host = ""

        print("%s" % (curr_host))
        # sys.stdout.write("%s\n" % (curr_host))

        ttl += 1
        if curr_addr == dest_addr or ttl > max_jump:
            break


if __name__ == "__main__":
    dest = sys.argv[1]
    trace(dest)
