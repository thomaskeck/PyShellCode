from PyShellCode import ExecutableCode
import ctypes
import errno
import os

if __name__ == '__main__':
    shell_code = b"\xeb\x13\xb8\x01\x00\x00\x00\xbf\x01\x00\x00\x00\x5e\xba\x0f\x00\x00\x00\x0f\x05\xc3\xe8\xe8\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21\x0a"
    code = ExecutableCode.from_ShellCode(shell_code)
    print("Is the generated Executable Code valid?", code.isValid())
    print("Generated Shell Code", code.print())
    print("Run code")
    result = code()
    print("Return value", result)
