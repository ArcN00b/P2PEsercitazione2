import socket
import sys
import time
import random

while True:

    r=random.randrange(0,100)
    if r<50:
        a='172.30.7.1'
        b='IPV4 '
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        a='fc00::7:1'
        b='IPV6 '
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    sock.connect((a, 2400))
    sock.sendall((b+sys.argv[1]).encode())

    time.sleep(random.randint(1,5))
    sock.close()
