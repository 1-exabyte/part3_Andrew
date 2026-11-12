# test_send.py -- send one test packet to test_socket.py
import socket
import struct
#name a socket and bind it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0",8000 ))
for n in [0, 2, 3, 1]:
    sock.sendto(struct.pack("!BI", 0, n) + b"data", ("127.0.0.1", 9000))
sock.sendto(struct.pack("!BI", 1, n) + b"dataend", ("127.0.0.1", 9000))
while True:
    data, addr = sock.recvfrom(65535)
    print("received data from " + str(addr)+ str(data))
    