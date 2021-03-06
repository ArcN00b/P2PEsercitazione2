import socket
import random
import sys

# questo semplice codice realizza un
# peer che esegue il download di un file di test
from Utility import Utility

ip = "127.000.000.001|0000:0000:0000:0000:0000:0000:0000:0001"
port = "03000"
md5 = Utility.generateMd5(path=Utility.PATHDIR + "live brixton.jpg")
output = "/home/marco/pendulum.jpg"

Utility.download(ipp2p=ip, pp2p=port, md5=md5, name=output)

'''

r=random.randrange(0,100)
if r < 50:
    ind = '127.0.0.1'
    info = 'IPV4 '
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    ind = '::1'
    info = 'IPV6 '
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

sock.connect((ind, 3000))
sock.sendall(('RETR'+'1'*32).encode())

# ricevo i primi 10 Byte che sono "ARET" + n_chunk
recv_mess = sock.recv(10).decode()
if recv_mess[:4] == "ARET":
    num_chunk = int(recv_mess[4:])
    count_chunk = 0

    # apro il file per la scrittura
    f = open("pendulum.jpg", "wb")
    buffer = bytes()

    while count_chunk < num_chunk:

        chunklen = int(sock.recv(5).decode())       # Leggo la lunghezza del chunk
        buffer = sock.recv(chunklen)                # Leggo il contenuto del chunk
        f.write(buffer)                             # Scrivo il contenuto del chunk nel file
        count_chunk += 1                            # Aggiorno il contatore
    f.close()
'''