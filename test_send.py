# test_send.py -- send one test packet to test_socket.py
import socket
#name a socket and bind it to a port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0",8000 ))
sock.sendto(b"hello", ("127.0.0.1", 9000))