# receiver_practice.py -- Member 3 (Andrew Samaha): first practice version of the receiver
# (the finished version is receiver.py)

import socket
import struct
import hashlib


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 9000))

expected=0

buffer={}
chunks=[]
seq=4
end_seq = None

def glue(data):
    chunks.append(data)
    #print("chunk:" + str(chunks))

while True:
    data, addr = sock.recvfrom(65535)
    ptype, seq = struct.unpack("!BI", data[:5])
    payload = data[5:]
    if ptype == 2:
        print("end packet")
        end_seq = seq
        end_hash = payload
    elif seq == expected:
        print("in order")
        glue(payload)
        expected += 1
        while expected in buffer:
            print("took out", expected)
            glue(buffer.pop(expected))
            expected += 1
    elif seq > expected:
        print("put in buffer")
        buffer[seq] = payload
        print(buffer)
    else:
        print("discard")
    print(f"----------------------- ACK {expected} -----------------------")
    sock.sendto(struct.pack("!I", expected), addr)
    if end_seq is not None and expected == end_seq:
        sock.sendto(struct.pack("!I", expected + 1), addr)
        print(chunks)
        ############
        file_data = b"".join(chunks)
        with open("received.txt", "wb") as f:
            f.write(file_data+b"x")
        ############
        with open ("received.txt", "rb") as f:
            data = f.read()
        if hashlib.sha256(data).digest() == end_hash:
            print(":) HASH MATCH")
        else:
            print(":( HASH MISMATCH")

        print("FILE COMPLETE")
        break
print(buffer, expected)
