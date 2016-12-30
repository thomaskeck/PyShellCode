from PyShellCode import ShellCode
from PyShellCode import ExecutableCode
import ctypes
import errno
import os

if __name__ == '__main__':
    shell_code = ShellCode.syscall_write(1, 'Hallo Welt!\n')
    code = ExecutableCode.ExecutableCode.from_ShellCode(shell_code)
    code.print()
    print("isValid?", code.isValid())
    result = code()
    if result < 0:
        print(-result, errno.errorcode[-result], os.strerror(-result))
