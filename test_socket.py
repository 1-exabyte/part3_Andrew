import socket
#name a socket and bind it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0",9000))
while True:
    data, addr = sock.recvfrom(65535)
    print("received data from " + str(addr))
    sock.sendto(b"ACK", addr)