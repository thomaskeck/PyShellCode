from PyShellCode import ShellCode
from PyShellCode import ExecutableCode

import ctypes
import numpy as np
import matplotlib.pyplot as plt

import struct

if __name__ == '__main__':
    array = (ctypes.c_ulong*(5*1024))()
    ptr = ctypes.addressof(array) + ctypes.sizeof(ctypes.c_ulong)*(2*1024)

    print(hex(ptr))
    print(struct.pack('=Q', ptr))

    rdtsc = ExecutableCode.ExecutableCode.from_ShellCode(ShellCode.call_rdtsc())
    maccess =  ExecutableCode.ExecutableCode.from_ShellCode(ShellCode.call_maccess(ptr))
    flush = ExecutableCode.ExecutableCode.from_ShellCode(ShellCode.call_flush(ptr))

    def onlyreload():
        time = rdtsc()
        maccess()
        delta = rdtsc() - time
        return delta

    def flushandreload():
        time = rdtsc()
        maccess()
        delta = rdtsc() - time
        flush()
        return delta

    N = 1*1024**2
    hits = np.zeros(N)
    for i in range(N):
        hits[i] = onlyreload()
    
    miss = np.zeros(N)
    for i in range(N):
        miss[i] = flushandreload()

    plt.hist(hits, label='hits', alpha=0.5)
    plt.hist(miss, label='miss', alpha=0.5)
    plt.legend()
    plt.show()
