import GoBackN.sender as sd
import GoBackN.receiver as re
import socket


class Host:
    def __init__(self, sendnet, recenet, sendfile, recefile):
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_sock.bind(sendnet)
        self.rece_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rece_sock.bind(recenet)
        self.sendfile = sendfile
        self.recefile = recefile

    def send(self):
        RECEIVER_ADDR = ()
        answer = sd.send(self.send_sock, self.sendfile,RECEIVER_ADDR)
        print(answer)
        self.send_sock.close()

    def receive(self):
        answer = re.receive(self.rece_sock,self.recefile)
        print(answer)
        self.rece_sock.close()

