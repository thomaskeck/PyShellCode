#!/usr/bin/env python3

import ctypes
import ctypes.util

import os
import tempfile
import subprocess
import mmap


def create_shellcode_from_nasmcode(nasm_code):
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
    return shell_code


def create_function_from_shellcode(shell_code, restype=ctypes.c_int64, argtypes=()):
    mm = mmap.mmap(-1, len(shell_code), flags=mmap.MAP_SHARED | mmap.MAP_ANONYMOUS, prot=mmap.PROT_WRITE | mmap.PROT_READ | mmap.PROT_EXEC)
    mm.write(shell_code)
    ctypes_buffer = ctypes.c_int.from_buffer(mm)
    function = ctypes.CFUNCTYPE(restype, *argtypes)(ctypes.addressof(ctypes_buffer))
    function._avoid_gc_for_mmap = mm
    return function


if __name__ == '__main__':
    text = b'Hallo Welt\n'
    data = (ctypes.c_char*len(text))()
    data[:] = text

    nasm_code = """
    mov rax, 0x1 ; Parameter 0 -> Syscall Nr
    mov rsi, rdi ; Parameter 2 -> buffer is passed as first argument to the function call
    mov rdi, 0x1 ; Parameter 1 -> fd
    mov rdx, {length}; Parameter 3 -> length
    syscall
    ret
    """.format(length=len(text))
    print("NASM code", nasm_code)

    shell_code = create_shellcode_from_nasmcode(nasm_code)
    print("ShellCode", shell_code)
    
    function = create_function_from_shellcode(shell_code, argtypes=(ctypes.c_void_p,))
    print("Function", function)

    result = function(data)
    print("Result", result)
