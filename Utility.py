import random
import time
import hashlib

class Utility:

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