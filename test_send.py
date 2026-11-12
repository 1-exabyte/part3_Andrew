# test_send.py -- send one test packet to test_socket.py
import socket
import struct
import hashlib
#name a socket and bind it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0",8000 ))
#sock.sendto(struct.pack("!BI", 0, 0) + b"hello", ("127.0.0.1", 9000))
#sock.sendto(struct.pack("!BI", 0, 1) + b" my", ("127.0.0.1", 9000))
#sock.sendto(struct.pack("!BI", 0, 2) + b" name", ("127.0.0.1", 9000)) 
#sock.sendto(struct.pack("!BI", 0, 3) + b" is", ("127.0.0.1", 9000))
#sock.sendto(struct.pack("!BI", 0, 4) + b" andrew", ("127.0.0.1", 9000))
#sock.sendto(struct.pack("!BI", 2, 5) + b"dataend", ("127.0.0.1", 9000))
chunksize = 150
with open ("test_send.py", "rb") as f:
    data = f.read()
    print(len(data))
    for i in range(0, len(data), chunksize):
        chunk = data[i:i+chunksize]
        print(i, chunk)
        sock.sendto(struct.pack("!BI", 0, i//chunksize) + chunk, ("127.0.0.1", 9000))
    sock.sendto(struct.pack("!BI", 2, i // chunksize + 1)+hashlib.sha256(data).digest(), ("127.0.0.1", 9000))

while True:
    data, addr = sock.recvfrom(65535)
    print("received data from " + str(addr)+ str(data))
    