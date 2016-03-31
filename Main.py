import queue
import sys
import asyncore
import socket
import threading
import Utility
import ManageDB

class Peer:

    def __init__(self,ipv4,ipv6):
        self.ipv4=ipv4
        self.ipv6=ipv6
        self.port=2400
        self.stop_queueIpv4 = queue.Queue(1)
        u1 = ReceiveServerIPV4(self.stop_queueIpv4,self.ipv4,self.port,(3,self.ipv4,self.port))
        self.server_thread = threading.Thread(target=u1)#crea un thread e gli assa l'handler per il server da far partire
        self.stop_queueIpv6 = queue.Queue(1)
        u2 = ReceiveServerIPV6(self.stop_queueIpv6,self.ipv6,self.port,(3,self.ipv6,self.port))
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
        type=msg[0:4]
        database=ManageDB()

        if type=="QUER":
            #TODO è meglio mettere tutta l'esecuzione del metodo in un thread
            lista=[]
            msgRet='AQUE'
            pkID=msg[4:20]
            ipDest=msg[20:75]
            portDest=msg[75:80]
            ttl=msg[80:82]
            file=msg[82:]

            #TODO eseguire metodo che controlla se è presente un packetId nel database
            #ad esempio database.checkId(pkId)

            #Esegue la risposta ad una query
            msgRet=msgRet+pkID
            ip=Utility.MY_IPV4+'|'+Utility.MY_IPV6
            port='{:0>5}'.format(Utility.PORT)
            msgRet=msgRet+ip+port
            l=database.findMd5(file)
            for i in range(0,len(l)):
                f=database.findFile(l[i][0])
                r=msgRet
                r=r+l[i][0]+f
                t1 = threading.Thread(target=Utility.sendMessage(r,ipDest,portDest))
                t1.start()
                lista.append(t1)

            #controllo se devo divulgare la query
            if int(ttl)>1:
                Utility.sendAllNear(msg,database.listClient())

            for i in range(0,len(lista)):
            	lista[i].join()




p=Peer('localhost','::1')
database=ManageDB()
while True:
    print("1. Ricerca")
    print("2. Aggiorna Vicini")
    print("3. Aggiungi File")
    print("4. Rimuovi File")
    print("5. Visualizza File")
    print("6. Visualizza Vicini")
    print(" ")
    sel=input("Inserisci il numero del comando da eseguire ")
    if sel==1: #TODO Eseguire una ricerca
        print(sel)
    elif sel==2:
        #TODO Aggiornare i near
        print(sel)
    elif sel==3:        #TODO Aggiungere un file al database
        print(sel)
    elif sel==4:        #TODO Rimozione di un file dal database
        print(sel)
    elif sel==5:        #TODO visualizza tutti i file del database
        print(sel)
    elif sel==6:
        lista=database.listClient()
        print(" ")
        print("IP e PORTA")
        for i in range(0,len(lista)):
            print("IP"+i+" "+lista[i][0]+" "+lista[i][1])
    else:
        sel=input("Commando Errato, attesa nuovo comando ")

