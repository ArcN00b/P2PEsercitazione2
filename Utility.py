import random
import time

class Utility:

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




