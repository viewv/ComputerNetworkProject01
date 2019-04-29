import multiprocessing
import socket
import ARQGBN.send as send

data = ['7f7d7e1d1456778167', '7f7d7e1d1456778167',
        '7f7d7e1d1456778167', '7f7d7e1d1456765444',
        '7f7d7e1d1456778166', '7f7d7e1d1456778165',
        '7f7d7e1d1456778164', '7f7d7e1d1456778166',
        '7f7d7e1d1456778163', '7f7d7e1d145677816d',
        '7f7d7e1d145677816f', '7f7d7e1d145677816e',
        '7f7d7e1d145677816e', '7f7d7e1d1456778166',
        '7f7d7e1d145677816d', '7f7d7e1d1456778165',
        '7f7d7e1d1456778164', '7f7d7e1d1456778166',
        '7f7d7e1d145677816e', '7f7d7e1d145677816f',
        '7f7d7e1d1456778164', '7f7d7e1d1456778161',
        '7f7d7e1d1456778165', '7f7d7e1d1456778166',
        '7f7d7e1d145677816d', '7f7d7e1d145677816d']


def sim(alldata):
    socket_a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_b = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_a.bind(('127.0.0.1', 8888))
    socket_b.bind(('127.0.0.2', 8888))

    arece = []
    brece = []
    # def main(send_data, recv_data, socket, target, size):
    p1 = multiprocessing.Process(target=send.main,
                                 args=(alldata, arece, socket_a, ('127.0.0.2', 8888), 5))
    p2 = multiprocessing.Process(target=send.main,
                                 args=(alldata, brece, socket_b, ('127.0.0.1', 8888), 5))

    # sr.main(n)
    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Host A:", arece)
    print("Host B:", brece)


try:
    sim(data)
except Exception as e:
    print("Wrong", e)
