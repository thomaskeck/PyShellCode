from PyShellCode import ExecutableCode

import ctypes
import os


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

    code = ExecutableCode.from_NASMCode(nasm_code)
    result = code(data)
