import GoBackN.packet as packet
# import socket
# import sys
import GoBackN.filter as udt
import CRC.verify as cv

# RECEIVER_ADDR = ('localhost', 8080)


# Receive packets from the sender
def receive(sock, filename):
    # Open the file for writing
    try:
        file = open(filename, 'wb')
    except IOError:
        print('Unable to open', filename)
        return

    expected_num = 0
    while True:
        # Get the next packet from the sender
        pkt, addr = udt.recv(sock)
        if not pkt:
            break
        seq_num, data = packet.extract(pkt)
        if cv.verify(data):
            print('Got packet', seq_num)

        # Send back an ACK
        if seq_num == expected_num:
            print('Got expected packet')
            print('Sending ACK', expected_num)
            pkt = packet.make(expected_num)
            udt.send(pkt, sock, addr)
            expected_num += 1
            if cv.verify(data):
                print(data[:-4])
                file.write(data)
        else:
            print('Sending ACK', expected_num - 1)
            pkt = packet.make(expected_num - 1)
            udt.send(pkt, sock, addr)

    file.close()
    return "Finish"


# # Main function
# if __name__ == '__main__':
#     if len(sys.argv) != 2:
#         print('Expected filename as command line argument')
#         exit()
#
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind(RECEIVER_ADDR)
#     filename = sys.argv[1]
#     receive(sock, filename)
#     sock.close()