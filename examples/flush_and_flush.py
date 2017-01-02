from PyShellCode import ExecutableCode

import ctypes
import numpy as np
import matplotlib.pyplot as plt

import pdb

if __name__ == '__main__':
    array = (ctypes.c_ulong*(5*1024))()
    ptr = ctypes.addressof(array) + ctypes.sizeof(ctypes.c_ulong)*(2*1024)

    onlyreload_nasm_code = """
        mov   rbx, {ptr}
        mov   rcx, [rbx]
        mov   rcx, [rbx]
        cpuid
        mfence
        rdtsc
        shl   rdx, 32
        or    rax, rdx
        mfence
        mov   rcx, rax  ; Save rax
        mov   rax, {ptr}
        clflush [rax]
        mfence
        rdtsc
        shl   rdx, 32
        or    rax, rdx
        mfence
        sub   rax, rcx
        ret
    """.format(ptr=ptr)

    flushandreload_nasm_code = """
        mov   rbx, {ptr}
        mov   rcx, [rbx]
        mov   rcx, [rbx]
        cpuid
        mov   rax, {ptr}
        clflush [rax]
        cpuid
        mfence
        rdtsc
        shl   rdx, 32
        or    rax, rdx
        mfence
        mov   rcx, rax  ; Save rax
        mov   rax, {ptr}
        clflush [rax]
        mfence
        rdtsc
        shl   rdx, 32
        or    rax, rdx
        mfence
        sub   rax, rcx
        ret
    """.format(ptr=ptr)

    onlyreload = ExecutableCode.ExecutableCode.from_NASMCode(onlyreload_nasm_code)
    flushandreload = ExecutableCode.ExecutableCode.from_NASMCode(flushandreload_nasm_code)

    N = 1*1024**2
    hits = np.zeros(N)
    for i in range(N):
        hits[i] = onlyreload()
    
    miss = np.zeros(N)
    for i in range(N):
        miss[i] = flushandreload()

    bins = 300
    plt.hist(hits[hits < bins], label='hits', bins=bins/5, alpha=0.5)
    plt.hist(miss[miss < bins], label='miss', bins=bins/5, alpha=0.5)
    plt.legend()
    plt.show()
