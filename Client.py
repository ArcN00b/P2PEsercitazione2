import socket
import sys
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("localhost", 3000))
sock.sendall(("Ciao "+sys.argv[1]).encode())

time.sleep(30)
sock.close()