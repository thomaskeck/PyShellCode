from PyShellCode import ExecutableCode

import ctypes
import numpy as np
import matplotlib.pyplot as plt

import pdb

if __name__ == '__main__':
    array = (ctypes.c_ulong*(5*1024))()
    ptr = ctypes.addressof(array) + ctypes.sizeof(ctypes.c_ulong)*(2*1024)

    onlyreload_nasm_code = """
        mfence
        rdtsc
        shl   rdx, 32
        or    rax, rdx
        mfence
        mov   rcx, rax  ; Save rax
        mov   rbx, {ptr}
        mov   rax, [rbx]
        mfence
        rdtsc
        shl   rdx, 32
        or    rax, rdx
        mfence
        sub   rax, rcx
        ret
    """.format(ptr=ptr)

    flushandreload_nasm_code = """
        mfence
        rdtsc
        shl   rdx, 32
        or    rax, rdx
        mfence
        mov   rcx, rax  ; Save rax
        mov   rbx, {ptr}
        mov   rax, [rbx]
        mfence
        rdtsc
        shl   rdx, 32
        or    rax, rdx
        mfence
        sub   rax, rcx
        mov   rcx, rax
        mov   rax, {ptr}
        clflush [rax]
        mov   rax, rcx
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

    bins = 600
    plt.hist(hits[hits < bins], label='hits', bins=bins/10)
    plt.hist(miss[miss < bins], label='miss', bins=bins/10)
    plt.legend()
    plt.show()
