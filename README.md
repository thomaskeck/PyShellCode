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

# Resource

  * Linux Syscalls http://syscalls.kernelgrok.com/
  * x86 Assembler http://x86.renejeschke.de/
  * Flush+Flush Cache Attack https://github.com/IAIK/flush_flush
