from PyShellCode import ShellCode
from PyShellCode import ExecutableCode

import ctypes
import numpy as np
import matplotlib.pyplot as plt

import pdb

if __name__ == '__main__':
    array = (ctypes.c_ulong*(5*1024))()
    ptr = ctypes.addressof(array) + ctypes.sizeof(ctypes.c_ulong)*(2*1024)

    rdtsc = ExecutableCode.ExecutableCode.from_ShellCode(ShellCode.call_rdtsc())
    maccess =  ExecutableCode.ExecutableCode.from_ShellCode(ShellCode.call_maccess(ptr))
    flush = ExecutableCode.ExecutableCode.from_ShellCode(ShellCode.call_flush(ptr))

    def onlyreload():
        time = rdtsc()
        maccess()
        delta = rdtsc() - time
        return ctypes.c_uint32(delta).value

    def flushandreload():
        time = rdtsc()
        maccess()
        delta = rdtsc() - time
        flush()
        return ctypes.c_uint32(delta).value

    N = 1*1024**2
    hits = np.zeros(N)
    for i in range(N):
        hits[i] = onlyreload()
    
    miss = np.zeros(N)
    for i in range(N):
        miss[i] = flushandreload()

    plt.hist(hits[hits < 1e4], label='hits', alpha=0.5, bins=1000)
    plt.hist(miss[miss < 1e4], label='miss', alpha=0.5, bins=1000)
    plt.legend()
    plt.show()
