#!/bin/bash

nasm -f elf64 shellcode.asm
ld -o shellcode shellcode.o
for i in `objdump -d shellcode | tr '\t' ' ' | tr ' ' '\n' | egrep '^[0-9a-f]{2}$' ` ; do echo -n "\x$i" ; done
echo ""
