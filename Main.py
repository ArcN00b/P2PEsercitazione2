import queue
import sys
import os
import asyncore
import socket
import threading
from ManageDB import *

class Peer:

    def __init__(self,ipv4,ipv6):
        self.ipv4=ipv4
        self.ipv6=ipv6
        self.port=3000
        self.stop_queue = queue.Queue(1)
        u1 = ReceiveServerIPV4(self.stop_queue,self.ipv4,self.port,(3,self.ipv4,self.port))
        self.server_thread = threading.Thread(target=u1)#crea un thread e gli assa l'handler per il server da far partire
        u2 = ReceiveServerIPV6(self.stop_queue,self.ipv6,self.port,(3,self.ipv6,self.port))
        self.server_threadIP6 = threading.Thread(target=u2)
        self.server_thread.start()#parte
        self.server_threadIP6.start()


class ReceiveServerIPV4(asyncore.dispatcher):
    """Questa classe rappresenta un server per accettare i pacchetti
    degli altri peer."""
    def __init__(self, squeue, ip, port, data_t):
        asyncore.dispatcher.__init__(self)
        self.squeue = squeue
        self.data_t = data_t #max near, mio ip e mia porta
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)#crea socket ipv6
        self.set_reuse_addr()#riusa indirizzo, evita problemi indirizzo occupato
        self.bind((ip, port)) #crea la bind del mio ip e porta
        self.listen(5)# sta in ascolto di 5 persone max

    def handle_accepted(self, socket_peer, address_peer):
        handler = ReceiveHandler(socket_peer, address_peer, self.data_t)

    def __call__(self):
        while self.squeue.qsize() == 0:
            asyncore.loop(timeout=1, count=5)

class ReceiveServerIPV6(asyncore.dispatcher):
    """Questa classe rappresenta un server per accettare i pacchetti
    degli altri peer."""
    def __init__(self, squeue, ip, port, data_t):
        asyncore.dispatcher.__init__(self)
        self.squeue = squeue
        self.data_t = data_t #max near, mio ip e mia porta
        self.create_socket(socket.AF_INET6,socket.SOCK_STREAM)#crea socket ipv6
        self.set_reuse_addr()#riusa indirizzo, evita problemi indirizzo occupato
        self.bind((ip, port)) #crea la bind del mio ip e porta
        self.listen(5)# sta in ascolto di 5 persone max

    def handle_accepted(self, socket_peer, address_peer):
        handler = ReceiveHandler(socket_peer, address_peer, self.data_t)

    def __call__(self):
        while self.squeue.qsize() == 0:
            asyncore.loop(timeout=1, count=5)

class ReceiveHandler(asyncore.dispatcher_with_send):

    def __init__(self, conn_sock, near_address, data):
        asyncore.dispatcher_with_send.__init__(self,conn_sock)
        self.near_address = near_address
        self.data_tuple = data

    # Questo e il metodo che viene chiamato quando ci sono delle recive
    def handle_read(self):
        msg=self.recv(2048)

        if msg[:4].decode() == "RETR":
            peer_md5 = msg[4:].decode()
            chuncklen = 512;

            obj = db.findFile(md5=peer_md5)

            if len(obj) > 0:
                # lettura statistiche file
                statinfo = os.stat(obj[0][0])
                # imposto lunghezza del file
                len_file = statinfo.st_size
                # controllo quante parti va diviso il file
                num_chunk = len_file // chuncklen
                if len_file % chuncklen != 0:
                    num_chunk = num_chunk + 1
                # pad con 0 davanti
                num_chunk = str(num_chunk).zfill(6)
                # costruzione risposta come ARET0000XX
                send_msg = ("ARET" + num_chunk).encode()

                f = open(obj[0][0],mode="rb")
                cont = True
                while cont:
                    r = f.read(chuncklen)
                    send_msg = send_msg + str(len(r)).zfill(5).encode()
                    send_msg = send_msg + r
                    if len(r) != chuncklen:
                        cont = False

                f.close()
                # ciclo di invio per numero di chunck
                cont = True
                while cont:
                    mess = send_msg[:2048]  #invio di 1024 alla volta
                    self.send(mess)
                    send_msg = send_msg[2048:]  #passo ai 2048 successivi
                    if len(mess) < 2048:
                        cont = False


        elif(msg[:4].decode() == "QUER"):
            print("ricevuto una query")

        else:
            print("ricevuto altro")


db = ManageDB()
db.addFile("1"*32, "live brixton.jpg")

# i = db.findFile(md5="1"*32)
# print("valore i: "+i[0][0])

p=Peer('127.0.0.1','::1')

while True:
    sel=input("Inserisci qualcosa ")
    print(sel)

