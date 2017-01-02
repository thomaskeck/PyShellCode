from PyShellCode import ExecutableCode

if __name__ == '__main__':
    nasm_code = """
    jmp MESSAGE      ; 1) lets jump to MESSAGE
GOBACK:
    mov rax, 0x1
    mov rdi, 0x1
    pop rsi          ; 3) we are poping into `rdi`, now we have the
                     ; address of "Hello, World!" 
    mov rdx, 0xF
    syscall
    ret
MESSAGE:
    call GOBACK       ; 2) we are going back, since we used `call`, that means
                      ; the return address, which is in this case the address 
                      ; of "Hello, World!", is pushed into the stack.
    db "Hello, World!", 0ah, 000, 000
    """

    code = ExecutableCode.ExecutableCode.from_NASMCode(nasm_code)
    print("Is the generated Executable Code valid?", code.isValid())
    print("Generated Shell Code", code.print())
    print("Run code")
    result = code()
    print("Return value", result)
