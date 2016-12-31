SECTION .data       
array times 256 dq 0
SECTION .text       
global _start   
_start:
	mov eax, [array+128*8]
	add eax, 1
	mov [array+128*8], eax
	jmp _start
