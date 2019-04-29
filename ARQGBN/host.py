import os
import socket
import errno
# import ByteFill.generate as bg
# import ByteFill.decode as bd
# import CRC.generate as cg
# import CRC.verify as cv
# import CRC.crctable as cc
from ARQGBN.timeout import timeout


class Host:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, addr, port, send_window):
        try:
            self.s.bind((addr, port))
        except Exception as e:
            print("Wrong:", e)
        self.size = send_window
        self.addr = addr
        self.port = port
        # self.recv_window = recv_window
        print('UDP bind on %s:%d' % (addr, port))
