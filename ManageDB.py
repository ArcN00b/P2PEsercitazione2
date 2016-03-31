# Ho mantenuto i nomi delle tabelle per semplicita
# I peer sono salvati nella tabella CLIENTS
# CLIENTS:  IP      PORT
# FILES:    MD5     NAME

import sqlite3
import time

class ManageDB:

    # Metodo che inizializza il database
    def __init__(self):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Creo la tabella dei peer e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS CLIENTS")
            c.execute("CREATE TABLE CLIENTS (IP TEXT NOT NULL, PORT TEXT NOT NULL)")

            # Creo la tabella dei file e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS FILES")
            c.execute("CREATE TABLE FILES (NAME TEXT NOT NULL, MD5 TEXT NOT NULL)")

            # Creo la tabella dei packetId e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS PACKETS")
            c.execute("CREATE TABLE PACKETS (ID TEXT NOT NULL, DATE INTEGER NOT NULL)")

            '''
            # Creo la lista dei pktid
            self.__pkIdList = []
            '''

            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - init: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che aggiunge un peer
    def addClient(self, ip, port):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il client
            c.execute("INSERT INTO CLIENTS (IP, PORT) VALUES (?,?)" , (ip, port))
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - addClient: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che aggiunge un file
    def addFile(self, md5, name):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Controllo se esiste il file
            c.execute("SELECT COUNT(MD5) FROM FILES WHERE MD5=:COD" , {"COD": md5})
            num = c.fetchall()

            # Aggiungo  il file se non e' presente
            if num[0][0] == 0:
                c.execute("INSERT INTO FILES (NAME, MD5) VALUES (?,?)" , (name, md5))

            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - addFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina un peer tramite indirizzo ip e porta
    def removeClient(self, ip, port):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il client
            c.execute("DELETE FROM CLIENTS WHERE IP=:INDIP AND PORT=:PORTA", {"INDIP": ip, "PORTA": port})
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - removeClient: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina il file identificato da md5
    def removeFile(self, md5):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il file
            c.execute("DELETE FROM FILES WHERE MD5=:COD" , {"COD": md5} )
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - removeFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina tutti i file
    def removeAllFile(self):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo tutti i file
            c.execute("DELETE FROM FILES")
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - removeAllFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per ricercare il nome del file tramite md5
    def findFile(self,md5):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il file
            c.execute("SELECT DISTINCT NAME FROM FILES WHERE MD5 = ? " , (md5,))
            conn.commit()

            result = c.fetchall()
            return result

        except sqlite3.Error as e:

            raise Exception("Errore - findFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per ricercare l'md5 del file da stringa di ricerca
    def findMd5(self,name):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il file
            c.execute("SELECT DISTINCT MD5 FROM FILES WHERE NAME LIKE '%" + name + "%' ")
            conn.commit()

            result = c.fetchall()
            return result

        except sqlite3.Error as e:

            raise Exception("Errore - findFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per verificare se esiste un file tramite md5
    def searchIfExistFile(self,md5):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il file
            c.execute("SELECT COUNT(MD5) FROM FILES WHERE MD5=:COD" , {"COD": md5})
            conn.commit()

            result = c.fetchall()
            return result

        except sqlite3.Error as e:

            raise Exception("Errore - searchIfExistFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che ritorna il numero di file presenti con nome simile alla stringa di ricerca
    def numOfFile(self, name):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il numero di file
            c.execute("SELECT COUNT(MD5) FROM FILES WHERE NAME LIKE '%" + name + "%' ")

            conn.commit()

            result = c.fetchall()
            return result

        except sqlite3.Error as e:

            raise Exception("Errore - numOfFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che ritorna la lista dei peer
    def listClient(self):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Prelevo la lista di peer
            c.execute("SELECT * FROM CLIENTS")
            conn.commit()

            return c.fetchall()

        except sqlite3.Error as e:

            raise Exception("Errore - ListCLients: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che ritorna la lista dei file
    def listFile(self):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Prelevo la lista di file
            c.execute("SELECT MD5, NAME FROM FILES")
            conn.commit()

            return c.fetchall()

        except sqlite3.Error as e:

            raise Exception("Errore - listFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che aggiunge un packetId
    def addPkt(self, id):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il packet
            c.execute("INSERT INTO PACKETS (ID, DATE) VALUES ( ?, DATETIME('NOW'))" , (id,))
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - addPkt: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che rimuove un packetId
    def removeSinglePkt(self, id):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il packet
            c.execute("DELETE FROM PACKETS WHERE ID=:COD" , {"COD": id} )
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - removePkt: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che ritorna la lista dei packetId
    def listPkt(self):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Prelevo la lista di packets
            c.execute("SELECT ID FROM PACKETS")
            conn.commit()

            return c.fetchall()

        except sqlite3.Error as e:

            raise Exception("Errore - listPkt: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina i pacchetti piu' vecchi di 5 minuti e ritorna la lista dei packetId
    def removeOldPkt(self):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Prelevo la lista di packets
            c.execute("DELETE FROM PACKETS WHERE DATE < datetime('now', '-5 MINUTES')")
            conn.commit()

        except sqlite3.Error as e:

            raise Exception("Errore - returnAndClearPkt: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()


'''

    # Metodo che aggiunge un packetId
    def addPkt(self, id):

        # Aggiungo il packetId
        self.__pkIdList.append(id)

    # Metodo che rimuove un packetId
    def removePkt(self, id):

        # Rimuovo il packetId
        self.__pkIdList.remove(id)

        # Se e' presente un altro packetId uguale, genero una eccezione
        if(self.__pkIdList.count(id) > 0):
            raise Exception("Errore - removePkt: packetId multipli con stesso id")

    # Metodo che ritorna la lista dei packetId
    def listPkt(self):

        # Ritorno tutti i packetId in una lista differente
        return list(self.__pkIdList)

    # Metodo che ricerca un packetId
    def searchPkt(self, id):

        count = self.__pkIdList.count(id)

        # Ritorno True se il packet e' presente, altrimenti False
        if(count == 1):
            return True
        elif(count == 0):
            return False
        else:
            raise Exception("Errore - searchPkt: packetId multipli con stesso id")

'''

'''

# TEST PACKETID CON DATABASE
manager = ManageDB()

# Inserisco packet
print("1) Inserisco packet")
manager.addPkt(1)
manager.addPkt(2)
manager.addPkt(3)

print("Packet presenti")
all_rows = manager.listPkt()
for row in all_rows:
    print('{0}'.format(row[0]))
print("")


# Rimuovo packet
print("2) Rimuovo packet")
manager.removeSinglePkt(2)

print("Packet presenti")
all_rows = manager.listPkt()
for row in all_rows:
    print('{0}'.format(row[0]))
print("")

# Inserire -1 SECONDS al posto di -5 MINUTES in removeOldPkt
# Aggiungo una sleep per effettuare un ritardo tra l'inserimento e la rimozione

# Sleep che da esito incerto: possono essere rimossi o meno i packets a seconda dell'esecuzione
time.sleep(1.3)

# Sleep sufficiente a rimuovere i packets
# time.sleep(2)


# Aggiorno i packets
print("3) Rimuovo i packets meno recenti")
manager.removeOldPkt()

print("Packet presenti")
all_rows = manager.listPkt()
for row in all_rows:
    print('{0}'.format(row[0]))
print("")

'''


'''
# TEST PACKETID CON LISTA
manager = ManageDB()

# Inserisco packet
print("1) Inserisco packet")
manager.addPkt(1)
manager.addPkt(2)
manager.addPkt(3)

print("Packet presenti")
print(manager.listPkt())
print("")


# Rimuovo packet
print("2) Rimuovo packet")
manager.removePkt(3)

print("Packet presenti")
print(manager.listPkt())
print("")


# Inserisco packet dalla lista di copia
print("3) Aggiungo packet alla lista di copia")
manager.listPkt().append(5)

print("Packet presenti")
print(manager.listPkt())
print("")


# Ricerco un packet
print("4) Ricerco un packet presente")

print(manager.searchPkt(1))
print("")


# Ricerco un packet
print("5) Ricerco un packet non presente")

print(manager.searchPkt(100))
print("")

'''


'''

# TEST CLIENTS E FILES
manager = ManageDB()

# Inserimento peer
print("1) Inserisco peer")
manager.addClient("1.1.1.1","1")
manager.addClient("1.1.1.1","2")
manager.addClient("2.2.2.2","2")

print("Peer presenti")
all_rows = manager.listClient()
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
print("")


# Rimozione peer
print("2) Rimuovo un peer in ascolto su una porta")
manager.removeClient("1.1.1.1","2")

print("Peer presenti")
all_rows = manager.listClient()
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
print("")


# Inserimento file
print("3) Inserisco file")
manager.addFile("123", "pippo")
manager.addFile("345", "pluto")
manager.addFile("567", "paperino")
manager.addFile("789", "topolino")

print("File presenti")
all_rows = manager.listFile()
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
print("")


# Rimozione file
print("4) Rimuovo singolo file")
manager.removeFile("345")

print("File presenti")
all_rows = manager.listFile()
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
print("")


# Ricerca file per md5
print("5) Ricerco file per md5")

all_rows = manager.findFile("123")
for row in all_rows:
    print('{0}'.format(row[0]))
print("")


# Ricerca file per nome
print("6) Ricerco file per nome")

all_rows = manager.findMd5("pippo")
for row in all_rows:
    print('{0}'.format(row[0]))
print("")


# Ricerca di un file
print("7) Controllo se esiste un file presente")

all_rows = manager.searchIfExistFile("123")
for row in all_rows:
    print('{0}'.format(row[0]))
print("")


# Ricerca di un file
print("8) Controllo se esiste un file non presente")

all_rows = manager.searchIfExistFile("000")
for row in all_rows:
    print('{0}'.format(row[0]))
print("")


# Numero di file presenti
print("9) Controllo quanti file sono presenti")

all_rows = manager.numOfFile("")
for row in all_rows:
    print('{0}'.format(row[0]))
print("")


# Rimozione file
print("10) Rimuovo tutti i file")
manager.removeAllFile()

print("File presenti")
all_rows = manager.listFile()
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
print("")

'''