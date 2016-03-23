import socket
import sys
import time
import random

while True:

    r=random.randrange(0,100)
    if r<50:
        a='192.168.0.5'
        b='IPV4 '
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        a='::1'
        b='IPV6 '
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    sock.connect((a, 2545))
    sock.sendall((b+sys.argv[1]).encode())

    time.sleep(2)
    sock.close()
