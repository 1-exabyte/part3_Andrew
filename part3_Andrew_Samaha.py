import socket
import struct
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 9000))

expected=0

buffer={}
chunks=[]
seq=4


def glue(data):
    chunks.append(data)
    print("chunk:" + str(chunks))

while True:
    data, addr = sock.recvfrom(65535)
    seq = struct.unpack("!I", data[:4])[0]
    payload = data[4:]
    if seq == expected:
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
    print(f"ACK {expected}")
    sock.sendto(struct.pack("!I", expected), addr)

print(buffer, expected)