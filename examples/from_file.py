from PyShellCode import ExecutableCode
import ctypes
import errno
import os

if __name__ == '__main__':
    code = ExecutableCode.ExecutableCode.from_File(b"examples/example_shellcode_file")
    print("Is the generated Executable Code valid?", code.isValid())
    print("Generated Shell Code", code.print())
    print("Run code")
    result = code()
    print("Return value", result)
