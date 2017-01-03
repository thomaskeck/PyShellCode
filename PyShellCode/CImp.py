#!/usr/bin/env python3

import ctypes
import ctypes.util

import os
import tempfile
import subprocess

PyShellCode_library =  ctypes.cdll.LoadLibrary(os.getcwd() + '/libPyShellCode.so')
print('Loaded ', PyShellCode_library)

PyShellCode_library.create_ExecutableCode_from_ShellCode.restype = ctypes.c_void_p
PyShellCode_library.create_ExecutableCode_from_ShellCode.argtypes = [ctypes.c_char_p, ctypes.c_uint]
PyShellCode_library.create_ExecutableCode_from_File.restype = ctypes.c_void_p
PyShellCode_library.create_ExecutableCode_from_File.argtypes = [ctypes.c_char_p]
PyShellCode_library.valid_ExecutableCode.restype = ctypes.c_int
PyShellCode_library.valid_ExecutableCode.argtypes = [ctypes.c_void_p]
PyShellCode_library.execute_ExecutableCode.restype = ctypes.c_int64
PyShellCode_library.execute_ExecutableCode.argtypes = [ctypes.c_void_p]
PyShellCode_library.execute_with_void_ptr_ExecutableCode.restype = ctypes.c_int64
PyShellCode_library.execute_with_void_ptr_ExecutableCode.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
PyShellCode_library.destroy_ExecutableCode.argtypes = [ctypes.c_void_p]
PyShellCode_library.print_ExecutableCode.argtypes = [ctypes.c_void_p]


def PrintVersion():
    PyShellCode_library.PrintVersion()


class ExecutableCode(object):
    def __init__(self, executable_code):
        self.executable_code = executable_code

    def print(self):
        PyShellCode_library.print_ExecutableCode(self.executable_code)
    
    def isValid(self):
        return PyShellCode_library.valid_ExecutableCode(self.executable_code) != 0

    def __call__(self, data=None):
        if data is None:
            return PyShellCode_library.execute_ExecutableCode(self.executable_code)
        else:
            ptr = ctypes.addressof(data)
            return PyShellCode_library.execute_with_void_ptr_ExecutableCode(self.executable_code, ptr)

    def __del__(self):
        PyShellCode_library.destroy_ExecutableCode(self.executable_code)

    @classmethod
    def from_NASMCode(cls, nasm_code):
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
        return cls.from_ShellCode(shell_code)

    @classmethod
    def from_ShellCode(cls, shell_code):
        if not isinstance(shell_code, bytes):
            shell_code = bytes(shell_code, 'utf-8')
        return cls(PyShellCode_library.create_ExecutableCode_from_ShellCode(ctypes.c_char_p(shell_code), len(shell_code)))
    
    @classmethod
    def from_File(cls, filename):
        return cls(PyShellCode_library.create_ExecutableCode_from_File(filename))
