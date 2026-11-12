# test_send.py -- send one test packet to test_socket.py
import socket
import struct
#name a socket and bind it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0",8000 ))
#sock.sendto(struct.pack("!BI", 0, 0) + b"hello", ("127.0.0.1", 9000))
#sock.sendto(struct.pack("!BI", 0, 1) + b" my", ("127.0.0.1", 9000))
#sock.sendto(struct.pack("!BI", 0, 2) + b" name", ("127.0.0.1", 9000)) 
#sock.sendto(struct.pack("!BI", 0, 3) + b" is", ("127.0.0.1", 9000))
#sock.sendto(struct.pack("!BI", 0, 4) + b" andrew", ("127.0.0.1", 9000))
#sock.sendto(struct.pack("!BI", 2, 5) + b"dataend", ("127.0.0.1", 9000))
with open ("test_socket.py", "rb") as f:
    data = f.read()
    print(len(data))

while True:
    data, addr = sock.recvfrom(65535)
    print("received data from " + str(addr)+ str(data))
    