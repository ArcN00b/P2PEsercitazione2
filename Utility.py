import random
import time
import hashlib

class Utility:

    MY_IPV4='172.30.7.1'
    MY_IPV6='fc00::7:1'
    PORT=3000
    # Questo metodo genera un packet id randomico
    # Chiede di quanti numeri deve essere il valore generato
    @staticmethod
    def generateId(lunghezza):
        random.seed(time.process_time())
        s='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        val=''
        for i in range(0,lunghezza):
            val=val+s[random.randint(0,len(s)-1)]
        return val

    # Metodo per generare l'md5 di un file, va passato il percorso assoluto
    @staticmethod
    def generateMd5(path="/home/test.txt"):
        f=open(path)
        r=f.read(512)
        s=r
        while len(r)!=0:
            r=f.read(512)
            s=s+r
        m=hashlib.md5()
        m.update(s.encode())
        val=m.hexdigest()
        print(val)
        return val




