# PyShellCode

Execute ShellCode in Python.
In other words, allows to use "inline assembler" in Python.

This is intended as a simple project to learn more about x86-64 assembler and linux.
As well as serve for a easy platform to recreate cache-attacks and other side-channels attacks which require assembly.

Contains also some interesting code for CMake, to build shared-libraries which are executable and take command line arguments.


# Installation

  * cmake .
  * make
  * make install
  * make package (optional to build rpm, deb packages)


# Performance

In my tests PyShellCode yields the expected performance e.g.:
PyShellCode is 100 times faster than pure python and 10 times faster than numba
for equivalent implementations for finding the longest period of the collatz-sequence below a threshold.

python3 examples/collatz.py

Python [6.17894043999695, 6.065295364998747, 6.235952811999596]

Numba [0.603332129001501, 0.6196587439990253, 0.6055442029974074]

PyShellCode [0.06954922499426175, 0.06870782400073949, 0.06622266400518129]


# Resource

  * Linux Syscalls http://syscalls.kernelgrok.com/
  * x86 Assembler http://x86.renejeschke.de/
  * Flush+Flush Cache Attack https://github.com/IAIK/flush_flush
  * https://en.wikibooks.org/wiki/X86_Assembly/Interfacing_with_Linux
