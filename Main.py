import queue
import sys
import asyncore
import socket
import threading

class Peer:

    def __init__(self,ip):
        self.ip=ip
        self.port=3000
        self.stop_queue = queue.Queue(1)
        u = ReceiveServer(self.stop_queue,self.ip,self.port,(3,self.ip,self.port))
        self.server_thread = threading.Thread(target=u)#crea un thread e gli assa l'handler per il server da far partire
        self.server_thread.start()#parte

class ReceiveServer(asyncore.dispatcher):
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

class ReceiveHandler(asyncore.dispatcher_with_send):

    def __init__(self, conn_sock, near_address, data):
        asyncore.dispatcher_with_send.__init__(self,conn_sock)
        self.near_address = near_address
        self.data_tuple = data

    def handle_read(self):
        msg=self.recv(2048)
        print(msg.decode())

p=Peer('localhost')
while True:
    sel=input("Inserisci qualcosa ")
    print(sel)

