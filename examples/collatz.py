from PyShellCode import ExecutableCode

import timeit

N = 10000


def python_maximum_collatz_length_below():
    n = N
    max_n = 0
    max_length = 1
    for i in range(1, n):
        j = i
        length = 1
        while True:
            if i == 1:
                break
            if i % 2 == 0:
                i = i / 2
            else:
                i = 3 * i + 1
            length += 1
        if max_length < length:
            max_length = length
            max_n = j
    return max_n


def nasm_maximum_collatz_length_below():
    return """
        push    rbp                                     ; 0000 _ 55
        mov     rbp, rsp                                ; 0001 _ 48: 89. E5
	mov 	rdi, {number}
        mov     qword [rbp-38H], rdi                    ; 0004 _ 48: 89. 7D, C8
        mov     qword [rbp-8H], 0                       ; 0008 _ 48: C7. 45, F8, 00000000
        mov     qword [rbp-10H], 1                      ; 0010 _ 48: C7. 45, F0, 00000001
        mov     qword [rbp-18H], 1                      ; 0018 _ 48: C7. 45, E8, 00000001
        jmp     L_007                                   ; 0020 _ EB, 76

L_001:  mov     rax, qword [rbp-18H]                    ; 0022 _ 48: 8B. 45, E8
        mov     qword [rbp-20H], rax                    ; 0026 _ 48: 89. 45, E0
        mov     qword [rbp-28H], 1                      ; 002A _ 48: C7. 45, D8, 00000001
L_002:  cmp     qword [rbp-20H], 1                      ; 0032 _ 48: 83. 7D, E0, 01
        jz      L_005                                   ; 0037 _ 74, 3F
        mov     rax, qword [rbp-20H]                    ; 0039 _ 48: 8B. 45, E0
        and     eax, 01H                                ; 003D _ 83. E0, 01
        test    rax, rax                                ; 0040 _ 48: 85. C0
        jnz     L_003                                   ; 0043 _ 75, 17
        mov     rax, qword [rbp-20H]                    ; 0045 _ 48: 8B. 45, E0
        mov     rdx, rax                                ; 0049 _ 48: 89. C2
        shr     rdx, 63                                 ; 004C _ 48: C1. EA, 3F
        add     rax, rdx                                ; 0050 _ 48: 01. D0
        sar     rax, 1                                  ; 0053 _ 48: D1. F8
        mov     qword [rbp-20H], rax                    ; 0056 _ 48: 89. 45, E0
        jmp     L_004                                   ; 005A _ EB, 15

L_003:  mov     rdx, qword [rbp-20H]                    ; 005C _ 48: 8B. 55, E0
        mov     rax, rdx                                ; 0060 _ 48: 89. D0
        add     rax, rax                                ; 0063 _ 48: 01. C0
        add     rax, rdx                                ; 0066 _ 48: 01. D0
        add     rax, 1                                  ; 0069 _ 48: 83. C0, 01
        mov     qword [rbp-20H], rax                    ; 006D _ 48: 89. 45, E0
L_004:  add     qword [rbp-28H], 1                      ; 0071 _ 48: 83. 45, D8, 01
        jmp     L_002                                   ; 0076 _ EB, BA

L_005:  nop                                             ; 0078 _ 90
        mov     rax, qword [rbp-10H]                    ; 0079 _ 48: 8B. 45, F0
        cmp     rax, qword [rbp-28H]                    ; 007D _ 48: 3B. 45, D8
        jge     L_006                                   ; 0081 _ 7D, 10
        mov     rax, qword [rbp-28H]                    ; 0083 _ 48: 8B. 45, D8
        mov     qword [rbp-10H], rax                    ; 0087 _ 48: 89. 45, F0
        mov     rax, qword [rbp-18H]                    ; 008B _ 48: 8B. 45, E8
        mov     qword [rbp-8H], rax                     ; 008F _ 48: 89. 45, F8
L_006:  add     qword [rbp-18H], 1                      ; 0093 _ 48: 83. 45, E8, 01
L_007:  mov     rax, qword [rbp-18H]                    ; 0098 _ 48: 8B. 45, E8
        cmp     rax, qword [rbp-38H]                    ; 009C _ 48: 3B. 45, C8
        jl      L_001                                   ; 00A0 _ 7C, 80
        mov     rax, qword [rbp-8H]                     ; 00A2 _ 48: 8B. 45, F8
        pop     rbp                                     ; 00A6 _ 5D
        ret                                             ; 00A7 _ C3
    """.format(number=N)
    
pyshellcode_maximum_collatz_length_below = ExecutableCode.ExecutableCode.from_NASMCode(nasm_maximum_collatz_length_below())

import numba
numba_maximum_collatz_length_below = numba.jit()(python_maximum_collatz_length_below)

if __name__ == '__main__':

    #print(python_maximum_collatz_length_below())
    #print(numba_maximum_collatz_length_below())
    #print(pyshellcode_maximum_collatz_length_below())

    print("Python", timeit.repeat("python_maximum_collatz_length_below()", "from __main__ import python_maximum_collatz_length_below", number=10))
    print("Numba", timeit.repeat("numba_maximum_collatz_length_below()", "from __main__ import numba_maximum_collatz_length_below", number=10))
    print("PyShellCode", timeit.repeat("pyshellcode_maximum_collatz_length_below()", "from __main__ import pyshellcode_maximum_collatz_length_below", number=10))

