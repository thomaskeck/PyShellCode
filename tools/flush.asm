; Adapted from https://github.com/IAIK/flush_flush/blob/master/sc/cacheutils.h

global _start

section .text

_start:
    mov rax, 0x1234
    clflush [rax]
    clflush [0x1234]
    mov rax, [0x1234]
