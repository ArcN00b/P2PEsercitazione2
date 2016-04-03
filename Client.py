import socket
import sys
import time
import random

while True:

    sel=input("Inserici Ipv4 ")
    ip4=sel
    t=sel.split('.')
    ipv4=""
    ipv4=ipv4+'{:0>3}'.format(t[0])+'.'
    ipv4=ipv4+'{:0>3}'.format(t[1])+'.'
    ipv4=ipv4+'{:0>3}'.format(t[2])+'.'
    ipv4=ipv4+'{:0>3}'.format(t[3])+'|'
    sel=input("Inserici Ipv6 ")
    ip6=sel
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

    r=random.randrange(0,100)
    r=0
    if r<50:
        a=ip4
        b='IPV4 '
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        a=ip6
        b='IPV6 '
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    sock.connect((a, 2500))
    a="NEAR1234567890123452"+ip+port+'08'
    sock.sendall(a.encode())
    time.sleep(1)
    s=sock.recv(2048)
    while len(s)>0:
        s=sock.recv(2048)
        print(s.decoce())
    sock.close()
