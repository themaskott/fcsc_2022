import socket
from pwn import *
from Crypto.Util.number import long_to_bytes
from time import sleep


BITS = 256

msg = b'toto'
last = 0

HOST = "challenges.france-cybersecurity-challenge.fr"
PORT = 2255

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

	if i == 1:
		c = int(rep.split(b'\n')[0].decode())
		last = c
	if i > 1:
		c = int(rep.split(b'\n')[0].decode())
		if c != last:
			d[i-2] = "1"
		last = c
		print(i, end=' ')
		#print(d)


print(' ')

rep = r.recvuntil(b'c = ')
print(rep)

c = int(rep.split(b'\n')[0].decode())
if c != last:
	d[-1] = "1"

c = r.recv()
print(c)
c = int(c.replace(b'\n',b'').decode())
		
print("c = ", c)

k = int(''.join(d), 2)
print(k)
		
print(long_to_bytes(pow(int(c),k,n)))
