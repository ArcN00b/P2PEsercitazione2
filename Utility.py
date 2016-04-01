import random
import time
import hashlib
import socket
import threading

class Utility:

    MY_IPV4='192.168.0.9'
    MY_IPV6='::1'
    PORT=3000

    # Metodo che genera un numero random nel range [1024, 65535]
    @staticmethod
    def generatePort():
        random.seed(time.process_time())
        return random.randrange(1024, 65535)
    # Questo metodo genera un packet id randomico
    # Chiede di quanti numeri deve essere il valore generato
    @staticmethod
    def generateId(lunghezza):
        random.seed(time.process_time())
        seq = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        val = ''
        for i in range(0, lunghezza):
            val = val + random.choice(seq)
        return val

    # Metodo per generare l'md5 di un file, va passato il percorso assoluto
    @staticmethod
    def generateMd5(path):

        #path="/home/flavio/Scrivania/pippo.txt"
        # Inizializzo le variabili che utilizzerò
        f = open(path, 'rb')
        hash = hashlib.md5()

        # Per una lettura più efficiente suddivido il file in blocchi
        buf = f.read(4096)
        while len(buf) > 0:
            hash.update(buf)
            buf = f.read(4096)

        # Return del digest
        return hash.hexdigest()

        # Ritorna i due ip data la stringa generale
        # Ritorna prima ipv4 e poi ipv6

    @staticmethod
    def getIp(stringa):
        t = stringa.find('|')
        if t != -1:
            ipv4 = stringa[0:t]
            ipv6 = stringa[t + 1:]
            return ipv4, ipv6
        else:
            return '', ''

    # Manda un messaggio ad un determinato indirizzo
    # Apre e chiude la connessione velocemente
    @staticmethod
    def sendMessagge(messaggio, ip, porta):
        r = 0 #random.randrange(0, 100)
        ipv4, ipv6 = Utility.getIp(ip)
        if r < 50:
            a = ipv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            a = ipv6
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        sock.connect((a, int(porta)))
        sock.sendall(messaggio.encode())
        time.sleep(1)
        sock.close()

    # Manda un messaggio a tutti i vicini
    @staticmethod
    def sendAllNear(messaggio, listaNear):
        for i in range(0, len(listaNear)):
            Utility.sendMessage(messaggio, listaNear[i][0], listaNear[i][1])

    @staticmethod
    def download(ipp2p, pp2p, md5, name):

        r=0 #random.randrange(0,100)
        ipv4, ipv6 = Utility.getIp(ipp2p)
        if r < 50:
            ind = ipv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            ind = ipv6
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        sock.connect((ind, pp2p))
        sock.sendall(('RETR' + md5).encode())

        # ricevo i primi 10 Byte che sono "ARET" + n_chunk
        recv_mess = sock.recv(10).decode()
        if recv_mess[:4] == "ARET":
            num_chunk = int(recv_mess[4:])
            count_chunk = 0

            # apro il file per la scrittura
            f = open(name.rstrip(' '), "wb") #Apro il file rimuovendo gli spazi finali dal nome
            buffer = bytes()

            # Finchè i chunk non sono completi
            while count_chunk < num_chunk:

                chunklen = int(sock.recv(5).decode())       # Leggo la lunghezza del chunk
                buffer = sock.recv(chunklen)                # Leggo il contenuto del chunk
                f.write(buffer)                             # Scrivo il contenuto del chunk nel file
                count_chunk += 1                            # Aggiorno il contatore
            f.close()

class Sender:
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, messaggio, ip, port):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.messaggio = messaggio
        self.ip = ip
        self.port = port

    # Funzione che lancia il worker e controlla la chiusura improvvisa
    def start(self):
        try:
            self.sendAllNear(self.messaggio, self.ip, self.port)
        except Exception as e:
            print("errore: ", e)

    def sendMessagge(self, messaggio, ip, porta):
        r = 0  # random.randrange(0, 100)
        ipv4, ipv6 = Utility.getIp(ip)
        if r < 50:
            a = ipv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            a = ipv6
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        sock.connect((a, int(porta)))
        sock.sendall(messaggio.encode())
        time.sleep(1)
        sock.close()

class SenderAll:
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, messaggio, listaNear):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.messaggio = messaggio
        self.listaNear = listaNear

    # Funzione che lancia il worker e controlla la chiusura improvvisa
    def start(self):
        try:
            self.sendAllNear(self.messaggio, self.listaNear)
        except Exception as e:
            print("errore: ", e)

    def sendAllNear(self, messaggio, listaNear):
        for i in range(0, len(listaNear)):
            self.sendMessage(messaggio, listaNear[i][0], listaNear[i][1])

    def sendMessagge(messaggio, ip, porta):
        r = 0  # random.randrange(0, 100)
        ipv4, ipv6 = Utility.getIp(ip)
        if r < 50:
            a = ipv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            a = ipv6
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        sock.connect((a, int(porta)))
        sock.sendall(messaggio.encode())
        time.sleep(1)
        sock.close()

class Downloader:
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, ipp2p, pp2p, md5, name):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.ipp2p = ipp2p
        self.pp2p = pp2p
        self.md5 = md5
        self.name = name

    # Funzione che lancia il worker e controlla la chiusura improvvisa
    def start(self):
        try:
            self.download(self.ipp2p, self.pp2p, self.md5, self.name)
        except Exception as e:
            print("errore: ", e)

    def download(self, ipp2p, pp2p, md5, name):
        r = 0  # random.randrange(0,100)
        ipv4, ipv6 = Utility.getIp(ipp2p)
        if r < 50:
            ind = ipv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            ind = ipv6
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        sock.connect((ind, pp2p))
        sock.sendall(('RETR' + md5).encode())

        # ricevo i primi 10 Byte che sono "ARET" + n_chunk
        recv_mess = sock.recv(10).decode()
        if recv_mess[:4] == "ARET":
            num_chunk = int(recv_mess[4:])
            count_chunk = 0

            # apro il file per la scrittura
            f = open(name.rstrip(' '), "wb")  # Apro il file rimuovendo gli spazi finali dal nome
            buffer = bytes()

            # Finchè i chunk non sono completi
            while count_chunk < num_chunk:
                chunklen = int(sock.recv(5).decode())  # Leggo la lunghezza del chunk
                buffer = sock.recv(chunklen)  # Leggo il contenuto del chunk
                f.write(buffer)  # Scrivo il contenuto del chunk nel file
                count_chunk += 1  # Aggiorno il contatore
            f.close()