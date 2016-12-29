; http://stackoverflow.com/questions/29652446/how-to-change-interpreter-path-and-pass-command-line-arguments-to-an-executable
; Glue Code which makes command line arguments possible for the main-function in a shared library
; Specific to 64-bit

global _main
extern main, _GLOBAL_OFFSET_TABLE_

section .text
BITS 64

_main:
        mov rdi, [rsp] ; argc
        mov rsi, rsp   ; address of argc
        add rsi, 8     ; address of argv
        call .getGOT
.getGOT:
        pop rbx
        add rbx,_GLOBAL_OFFSET_TABLE_+$$-.getGOT wrt ..gotpc
        jmp main wrt ..plt
