import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 9000))

expected=4

buffer={}
chunks=[]
seq=4


def glue(data):
    chunks.append(data)
    print("chunk:" + str(chunks))


for seq in [4, 5, 6, 7, 8, 15, 16, 9, 10, 11, 12, 13, 14]:
    if seq == expected:
        print("in order")
        glue("data" + str(seq))
        expected += 1
        while expected in buffer:
            print("took out", expected)
            glue(buffer.pop(expected))
            expected += 1
    elif seq > expected:
        print("put in buffer")
        buffer[seq] = "data" + str(seq)
        print(buffer)
    else:
        print("discard")
    print(f"ACK {expected}")

print(buffer, expected)