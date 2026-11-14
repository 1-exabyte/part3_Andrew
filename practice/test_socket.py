# test_socket.py -- Member 3 practice: receive one packet on port 9000 and reply "ACK"

import socket
import struct
#name a socket and bind it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0",9000))
while True:
    data, addr = sock.recvfrom(65535)
    seq = struct.unpack("!I", data[:4])[0]
    payload = data[4:]
    print(seq, payload)
    sock.sendto(b"ACK", addr)
