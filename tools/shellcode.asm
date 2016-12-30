; Adapted from http://stackoverflow.com/questions/15593214/linux-shellcode-hello-world
; Exchanged 32bit registers with 64bit (e -> r)
; Replaced exit syscall 
;    mov eax, 0x1
;    mov ebx, 0x0
;    int 0x80
; with function return (since our shellcode will be called as a function in execute_ExecutableCode)
;    ret

global _start

section .text

_start:
    jmp MESSAGE      ; 1) lets jump to MESSAGE

GOBACK:
    xor rax, rax
    xor rbx, rbx
    xor rcx, rcx
    xor rdx, rdx
    mov rax, 0x4
    mov rbx, 0x1
    pop rcx          ; 3) we are poping into `ecx`, now we have the
                     ; address of "Hello, World!\n" 
    mov rdx, 0xC
    int 0x80
    ;mov rax, 0x1
    ;mov rbx, 0x2
    ;int 0x80
    ret

MESSAGE:
    call GOBACK       ; 2) we are going back, since we used `call`, that means
                      ; the return address, which is in this case the address 
                      ; of "Hello, World!\r\n", is pushed into the stack.
    db "Hello, World!", 0ah, 000, 000
