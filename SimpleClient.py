import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("127.0.0.1", 3000))
md5 = ["0001000100010001", "0002000200020002", "0003000300030003", "0004000400040004"]

sock.sendall("LOGI173.010.007.0007|FC30:0000:0000:0000:0000:0000:0004:000112345".encode());

buffer = sock.recv(1024).decode();
sessionID = buffer[-16:];
print("ricevuto: " + buffer)

# aggiungo un file
filename = "pippo.txt"
space = ' '*(100-len(filename))
mess = "ADDF"+sessionID+md5[0]+filename+space
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("aggiunto: " + buffer)

# aggiungo un altro file
filename = "pluto.txt"
space = ' '*(100-len(filename))
mess = "ADDF"+sessionID+md5[1]+filename+space
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("aggiunto: " + buffer)

# aggiungo un altro file
filename = "topolino.txt"
space = ' '*(100-len(filename))
mess = "ADDF"+sessionID+md5[2]+filename+space
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("aggiunto: " + buffer)

# test ricerca del file
find = "txt"
space = ' '*(20-len(find))
mess = "FIND"+sessionID+find+space
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("trovato: " + buffer)

# test download di un file
mess = "DREG"+sessionID+md5[1];
sock.sendall(mess.encode())
buffer = sock.recv(1024).decode()
print("download: " + buffer)

mess = "DREG"+sessionID+md5[1];
sock.sendall(mess.encode())
buffer = sock.recv(1024).decode()
print("download: " + buffer)

# test di rimozione di un file
mess = "DELF" + sessionID +md5[0];
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("rimosso: " + buffer)

# aggiunta di un altro file
filename = "paperino.txt"
space = ' '*(100-len(filename))
mess = "ADDF"+sessionID+md5[3]+filename+space
sock.sendall(mess.encode())

buffer = sock.recv(1024).decode()
print("aggiunto: " + buffer)

# test logout
mess = "LOGO"+sessionID
sock.sendall(mess.encode())
buffer = sock.recv(1024).decode()
print("logout :" + buffer)

sock.close()