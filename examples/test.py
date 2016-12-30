from PyShellCode import PyShellCode
import ctypes
import errno
import os

if __name__ == '__main__':
    shell_code = b'\xeb\x1f\x48\x31\xc0\x48\x31\xdb\x48\x31\xc9\x48\x31\xd2\xb8\x04\x00\x00\x00\xbb\x01\x00\x00\x00\x59\xba\x0f\x00\x00\x00\xcd\x80\xc3\xe8\xdc\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21\x0a'
    code = PyShellCode.ExecutableCode.from_ShellCode(shell_code)
    code.print()
    print("isValid?", code.isValid())
    result = code()
    if result < 0:
        print(-result, errno.errorcode[-result], os.strerror(-result))
    print("Still here")
