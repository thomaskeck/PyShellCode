#!/usr/bin/env python3

import ctypes
import ctypes.util

import os
import tempfile
import subprocess
import mmap


class ExecutableCode(object):
    def __init__(self, memory_chunk, restype=ctypes.c_int64, *argtypes):
        self.restype = restype
        self.argtypes = argtypes
        self.memory_chunk = memory_chunk
        self.ctypes_buffer = ctypes.c_int.from_buffer(memory_chunk)
        self.executable_code = ctypes.CFUNCTYPE(self.restype, *argtypes)(ctypes.addressof(self.ctypes_buffer))

    def print(self):
        print(self.memory_chunk)
    
    def isValid(self):
        return True

    def __call__(self, *data):
        return self.executable_code(*data)

    @classmethod
    def from_NASMCode(cls, nasm_code, restype=ctypes.c_int64, *argtypes):
        oldcwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tempdir:
            os.chdir(tempdir)
            with open('shellcode.asm', 'w') as f:
                f.write("global _start\nsection .text\n_start:\n")
                f.write(nasm_code)
            subprocess.check_call("nasm -f elf64 shellcode.asm -o shellcode.o", shell=True)
            subprocess.check_call("ld -o shellcode shellcode.o", shell=True)
            output = subprocess.getoutput("objdump -d shellcode | tr '\t' ' ' | tr ' ' '\n' | egrep '^[0-9a-f]{2}$'")
            shell_code = bytes(map(lambda x: int(x, base=16), output.strip().split('\n')))
        os.chdir(oldcwd)
        return cls.from_ShellCode(shell_code, restype, *argtypes)

    @classmethod
    def from_ShellCode(cls, shell_code, restype=ctypes.c_int64, *argtypes):
        if not isinstance(shell_code, bytes):
            shell_code = bytes(shell_code, 'utf-8')
        mm = mmap.mmap(-1, len(shell_code), flags=mmap.MAP_SHARED | mmap.MAP_ANONYMOUS, prot=mmap.PROT_WRITE | mmap.PROT_READ | mmap.PROT_EXEC)
        mm.write(shell_code)
        return cls(mm, restype, *argtypes)
    
    @classmethod
    def from_File(cls, filename, restype=ctypes.c_int64, *argtypes):
        with open(filename, 'rb') as f:
            shell_code = f.read()
            return cls.from_ShellCode(shell_code, restype, *argtypes )
