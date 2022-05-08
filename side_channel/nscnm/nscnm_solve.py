import socket
from pwn import *
from Crypto.Util.number import long_to_bytes
from time import sleep


BITS = 512
msg = b'toto'


HOST = "challenges.france-cybersecurity-challenge.fr"
PORT = 2254

r = remote(HOST, PORT)

rep = r.recvuntil(b'\n')
n = int(rep.split(b' ')[2].decode())

rep = r.recvuntil(b'\n')
e = int(rep.split(b' ')[2].decode())

print("n = ", n)
print("e = ", e)

d = ["0"] * 2 * BITS



for i in range(2 * BITS + 1 ):

    rep = r.recvuntil(b'msg = ')

    r.send(msg + b'\n')
    _ = r.recvuntil(b'skip = ')
    r.send((str(i) + '\n').encode())

    if i > 0:       
    
        c = int(rep.split(b'\n')[0].decode())
        if long_to_bytes(pow(c,e,n)) != msg:
            d[i-1] = "1"
        print(i, end=' ')
    
print(' ')

c = r.recvuntil(b'c = ')
c = r.recv()
print(c)
c = int(c.replace(b'\n',b'').decode())
        
print("c = ", c)

k = int(''.join(d), 2)
print(k)
        
print(long_to_bytes(pow(int(c),k,n)))
