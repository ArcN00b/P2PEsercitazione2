import queue
import sys
import os
import asyncore
import socket
import threading
from fileinput import filename

from ManageDB import *
from Parser import *
from Utility import *

global database
global numFindFile
global listFindFile

class Peer:

    def __init__(self,ipv4,ipv6):
        self.ipv4=ipv4
        self.ipv6=ipv6
        self.port=Utility.PORT                        # da sostituire con Utility.generatePort()
        self.stop_queue = queue.Queue(1)
        u1 = ReceiveServerIPV4(self.stop_queue,self.ipv4,self.port,(3,self.ipv4,self.port))
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

        # Ricevo i dati dal socket ed eseguo il parsing
        data = self.recv(2048)
        # controllo lunghezza dati ricevuta
        if len(data) > 0:
            # converto i comandi
            command, fields = Parser.parse(data.decode())

            if command == "RETR":
                # Imposto la lunghezza dei chunk e ottengo il nome del file a cui corrisponde l'md5
                chuncklen = 1024;
                peer_md5 = fields[0]
                obj = database.findFile(peer_md5)

                if len(obj) > 0:
                    filename = Utility.PATHDIR + str(obj[0][0])
                    # lettura statistiche file
                    statinfo = os.stat(filename)
                    # imposto lunghezza del file
                    len_file = statinfo.st_size
                    # controllo quante parti va diviso il file
                    num_chunk = len_file // chuncklen
                    if len_file % chuncklen != 0:
                        num_chunk = num_chunk + 1
                    # pad con 0 davanti
                    num_chunk = str(num_chunk).zfill(6)
                    # costruzione risposta come ARET0000XX
                    mess = ('ARET' + num_chunk).encode()
                    self.send(mess)

                    # Apro il file in lettura e ne leggo una parte
                    f = open(filename, 'rb')
                    r = f.read(chuncklen)

                    # Finchè il file non termina
                    while len(r) > 0:

                        # Invio la lunghezza del chunk
                        mess = str(len(r)).zfill(5).encode()
                        self.send(mess)
                        time.sleep(0.001)

                        # Invio il chunk
                        mess = r
                        self.send(mess)

                        # Proseguo la lettura del file
                        r = f.read(chuncklen)
                    # Chiudo il file
                    f.close()

            elif(command == "QUER"):
                msgRet = 'AQUE'
                # Prendo i campi del messaggio ricevuto
                pkID = fields[0]
                ipDest = fields[1]
                portDest = fields[2]
                ttl = fields[3]
                name = fields[4]

                # Controllo se il packetId è già presente se è presente non rispondo alla richiesta
                # E non la rispedisco
                if database.checkPkt(pkID)==False:
                    database.addPkt(pkID)
                    # Esegue la risposta ad una query
                    msgRet = msgRet + pkID
                    ip = Utility.MY_IPV4 + '|' + Utility.MY_IPV6
                    port = '{:0>5}'.format(Utility.PORT)
                    msgRet = msgRet + ip + port
                    l = database.findMd5(name.strip())
                    for i in range(0, len(l)):
                        f = database.findFile(l[i][0])
                        r = msgRet
                        r = r + l[i][0] + str(f[0][0]).ljust(width=100, fillchar=' ')
                        t1 = Sender(r, ipDest, portDest)
                        t1.run()

                    # controllo se devo divulgare la query
                    if int(ttl) > 1:
                        ttl='{:0>2}'.format(int(ttl)-1)
                        msg="QUER"+pkID+ipDest+portDest+ttl+name
                        lista=database.listClient()
                        if len(lista)>0:
                            t2 = SenderAll(msg, lista)
                            t2.run()

            elif command=="AQUE":
                if database.checkPkt(fields[0])==True:
                    global numFindFile
                    numFindFile+=1
                    listFindFile.append(fields)
                    print("-----")
                    print("Peer "+str(numFindFile))
                    print("IP "+fields[1]+fields[2])
                    print("MD5 "+fields[3])
                    print("Nome "+fields[4])
                    print("-----")

            elif command=="NEAR":
                if database.checkPkt(fields[0])==False and int(fields[3])>1:
                    database.addPkt(fields[0])
                    ip=Utility.MY_IPV4+"|"+Utility.MY_IPV6
                    port='{:0>5}'.format(Utility.PORT)
                    msgRet="ANEA"+fields[0]+ip+port
                    t=Sender(msgRet,fields[1],fields[2])
                    t.run()
                    ttl='{:0>2}'.format(int(fields[3])-1)
                    msg="NEAR"+fields[0]+fields[1]+fields[2]+ttl
                    lista=database.listClient()
                    if len(lista)>0:
                        t1 = SenderAll(msg,lista )
                        t1.run()

            elif command=="ANEA":
                if database.checkPkt(fields[0])==True:
                    database.addClient(fields[1],fields[2])

            else:
                print("ricevuto altro")
        else:
            print("\nXX fine della ricezione XX")

        self.close()


numFindFile=0
listFindFile=[]
database = ManageDB()
# TODO completare con la lista dei near iniziali
database.addClient(ip="172.030.007.003|fc00:0000:0000:000:0000:0000:0007:0003",port="3000")

#database.addFile("1"*32, "live brixton.jpg")

# i = db.findFile(md5="1"*32)
# print("valore i: "+i[0][0])
ipv4, ipv6 = Utility.getIp(Utility.MY_IPV4 +"|" + Utility.MY_IPV6)
p=Peer(ipv4,ipv6)
#if not os.path.exists(pathDir):
#    os.makedirs(pathDir)


while True:
    print("1. Ricerca")
    print("2. Aggiorna Vicini")
    print("3. Aggiungi File")
    print("4. Rimuovi File")
    print("5. Visualizza File")
    print("6. Visualizza Vicini")
    print("7. Aggiungi Vicino")
    print(" ")
    sel=input("Inserisci il numero del comando da eseguire ")
    if sel=="1":
        sel=input("Inserisci stringa da ricercare ")
        while len(sel)>20:
            sel=input("Stringa Troppo Lunga,reinserisci ")
        pktID=Utility.generateId(16)
        ip=Utility.MY_IPV4+'|'+Utility.MY_IPV6
        port='{:0>5}'.format(Utility.PORT)
        ttl='{:0>2}'.format(5)
        search=sel.ljust(width=20,fillchar=' ')
        msg="QUER"+pktID+ip+port+ttl+search
        database.addPkt(pktID)
        numFindFile = 0
        listFindFile = []
        lista=database.listClient()
        if len(lista)>0:
            t1 = SenderAll(msg, lista)
            t1.run()

        # Ogni 3 secondi controllo di avere risposte
        while numFindFile == 0:
            time.sleep(3)

        # Visualizzo le possibili scelte
        print("Scelta  PEER                                                        MD5                       Nome")
        print("0 Non scaricare nulla")
        for i in range(0,numFindFile):
            print(str(i + 1) + " " + listFindFile[i][1] + " " + listFindFile[i][3] + " " + listFindFile[i][4])

        # Chiedo quale file scaricare
        i = -1
        while i not in range(1, numFindFile +1):
            i = int(input("Scegli il file da scaricare oppure no ")) - 1

        if i > 0:
            t1 = Downloader(listFindFile[i][1], listFindFile[i][2], listFindFile[i][3], listFindFile[i][4])
            t1.run()

    elif sel=="2":
        listaNear=database.listClient()
        if len(listaNear)>0:
            pktID=Utility.generateId(16)
            ip=Utility.MY_IPV4+'|'+Utility.MY_IPV6
            port='{:0>5}'.format(Utility.PORT)
            ttl='{:0>2}'.format(2)
            msg="NEAR"+pktID+ip+port+ttl
            database.addPkt(pktID)
            database.removeAllClient()
            t1 = SenderAll(msg, listaNear)
            t1.run()

    elif sel=="3":

        #Ottengo la lista dei file dalla cartella corrente
        lst = os.listdir(Utility.PATHDIR)

        #Inserisco i file nel database
        if len(lst) > 0:
            for file in lst:
                database.addFile(Utility.generateMd5(Utility.PATHDIR+file), file)
            print("Operazione completata")
        else:
            print("Non ci sono file nella directory")

    elif sel=="4":

        # Ottengo la lista dei file dal database
        lst = database.listFile()

        # Visualizzo la lista dei file
        if len(lst) > 0:
            print("Scelta  MD5                                        Nome")
            for i in range(0,len(lst)):
                print(str(i) + "   " + lst[i][0] + " " + lst[i][1])

            # Chiedo quale file rimuovere
            i = -1
            while i not in range(0, len(lst)):
                i = int(input("Scegli il file da cancellare "))

            # Elimino il file
            database.removeFile(lst[i][0])
            print("Operazione completata")
        else:
            print("Non ci sono file nel database")

    elif sel=="5":

        # Ottengo la lista dei file dal database
        lst = database.listFile()

        # Visualizzo la lista dei file
        if len(lst) > 0:
            print("MD5                                        Nome")
            for file in lst:
                print(file[0] + " " + file[1])
        else:
            print("Non ci sono file nel database")

    elif sel=="6":
        lista=database.listClient()
        print(" ")
        print("IP e PORTA")
        for i in range(0,len(lista)):
            print("IP"+str(i)+" "+lista[i][0]+" "+lista[i][1])

    elif sel=="7":
        sel=input("Inserici Ipv4 ")
        t=sel.split('.')
        ipv4=""
        ipv4=ipv4+'{:0>3}'.format(t[0])+'.'
        ipv4=ipv4+'{:0>3}'.format(t[1])+'.'
        ipv4=ipv4+'{:0>3}'.format(t[2])+'.'
        ipv4=ipv4+'{:0>3}'.format(t[3])+'|'
        sel=input("Inserici Ipv6 ")
        t=sel.split(':')
        ipv6=""
        ipv6=ipv6+'{:0>4}'.format(t[0])+':'
        ipv6=ipv6+'{:0>4}'.format(t[1])+':'
        ipv6=ipv6+'{:0>4}'.format(t[2])+':'
        ipv6=ipv6+'{:0>4}'.format(t[3])+':'
        ipv6=ipv6+'{:0>4}'.format(t[4])+':'
        ipv6=ipv6+'{:0>4}'.format(t[5])+':'
        ipv6=ipv6+'{:0>4}'.format(t[6])+':'
        ipv6=ipv6+'{:0>4}'.format(t[7])
        sel=input("Inserici Porta ")
        port='{:0>5}'.format(int(sel))
        ip=ipv4+ipv6
        database.addClient(ip,port)
    else:
        sel=input("Commando Errato, attesa nuovo comando ")

