import socket
import random
import sys

# questo semplice codice realizza un
# peer che esegue il download di un file di test

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
        # ricevo le informazioni
        recv_mess = sock.recv(2048)
        buffer = buffer + recv_mess
        # verifico se esiste un chunk da leggere
        cont = True
        while cont:
            # and cortoricuitato se viene letta la lunghezza e se nel buffer
            # ci sono piu' bytes di quelli specificati in lunghezza posso leggere
            # altrimenti aspetto la prossima ricezione per leggere il chunk completo
            if len(buffer[:5]) >= 5 and len(buffer[5:]) >= int(buffer[:5]):
                len_chunk = int(buffer[:5])    # estrae la lunghezza del chunk
                data = buffer[5:5+len_chunk]    # estree i dati
                f.write(data)                   # scrive i dati
                count_chunk = count_chunk + 1   # contantore incrementato
                buffer = buffer[5 +len_chunk:]  # passa al prossimo chunk
            else:
                cont = False

    f.close()
