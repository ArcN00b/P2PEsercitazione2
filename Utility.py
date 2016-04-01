import random
import time
import hashlib
import socket
import threading

class Utility:

    MY_IPV4='127.0.0.1'
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
            ipv6 = stringa[t:]
            return ipv4, ipv6
        else:
            return '', ''

    # Manda un messaggio ad un determinato indirizzo
    # Apre e chiude la connessione velocemente
    @staticmethod
    def sendMessagge(messaggio, ip, porta):
        r = random.randrange(0, 100)
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
        lista = []
        for i in range(0, len(listaNear)):
            t1 = threading.Thread(target=Utility.sendMessage(messaggio, listaNear[i][0], listaNear[i][1]))
            t1.start()
            lista.append(t1)

        for i in range(0, len(lista)):
            lista[i].join()