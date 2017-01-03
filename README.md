# PyShellCode

Execute ShellCode in Python.
In other words, allows to use "inline assembler" in Python.

There are two implementations:
  * C Implementation -- which is called wrapped using ctypes for usage in python, but can be used standalone as well
  * Python3 Implementation -- does not require the shared library which is build by cmake
In my opinion the python implementation is superior and could be even better (more pythonic) if I wouldn't enforce
the same interface for both implementations.

All the code is highly platform-dependent in my case:
Linux thinkpad 4.8.0-2-amd64 #1 SMP Debian 4.8.11-1 (2016-12-02) x86_64 GNU/Linux

This is intended as a simple project to learn more about x86-64 assembler and linux.
As well as serve for a easy platform to recreate cache-attacks and other side-channels attacks which require assembly.
If you want to use the code to do something similar I recommend reading the paragraph **Technical Details** below
and implement it yourself since it's not hard once you know how-to do it.

Contains also some interesting code for CMake, to build shared-libraries which are executable and take command line arguments.


# Installation

  * cmake .
  * make
  * make install
  * make package (optional to build rpm, deb packages)

and/or (latter if you only require the Python version)

  * python3 setup.py install


# Technical Details

At first we require some shell-code (a binary string containing the correct opcodes which can directly be executed by your CPU).
One can create such a string by hand, or use an assembler like nasm to create it for you:

For instance, create a file shellcode.asm

```asm
global _start
section .text
_start:
    <Your Assembly Code goes here>
```

and execute:

```bash
nasm -f elf64 shellcode.asm -o shellcode.o
ld -o shellcode shellcode.o
for i in `objdump -d shellcode | tr '\t' ' ' | tr ' ' '\n' | egrep '^[0-9a-f]{2}$' ` ; do echo -n "\x$i" ; done
```
The class method *from_NASMCode* does this for you.

**Side note**: *Traditional* shell-code is concerned with avoiding 0-bytes, because it is typically injected 
into a unvalided user-input request. This isn't a problem if you just want to execute your code as inline-assembler,
because python-strings can contain 0-bytes.


Secondly we create a pice of executable memory in python and write our shell-code into this memory

```python
import mmap
shell_code = b'<Your Shell Code goes here>'
p = mmap.mmap(-1, len(shell_code), flags=mmap.MAP_SHARED | mmap.MAP_ANONYMOUS, prot=mmap.PROT_WRITE | mmap.PROT_READ | mmap.PROT_EXEC)
mm.write(shell_code)
```

Finally we obtain the address of the memory and create a C Function Pointer using ctypes and this address:
```python
import ctypes
restype = ctypes.c_int64
argtypes = tuple()
buffer = ctypes.c_int.from_buffer(memory_chunk)
func = ctypes.CFUNCTYPE(restype, *argtypes)(ctypes.addressof(buffer))
func()
```

The class *ExecutableCode* in the PyShellCode implements this. As I stated above this code was meant as a learn-project.
I recommend using directly the code I described above instead of PyShellCode itself.

The C-Implementation looks similar.


# Performance

In my tests PyShellCode yields the expected performance e.g.:
PyShellCode is 100 times faster than pure python and 10 times faster than numba
for equivalent implementations for finding the longest period of the collatz-sequence below a threshold.

python3 examples/collatz.py

Python [6.17894043999695, 6.065295364998747, 6.235952811999596]

Numba [0.603332129001501, 0.6196587439990253, 0.6055442029974074]

PyShellCode [0.06954922499426175, 0.06870782400073949, 0.06622266400518129]


# Resources

  * Linux Syscalls http://syscalls.kernelgrok.com/
  * x86 Assembler http://x86.renejeschke.de/
  * Flush+Flush Cache Attack https://github.com/IAIK/flush_flush
  * https://en.wikibooks.org/wiki/X86_Assembly/Interfacing_with_Linux
