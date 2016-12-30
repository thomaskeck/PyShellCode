; Adapted from https://github.com/IAIK/flush_flush/blob/master/sc/cacheutils.h

global _start

section .text

_start:
    xor rax, rax
    xor rdx, rdx
    nop
    rdtsc
    shl   rdx, 32
    or    rax, rdx
    cpuid
    rdtscp
    shl   rdx, 32
    or    rax, rdx
