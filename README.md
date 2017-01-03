# PyShellCode

Execute ShellCode in Python.
In other words, allows to use "inline assembler" in Python.

There are three implementations:
  * C Implementation (Cimp.py) -- which is called wrapped using ctypes for usage in python, but can be used standalone as well
  * Python3 Implementation (PythonImp.py) -- does not require the shared library which is build by cmake, has the same interface as CImp
  * Python3 Implementation (Simple.py) -- most condensed implementation, pure python, just two functions (**use this**)

All the code is highly platform-dependent. In my case:
Linux thinkpad 4.8.0-2-amd64 #1 SMP Debian 4.8.11-1 (2016-12-02) x86_64 GNU/Linux

 **This is intended as a simple project to learn more about x86-64 assembler and linux (see paragraph Other Work)**
As well as serve for a easy platform to recreate cache-attacks and other side-channels attacks which require assembly.
If you want to use the code to do something similar I recommend reading the paragraph **Technical Details** below
and implement it yourself (or copy&paste Simple.py) since it's not hard once you know how-to do it.

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
The function *create_shellcode_from_nasmcode* in *Simple.py* does this for you.

A simple hello world shell-code looks like this
```python
shell_code = b"\xeb\x13\xb8\x01\x00\x00\x00\xbf\x01\x00\x00\x00\x5e\xba\x0f\x00\x00\x00\x0f\x05\xc3\xe8\xe8\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64\x21\x0a"
```

**Side note**: *Traditional* shell-code is concerned with avoiding 0-bytes, because it is typically injected 
into a unvalided user-input request. This isn't a problem if you just want to execute your code as inline-assembler,
because python-strings can contain 0-bytes.


Secondly we create a pice of executable memory in python and write our shell-code into this memory

```python
import mmap
shell_code = b'<Your Shell Code goes here>'
mm = mmap.mmap(-1, len(shell_code), flags=mmap.MAP_SHARED | mmap.MAP_ANONYMOUS, prot=mmap.PROT_WRITE | mmap.PROT_READ | mmap.PROT_EXEC)
mm.write(shell_code)
```

Finally we obtain the address of the memory and create a C Function Pointer using ctypes and this address:
```python
import ctypes
restype = ctypes.c_int64
argtypes = tuple()
ctypes_buffer = ctypes.c_int.from_buffer(mm)
function = ctypes.CFUNCTYPE(restype, *argtypes)(ctypes.addressof(ctypes_buffer))
function()
```

The function *create_function_from_shellcode* in *Simple.py* implements this.
As I stated above this code was meant as a learn-project.
I recommend using directly the code I described above (or Simple.py which basically contains this code) instead of PyShellCode itself,
because the dependency on the shared-library of the C-Implementation is unnecessary for you.

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


# Other work
  * https://gist.github.com/dcoles/4071130  -- Very similar to the code provided here, but uses mprotect instead of mmap to create an executable buffer
  * https://github.com//pycca/pycca -- Does not depend on external assembler, you can write assembler code directly in python in form of statements, supports C as well (alpha)
  * https://github.com/Maratyszcza/PeachPy -- Write assembler in python, generates object files and more
